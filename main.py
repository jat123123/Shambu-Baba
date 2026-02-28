from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

# Android specific imports aur Global Class
if platform == "android":
    try:
        from jnius import autoclass, cast, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
    
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
        AdRequest = autoclass("com.google.android.gms.ads.AdRequest$Builder")
        InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")
        
        # Callback class jo Java interface ko handle karegi
        class AdLoadCallback(PythonJavaClass):
            __javainterfaces__ = ["com/google/android/gms/ads/interstitial/InterstitialAdLoadCallback"]
            __javacontext__ = "app"

            def __init__(self, app_instance):
                super().__init__()
                self.app = app_instance

            @java_method("(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V")
            def onAdLoaded(self, interstitialAd):
                self.app.interstitial_ad = interstitialAd
                self.app.update_status("Ad Loaded! Click SHOW AD")

            @java_method("(Lcom/google/android/gms/ads/LoadAdError;)V")
            def onAdFailedToLoad(self, loadAdError):
                self.app.interstitial_ad = None
                err = f"Load Failed: {loadAdError.toString()}"
                self.app.update_status(err)
                Clipboard.copy(f"onAdFailedToLoad :- {err}")

    except Exception as e:
        Clipboard.copy(f"Import Error :- {str(e)}")

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDTopAppBar:
            title: "AdMob Interstitial Fixed"

        MDRaisedButton:
            text: "1. LOAD AD"
            pos_hint: {"center_x": .5}
            on_release: app.load_ad_process()

        MDRaisedButton:
            text: "2. SHOW AD"
            pos_hint: {"center_x": .5}
            on_release: app.show_ad_process()       

        MDLabel:
            id: status_label
            text: "Status: Ready"
            halign: "center"
'''

class MainApp(MDApp):
    def build(self):
        self.interstitial_ad = None
        self.callback_handler = None
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            try:
                activity = cast("android.app.Activity", PythonActivity.mActivity)
                MobileAds.initialize(activity)
                self.update_status("Ads Initialized")
            except Exception as e:
                err = f"Init Error: {e}"
                self.update_status(err)
                Clipboard.copy(f"on_start :- {err}")

    def update_status(self, text):
        self.root.ids.status_label.text = f"Status: {text}"

    def load_ad_process(self):
        if platform == "android":
            self.update_status("Loading...")
            self.actual_load_logic()
        else:
            self.update_status("Not on Android")

    @run_on_ui_thread
    def actual_load_logic(self):
        try:
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            ad_request = AdRequest().build()
            test_id = "ca-app-pub-3940256099942544/1033173712"
            
            # Callback handler ko set karna zaroori hai (Fix)
            self.callback_handler = AdLoadCallback(self)
            InterstitialAd.load(activity, test_id, ad_request, self.callback_handler)
        except Exception as e:
            err = str(e)
            self.update_status(f"Load Exception: {err}")
            Clipboard.copy(f"actual_load_logic :- {err}")

    def show_ad_process(self):
        if platform == "android":
            if self.interstitial_ad:
                self.actual_show_logic()
            else:
                self.update_status("Ad Not Loaded Yet!")
        else:
            self.update_status("Not on Android")

    @run_on_ui_thread
    def actual_show_logic(self):
        try:
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            self.interstitial_ad.show(activity)
            self.interstitial_ad = None # Clear after use
            self.update_status("Ad Shown")
        except Exception as e:
            err = str(e)
            self.update_status(f"Show Error: {err}")
            Clipboard.copy(f"actual_show_logic :- {err}")

if __name__ == "__main__":
    MainApp().run()
    
