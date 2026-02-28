from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.toast import toast

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread

KV = '''
MDScreen:
    MDRaisedButton:
        text: "Show Reward Ad"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_reward()
'''

if platform == "android":

    # 🔹 Reward Listener
    class RewardListener(PythonJavaClass):
        try:
            __javainterfaces__ = [
                'com/google/android/gms/ads/OnUserEarnedRewardListener'
            ]
            __javacontext__ = 'app'
    
            @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
            def onUserEarnedReward(self, rewardItem):
                toast("Reward mil gaya 🎉")
        except Exception as e:
            Clipboard.copy(str(e))       

    # 🔹 Load Callback
    class RewardLoadCallback(PythonJavaClass):
        try:
            __javainterfaces__ = [
                'com/google/android/gms/ads/rewarded/RewardedAdLoadCallback'
            ]
            __javacontext__ = 'app'
    
            def __init__(self, app):
                super().__init__()
                self.app = app
    
            @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
            def onAdLoaded(self, rewardedAd):
                self.app.rewarded_ad = rewardedAd
              
    
            @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
            def onAdFailedToLoad(self, error):
                Clipboard.copy('ADD NOT LOADED YET')
        except Exception as e:
            Clipboard.copy(str(e))                
            


class RewardApp(MDApp):

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            self.rewarded_ad = None
            self.load_reward()

    @run_on_ui_thread
    def load_reward(self):
        if platform != "android":
            return

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')

        activity = PythonActivity.mActivity
        MobileAds.initialize(activity)

        RewardedAd.load(
            activity,
            "ca-app-pub-3940256099942544/5224354917",  # 🔹 Test Reward ID
            AdRequest().build(),
            RewardLoadCallback(self)
        )

    @run_on_ui_thread
    def show_reward(self):
        try:
            if platform != "android":
                return
    
            if self.rewarded_ad:
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                self.rewarded_ad.show(activity, RewardListener())
                self.rewarded_ad = None
                self.load_reward()  # 🔄 Next ad preload
            else:
                toast("Ad not ready yet")
        except Exception as e:
            Clipboard.copy(str(e))

RewardApp().run()
