from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.toast import toast
from kivy.core.clipboard import Clipboard # 👈 Clipboard fix

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
else:
    # Dummy decorator for PC testing
    def run_on_ui_thread(func):
        return func

KV = '''
MDScreen:
    MDRaisedButton:
        text: "Show Reward Ad"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_reward()
'''

if platform == "android":
    # 🔹 Reward Listener Fix
    class RewardListener(PythonJavaClass):
        __javainterfaces__ = ['com/google/android/gms/ads/OnUserEarnedRewardListener']
        __javacontext__ = 'app'

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
        def onUserEarnedReward(self, rewardItem):
            self.callback()

    # 🔹 Load Callback Fix
    class RewardLoadCallback(PythonJavaClass):
        __javainterfaces__ = ['com/google/android/gms/ads/rewarded/RewardedAdLoadCallback']
        __javacontext__ = 'app'

        def __init__(self, app):
            super().__init__()
            self.app = app

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
        def onAdLoaded(self, rewardedAd):
            self.app.rewarded_ad = rewardedAd
            print("Ad Loaded Successfully")

        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onAdFailedToLoad(self, error):
            print(f"Ad Failed to Load: {error.toString()}")
            self.app.rewarded_ad = None

class RewardApp(MDApp):
    rewarded_ad = None

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            self.load_reward()

    @run_on_ui_thread
    def load_reward(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
            AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
            
            activity = PythonActivity.mActivity
            
            # Request build
            ad_request = AdRequest().build()
            
            RewardedAd.load(
                activity,
                "ca-app-pub-3940256099942544/5224354917", # Test ID
                ad_request,
                RewardLoadCallback(self)
            )
        except Exception as e:
            print(f"Load Error: {str(e)}")

    def on_reward_earned(self):
        toast("Reward mil gaya 🎉")

    @run_on_ui_thread
    def show_reward(self):
        if platform != "android":
            toast("Kivy is not on Android")
            return

        if self.rewarded_ad:
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.rewarded_ad.show(activity, RewardListener(self.on_reward_earned))
            self.rewarded_ad = None # Reset after showing
            self.load_reward() # Reload next ad
        else:
            toast("Ad loading... please wait")
            self.load_reward()

RewardApp().run()
