import traceback
import sys

# Sabse pehle clipboard aur basic imports ka check
try:
    from kivymd.app import MDApp
    from kivy.lang import Builder
    from kivy.core.clipboard import Clipboard
    from kivy.clock import mainthread
    from kivy.utils import platform
except Exception as e:
    # Agar basic Kivy hi fail ho jaye toh console par print karega
    print(f"Basic Import Error: {str(e)}")

# --- Global Error Logger (Traceback ke saath) ---
def copy_detailed_error(location, error):
    try:
        full_trace = traceback.format_exc()
        err_msg = f"STEP: {location}\nERROR: {str(error)}\nTRACEBACK:\n{full_trace}"
        Clipboard.copy(err_msg) # Clipboard me copy karega
        print(err_msg) # Logcat me print karega
    except:
        print(f"Critical Error in Logger at {location}")

# --- UI String Check ---
try:
    KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            id: status_label
            text: "AdMob Status: Ready"
            halign: "center"
            theme_text_color: "Primary"

        MDRaisedButton:
            id: main_btn
            text: "Watch Ad"
            pos_hint: {"center_x": .5}
            on_release: app.show_ad()
'''
except Exception as e:
    copy_detailed_error("KV_String_Definition", e)

# --- Android Specific Imports ---
if platform == "android":
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
    except Exception as e:
        copy_detailed_error("Jnius_Import_Step", e)

    try:
        AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
        RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except Exception as e:
        copy_detailed_error("Autoclass_Import_Step", e)
else:
    def run_on_ui_thread(f): return f

# --- Ad Load Callback Class ---
class MyAdLoadCallback(PythonJavaClass):
    __javaparent__ = 'com/google/android/gms/ads/rewarded/RewardedAdLoadCallback'
    __javacontext__ = 'app'
    __javainterfaces__ = []

    def __init__(self, app):
        try:
            self.app = app
        except Exception as e: copy_detailed_error("Callback_Init_Attr", e)
        try:
            super().__init__()
        except Exception as e: copy_detailed_error("Callback_Super_Init", e)

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
    def onAdLoaded(self, ad):
        try:
            self.app.rewarded_ad = ad
        except Exception as e: copy_detailed_error("onAdLoaded_Assign", e)
        try:
            self.app.update_ui_status("Ad Loaded! Press Show.")
        except Exception as e: copy_detailed_error("onAdLoaded_UI_Call", e)

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        try:
            self.app.rewarded_ad = None
            err_str = loadAdError.toString()
            copy_detailed_error("onAdFailedToLoad_Java_Side", err_str)
            self.app.update_ui_status(f"Load Failed: {err_str}")
        except Exception as e: copy_detailed_error("onAdFailedToLoad_Exception", e)

# --- Reward Listener Class ---
class MyRewardListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/rewarded/OnUserEarnedRewardListener']
    __javacontext__ = 'app'

    def __init__(self, app):
        try:
            self.app = app
            super().__init__()
        except Exception as e: copy_detailed_error("RewardListener_Init", e)

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
    def onUserEarnedReward(self, reward):
        try:
            amount = reward.getAmount()
            self.app.give_reward(amount)
        except Exception as e: copy_detailed_error("onUserEarnedReward_Callback", e)

# --- Main App ---
class MainApp(MDApp):
    rewarded_ad = None
    ad_unit_id = "ca-app-pub-3940256099942544/5224354917"

    def build(self):
        try:
            self.theme_cls.primary_palette = "Blue"
        except Exception as e: copy_detailed_error("Theme_Setup", e)
        
        try:
            self.load_ad()
        except Exception as e: copy_detailed_error("Initial_Load_Call", e)
        
        try:
            return Builder.load_string(KV)
        except Exception as e:
            copy_detailed_error("Builder_Load_String", e)
            return MDScreen()

    @run_on_ui_thread
    def load_ad(self):
        try:
            if platform == "android":
                try:
                    activity = PythonActivity.mActivity
                    MobileAds.initialize(activity)
                except Exception as e: copy_detailed_error("MobileAds_Init", e)

                try:
                    builder_instance = AdRequestBuilder()
                    ad_request = builder_instance.build()
                except Exception as e: copy_detailed_error("AdRequest_Build", e)

                try:
                    callback = MyAdLoadCallback(self)
                    RewardedAd.load(activity, self.ad_unit_id, ad_request, callback)
                except Exception as e: copy_detailed_error("RewardedAd_Load_Call", e)
                
                self.update_ui_status("Loading Ad...")
        except Exception as e:
            copy_detailed_error("Full_load_ad_Method", e)

    def show_ad(self):
        try:
            if self.rewarded_ad:
                self.display_now()
            else:
                self.update_ui_status("Ad not ready. Loading...")
                self.load_ad()
        except Exception as e: copy_detailed_error("show_ad_Button", e)

    @run_on_ui_thread
    def display_now(self):
        try:
            activity = PythonActivity.mActivity
            listener = MyRewardListener(self)
            self.rewarded_ad.show(activity, listener)
            self.rewarded_ad = None
        except Exception as e: copy_detailed_error("Display_Now_Method", e)

    @mainthread
    def update_ui_status(self, text):
        try:
            self.root.ids.status_label.text = str(text)
        except Exception as e: copy_detailed_error("Update_UI_Status_Step", e)

    @mainthread
    def give_reward(self, amount):
        try:
            self.update_ui_status(f"Mubarak! Reward: {amount}")
            self.load_ad()
        except Exception as e: copy_detailed_error("Give_Reward_Step", e)

if __name__ == "__main__":
    try:
        MainApp().run()
    except Exception as e:
        # Final catch for everything
        copy_detailed_error("FINAL_APP_RUN", e)
        
