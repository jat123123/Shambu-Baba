import traceback
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.clock import mainthread
from kivy.utils import platform

# --- Error Logger ---
def full_log(loc, e):
    msg = f"STEP: {loc}\nERR: {str(e)}\n{traceback.format_exc()}"
    Clipboard.copy(msg)
    print(msg)

# --- UI Design ---
KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            id: status_label
            text: "Status: Ready"
            halign: "center"

        MDRaisedButton:
            text: "1. Initialize & Load Ad"
            pos_hint: {"center_x": .5}
            on_release: app.manual_init_load()

        MDRaisedButton:
            text: "2. Show Ad"
            pos_hint: {"center_x": .5}
            on_release: app.show_ad()
'''

if platform == "android":
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
        RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
    except Exception as e:
        full_log("Jnius_Imports", e)
else:
    def run_on_ui_thread(f): return f

# --- Callback Classes ---
class MyAdLoadCallback(PythonJavaClass):
    __javaparent__ = 'com/google/android/gms/ads/rewarded/RewardedAdLoadCallback'
    __javacontext__ = 'app'
    __javainterfaces__ = []

    def __init__(self, app):
        self.app = app
        super().__init__()

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
    def onAdLoaded(self, ad):
        try:
            self.app.rewarded_ad = ad
            self.app.update_label("Ad Loaded! Now press Show.")
        except Exception as e: full_log("onAdLoaded", e)

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        try:
            self.app.update_label(f"Failed: {loadAdError.toString()}")
        except Exception as e: full_log("onAdFailed", e)

class MyRewardListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/rewarded/OnUserEarnedRewardListener']
    __javacontext__ = 'app'

    def __init__(self, app):
        self.app = app
        super().__init__()

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
    def onUserEarnedReward(self, reward):
        try:
            self.app.reward_success(reward.getAmount())
        except Exception as e: full_log("onReward", e)

# --- App Class ---
class MainApp(MDApp):
    rewarded_ad = None
    ad_unit_id = "ca-app-pub-3940256099942544/5224354917"

    def build(self):
        return Builder.load_string(KV)

    def manual_init_load(self):
        self.update_label("Initializing...")
        self.load_ad_logic()

    @run_on_ui_thread
    def load_ad_logic(self):
        try:
            activity = PythonActivity.mActivity
            MobileAds.initialize(activity) # <--- YAHAN CRASH HOGA AGAR SPEC GALAT HAI
            
            builder = AdRequestBuilder().build()
            callback = MyAdLoadCallback(self)
            RewardedAd.load(activity, self.ad_unit_id, builder, callback)
        except Exception as e:
            full_log("Load_Logic_Crash", e)

    def show_ad(self):
        if self.rewarded_ad:
            self.display_now()
        else:
            self.update_label("Ad not loaded yet!")

    @run_on_ui_thread
    def display_now(self):
        try:
            activity = PythonActivity.mActivity
            listener = MyRewardListener(self)
            self.rewarded_ad.show(activity, listener)
            self.rewarded_ad = None
        except Exception as e: full_log("Display_Crash", e)

    @mainthread
    def update_label(self, txt):
        self.root.ids.status_label.text = txt

    @mainthread
    def reward_success(self, amt):
        self.update_label(f"Mubarak! Reward: {amt}")

if __name__ == "__main__":
    try:
        MainApp().run()
    except Exception as e:
        full_log("Fatal_Crash", e)
        
