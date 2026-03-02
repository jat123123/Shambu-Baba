import traceback
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.clock import mainthread
from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread

# --- KV UI Design ---
KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            id: status_label
            text: "AdMob Status: Waiting..."
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            id: ad_btn
            text: "Watch Ad for Reward"
            pos_hint: {"center_x": .5}
            on_release: app.ad_manager.show_ad(app.give_reward)

        MDLabel:
            text: "Agar crash ho, toh error clipboard me copy ho jayega."
            halign: "center"
            font_style: "Caption"
'''

# --- Error Logging Function ---
def log_and_copy(loc, e):
    msg = f"LOC: {loc}\\nERR: {str(e)}\\nTRACE: {traceback.format_exc()}"
    Clipboard.copy(msg)
    print(msg)

# --- Java Classes ---
try:
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
except Exception as e:
    log_and_copy("Java_Import", e)

# --- Ad Callback Class ---
class AdLoadCallback(PythonJavaClass):
    __javaparent__ = 'com/google/android/gms/ads/rewarded/RewardedAdLoadCallback'
    __javainterfaces__ = []
    __javacontext__ = 'app'

    def __init__(self, manager):
        self.manager = manager
        super().__init__()

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
    def onAdLoaded(self, ad):
        try:
            self.manager.rewarded_ad = ad
            self.manager.update_status("Ad Ready!")
        except Exception as e:
            log_and_copy("onAdLoaded", e)

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        try:
            self.manager.rewarded_ad = None
            log_and_copy("onAdFailedToLoad", loadAdError.toString())
            self.manager.update_status("Ad Load Failed")
        except Exception as e:
            log_and_copy("onAdFailedToLoad_Ex", e)

# --- Reward Listener ---
class RewardListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/rewarded/OnUserEarnedRewardListener']
    __javacontext__ = 'app'

    def __init__(self, callback):
        self.callback = callback
        super().__init__()

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
    def onUserEarnedReward(self, reward):
        try:
            amount = reward.getAmount()
            self.callback(amount)
        except Exception as e:
            log_and_copy("onUserEarnedReward", e)

# --- Ad Manager ---
class AdMobManager:
    def __init__(self, app):
        self.app = app
        self.rewarded_ad = None
        self.ad_unit_id = "ca-app-pub-3940256099942544/5224354917" # Test ID

    @mainthread
    def update_status(self, text):
        self.app.root.ids.status_label.text = text

    @run_on_ui_thread
    def initialize_and_load(self):
        try:
            activity = PythonActivity.mActivity
            MobileAds.initialize(activity)
            
            builder = AdRequestBuilder()
            ad_request = builder.build()
            callback = AdLoadCallback(self)
            RewardedAd.load(activity, self.ad_unit_id, ad_request, callback)
        except Exception as e:
            log_and_copy("Init_Load", e)

    @run_on_ui_thread
    def show_ad(self, reward_callback):
        try:
            if self.rewarded_ad:
                activity = PythonActivity.mActivity
                listener = RewardListener(reward_callback)
                self.rewarded_ad.show(activity, listener)
                self.rewarded_ad = None
            else:
                self.initialize_and_load()
        except Exception as e:
            log_and_copy("Show_Ad", e)

# --- Main App ---
class MainApp(MDApp):
    def build(self):
        try:
            self.theme_cls.primary_palette = "DeepPurple"
            self.ad_manager = AdMobManager(self)
            self.ad_manager.initialize_and_load()
            return Builder.load_string(KV)
        except Exception as e:
            log_and_copy("App_Build", e)

    @mainthread
    def give_reward(self, amount):
        try:
            self.root.ids.status_label.text = f"Mubarak! Reward: {amount}"
            self.ad_manager.initialize_and_load()
        except Exception as e:
            log_and_copy("Give_Reward", e)

if __name__ == "__main__":
    try:
        MainApp().run()
    except Exception as e:
        log_and_copy("Fatal_Crash", e)
        
