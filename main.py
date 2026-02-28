from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.logger import Logger
from kivy.clock import Clock # UI update ke liye zaroori hai

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method, cast
    from android.runnable import run_on_ui_thread

    # Android AdMob Classes
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    
    class RewardedAdLoadCallback(PythonJavaClass):
        __javainterfaces__ = ['com.google.android.gms.ads.rewarded.RewardedAdLoadCallback']
        __javacontext__ = 'app'

        def __init__(self, app_instance):
            super().__init__()
            self.app = app_instance

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
        def onAdLoaded(self, rewardedAd):
            Logger.info("KivMob: Ad Loaded Successfully!")
            self.app.mRewardedAd = rewardedAd
            # UI update hamesha Clock ke zariye karein
            Clock.schedule_once(lambda dt: self.app.update_status("Ad Loaded! Press Show."))

        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onAdFailedToLoad(self, loadAdError):
            err_msg = loadAdError.getMessage()
            Logger.info(f"KivMob: Ad Failed - {err_msg}")
            self.app.mRewardedAd = None
            Clock.schedule_once(lambda dt: self.app.update_status(f"Failed: {err_msg}"))

    class OnUserEarnedRewardListener(PythonJavaClass):
        __javainterfaces__ = ['com.google.android.gms.ads.OnUserEarnedRewardListener']
        __javacontext__ = 'app'

        def __init__(self, app_instance):
            super().__init__()
            self.app = app_instance

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
        def onUserEarnedReward(self, rewardItem):
            amount = rewardItem.getAmount()
            reward_type = rewardItem.getType()
            Clock.schedule_once(lambda dt: self.app.give_reward(amount, reward_type))
else:
    def run_on_ui_thread(x): return x

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "20dp"
        padding: "20dp"

        MDLabel:
            text: "AdMob Rewarded Integration"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: status
            text: "Status: Ready"
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            text: "1. LOAD REWARDED AD"
            pos_hint: {"center_x": .5}
            on_release: app.load_rewarded_ad()

        MDFillRoundFlatButton:
            text: "2. SHOW AD & GET COINS"
            pos_hint: {"center_x": .5}
            on_release: app.show_rewarded_ad()
'''

class MainApp(MDApp):
    mRewardedAd = None

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        if platform == "android":
            self.activity = PythonActivity.mActivity
            # Initialize Mobile Ads
            MobileAds.initialize(self.activity)
        return Builder.load_string(KV)

    def update_status(self, text):
        self.root.ids.status.text = text

    @run_on_ui_thread
    def load_rewarded_ad(self):
        if platform != "android":
            self.update_status("PC: Simulating Load...")
            return

        self.update_status("Loading Ad...")
        # TEST ID: Isse hamesha ad aana chahiye
        ad_unit_id = "ca-app-pub-3940256099942544/5224354917" 
        ad_request = AdRequestBuilder().build()
        
        # Casting is IMPORTANT for Python to Java callback
        load_callback = RewardedAdLoadCallback(self)
        j_callback = cast('com.google.android.gms.ads.rewarded.RewardedAdLoadCallback', load_callback)
        
        RewardedAd.load(self.activity, ad_unit_id, ad_request, j_callback)

    @run_on_ui_thread
    def show_rewarded_ad(self):
        if platform == "android":
            if self.mRewardedAd:
                listener = OnUserEarnedRewardListener(self)
                j_listener = cast('com.google.android.gms.ads.OnUserEarnedRewardListener', listener)
                self.mRewardedAd.show(self.activity, j_listener)
            else:
                self.update_status("Ad not loaded yet!")
        else:
            self.give_reward(10, "Test-Coins")

    def give_reward(self, amount, type):
        self.root.ids.status.text = f"SUCCESS! Received {amount} {type}"
        self.root.ids.status.theme_text_color = "Primary"

if __name__ == "__main__":
    MainApp().run()
    
