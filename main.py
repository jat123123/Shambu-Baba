from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivy.core.clipboard import Clipboard
from kivy.clock import mainthread
from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread

# --- Error Logger (Clipboard me copy karega) ---
def log_error(location, error):
    err_msg = f"Error in {location}: {str(error)}"
    Clipboard.copy(err_msg)
    print(err_msg)

# --- Java Classes Import ---
try:
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
except Exception as e:
    log_error("Java_Imports", e)

# --- Ad Load Callback (FIXED) ---
class AdLoadCallback(PythonJavaClass):
    # Abstract class ke liye __javaparent__ use hota hai
    __javaparent__ = 'com/google/android/gms/ads/rewarded/RewardedAdLoadCallback'
    # ERROR FIX: Khali list dena zaroori hai
    __javainterfaces__ = []
    __javacontext__ = 'app'

    def __init__(self, manager):
        try:
            self.manager = manager
            super().__init__()
        except Exception as e:
            log_error("AdLoadCallback_Init", e)

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
    def onAdLoaded(self, ad):
        try:
            self.manager.rewarded_ad = ad
            print("Ad Load Ho Gayi!")
        except Exception as e:
            log_error("onAdLoaded_Method", e)

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        try:
            self.manager.rewarded_ad = None
            log_error("onAdFailedToLoad", loadAdError.toString())
        except Exception as e:
            log_error("onAdFailedToLoad_Exception", e)

# --- Reward Listener ---
class RewardListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/rewarded/OnUserEarnedRewardListener']
    __javacontext__ = 'app'

    def __init__(self, callback):
        try:
            self.callback = callback
            super().__init__()
        except Exception as e:
            log_error("RewardListener_Init", e)

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
    def onUserEarnedReward(self, reward):
        try:
            amount = reward.getAmount()
            self.callback(amount)
        except Exception as e:
            log_error("onUserEarnedReward", e)

# --- AdMob Manager ---
class AdMobManager:
    def __init__(self):
        self.rewarded_ad = None
        # Google Test ID
        self.ad_unit_id = "ca-app-pub-3940256099942544/5224354917"

    @run_on_ui_thread
    def load_rewarded_ad(self):
        try:
            activity = PythonActivity.mActivity
            builder = AdRequestBuilder()
            ad_request = builder.build()
            
            callback = AdLoadCallback(self)
            RewardedAd.load(activity, self.ad_unit_id, ad_request, callback)
        except Exception as e:
            log_error("load_rewarded_ad_Method", e)

    @run_on_ui_thread
    def show_ad(self, reward_callback):
        try:
            if self.rewarded_ad:
                activity = PythonActivity.mActivity
                listener = RewardListener(reward_callback)
                self.rewarded_ad.show(activity, listener)
                self.rewarded_ad = None 
            else:
                log_error("show_ad", "Ad Ready Nahi Hai! Loading...")
                self.load_rewarded_ad()
        except Exception as e:
            log_error("show_ad_Method", e)

# --- Main App ---
class MainApp(MDApp):
    def build(self):
        try:
            self.ad_manager = AdMobManager()
            self.ad_manager.load_rewarded_ad()
            
            screen = MDScreen()
            self.btn = MDRaisedButton(
                text="Watch Ad for Reward",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_release=lambda x: self.ad_manager.show_ad(self.give_reward)
            )
            screen.add_widget(self.btn)
            return screen
        except Exception as e:
            log_error("MainApp_Build", e)

    @mainthread
    def give_reward(self, amount):
        # Reward milne ke baad UI update
        self.btn.text = f"Mubarak ho! {amount} Points Mile"
        self.ad_manager.load_rewarded_ad() # Dusri ad load karein

if __name__ == "__main__":
    try:
        MainApp().run()
    except Exception as e:
        Clipboard.copy(f"FATAL: {e}")
        
