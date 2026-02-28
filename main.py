from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.logger import Logger

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method, cast
    from android.runnable import run_on_ui_thread

    # Android AdMob Classes
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequestBuilder') # Fix: Direct Builder class
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    
    # Callback class for Loading
    class RewardedAdLoadCallback(PythonJavaClass):
        __javainterfaces__ = ['com/google/android/gms/ads/rewarded/RewardedAdLoadCallback']
        __javacontext__ = 'app'

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
        def onAdLoaded(self, rewardedAd):
            self.callback(rewardedAd, "loaded")

        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onAdFailedToLoad(self, loadAdError):
            self.callback(None, "failed")

    # Callback class for Reward
    class OnUserEarnedRewardListener(PythonJavaClass):
        __javainterfaces__ = ['com/google/android/gms/ads/OnUserEarnedRewardListener']
        __javacontext__ = 'app'

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
        def onUserEarnedReward(self, rewardItem):
            self.callback(rewardItem.getAmount(), rewardItem.getType())

else:
    def run_on_ui_thread(x): return lambda *args: None

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            id: status
            text: "Banner Working? Let's fix Rewarded!"
            halign: "center"

        MDRaisedButton:
            text: "LOAD REWARDED"
            pos_hint: {"center_x": .5}
            on_release: app.load_rewarded_ad()

        MDFillRoundFlatButton:
            text: "SHOW REWARDED"
            pos_hint: {"center_x": .5}
            on_release: app.show_rewarded_ad()
'''

class MainApp(MDApp):
    mRewardedAd = None

    def build(self):
        if platform == "android":
            self.activity = PythonActivity.mActivity
            MobileAds.initialize(self.activity)
        return Builder.load_string(KV)

    def on_ad_result(self, ad, status):
        if status == "loaded":
            self.mRewardedAd = ad
            self.root.ids.status.text = "SUCCESS: Ad Loaded!"
        else:
            self.root.ids.status.text = "ERROR: Ad Failed to Load"

    @run_on_ui_thread
    def load_rewarded_ad(self):
        if platform != "android": return
        
        self.root.ids.status.text = "Loading Rewarded..."
        ad_unit_id = "ca-app-pub-3940256099942544/5224354917" # Test ID
        
        # Build Request
        ad_request = AdRequestBuilder().build()
        
        # Load with Casted Callback
        loader = RewardedAdLoadCallback(self.on_ad_result)
        j_loader = cast('com/google/android/gms/ads/rewarded/RewardedAdLoadCallback', loader)
        
        RewardedAd.load(self.activity, ad_unit_id, ad_request, j_loader)

    @run_on_ui_thread
    def show_rewarded_ad(self):
        if self.mRewardedAd:
            reward_listener = OnUserEarnedRewardListener(self.give_reward)
            j_listener = cast('com/google/android/gms/ads/OnUserEarnedRewardListener', reward_listener)
            self.mRewardedAd.show(self.activity, j_listener)
        else:
            self.root.ids.status.text = "Load ad first!"

    def give_reward(self, amount, r_type):
        self.root.ids.status.text = f"REWARD: {amount} {r_type} received!"

if __name__ == "__main__":
    MainApp().run()
    
