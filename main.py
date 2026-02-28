from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.toast import toast
from kivy.core.clipboard import Clipboard
import traceback

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
else:
    def run_on_ui_thread(func):
        return func

KV = '''
MDScreen:
    MDRaisedButton:
        text: "Show Reward Ad"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_reward()
'''

# --- ANDROID SPECIFIC CLASSES ---
if platform == "android":
    
    # 1. Reward Listener (Interface)
    class RewardListener(PythonJavaClass):
        __javainterfaces__ = ['com/google/android/gms/ads/OnUserEarnedRewardListener']
        __javacontext__ = 'app'

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
        def onUserEarnedReward(self, rewardItem):
            self.callback()

    # 2. Load Callback (Abstract Class Fix)
    class RewardLoadCallback(PythonJavaClass):
        # FIX: RewardedAdLoadCallback is an Abstract Class, so use __javabase__
        __javabase__ = 'com/google/android/gms/ads/rewarded/RewardedAdLoadCallback'
        __javacontext__ = 'app'

        def __init__(self, app):
            super().__init__()
            self.app = app

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
        def onAdLoaded(self, rewardedAd):
            self.app.rewarded_ad = rewardedAd
            Clipboard.copy("Success: Ad Loaded")
            toast("Ad Ready!")

        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onAdFailedToLoad(self, error):
            err_msg = f"Ad Load Failed: {error.toString()}"
            Clipboard.copy(err_msg)
            self.app.rewarded_ad = None

class RewardApp(MDApp):
    rewarded_ad = None

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            # Thoda delay dekar load karte hain taaki app crash na ho startup pe
            self.load_reward()

    @run_on_ui_thread
    def load_reward(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
            AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
            
            activity = PythonActivity.mActivity
            ad_request = AdRequest().build()
            
            # Test Ad Unit ID
            ad_unit_id = "ca-app-pub-3940256099942544/5224354917"
            
            RewardedAd.load(
                activity,
                ad_unit_id,
                ad_request,
                RewardLoadCallback(self)
            )
        except Exception as e:
            # Pura error trace copy karega
            Clipboard.copy(f"Load Error: {traceback.format_exc()}")

    def on_reward_earned(self):
        toast("Reward mil gaya 🎉")
        Clipboard.copy("Reward Successfully Earned!")

    @run_on_ui_thread
    def show_reward(self):
        if platform != "android":
            toast("Only works on Android")
            return

        try:
            if self.rewarded_ad:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                
                self.rewarded_ad.show(activity, RewardListener(self.on_reward_earned))
                self.rewarded_ad = None 
                self.load_reward() 
            else:
                toast("Ad loading... please wait")
                self.load_reward()
        except Exception as e:
            Clipboard.copy(f"Show Error: {traceback.format_exc()}")

if __name__ == "__main__":
    try:
        RewardApp().run()
    except Exception as e:
        Clipboard.copy(f"App Crash: {traceback.format_exc()}")
        
