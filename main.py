from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.clipboard import Clipboard

if platform == "android":
    try:
        from jnius import autoclass, cast, PythonJavaClass, java_method
        from android.runnable import run_on_ui_thread
    
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
        AdRequest = autoclass("com.google.android.gms.ads.AdRequest$Builder")
        InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")
        
        # --- FIX ATTEMPT: Yahan hum generic Object use karenge ---
        class AdLoadCallback(PythonJavaClass):
            # Agar ye 'interface' nahi hai, toh hum ise base class ki tarah define karte hain
            # Note: PyJnius mein abstract classes support karna thoda tricky hai
            __javainterfaces__ = ["com/google/android/gms/ads/admanager/AppEventListener"] # Optional dummy
            __javacontext__ = "app"

            def __init__(self, app_instance):
                super().__init__()
                self.app = app_instance

            @java_method("(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V")
            def onAdLoaded(self, interstitialAd):
                self.app.interstitial_ad = interstitialAd
                self.app.update_status("Ad Loaded! Ready.")

            @java_method("(Lcom/google/android/gms/ads/LoadAdError;)V")
            def onAdFailedToLoad(self, loadAdError):
                self.app.interstitial_ad = None
                self.app.update_status("Load Failed")
                Clipboard.copy(f"Failed: {loadAdError.toString()}")

    except Exception as e:
        Clipboard.copy(f"Import Error: {e}")

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"
        MDTopAppBar:
            title: "AdMob Fix v3"
        MDRaisedButton:
            text: "LOAD AD"
            on_release: app.load_ad_process()
        MDRaisedButton:
            text: "SHOW AD"
            on_release: app.show_ad_process()
        MDLabel:
            id: status_label
            text: "Status: Ready"
            halign: "center"
'''

class MainApp(MDApp):
    def build(self):
        self.interstitial_ad = None
        return Builder.load_string(KV)

    def update_status(self, text):
        self.root.ids.status_label.text = f"Status: {text}"

    def load_ad_process(self):
        if platform == "android":
            self.actual_load_logic()
        else:
            self.update_status("Desktop not supported")

    @run_on_ui_thread
    def actual_load_logic(self):
        try:
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            ad_request = AdRequest().build()
            test_id = "ca-app-pub-3940256099942544/1033173712"
            
            # Yahan problem hai: Java expects an Abstract Class, Python gives an Interface
            # Ek alternative: Kivy's 'android-ads' package use karna jo ye handles karta hai
            callback = AdLoadCallback(self)
            InterstitialAd.load(activity, test_id, ad_request, callback)
            
        except Exception as e:
            Clipboard.copy(f"Logic Error: {e}")
            self.update_status("Logic Error (Check Clipboard)")

    @run_on_ui_thread
    def show_ad_process(self):
        if self.interstitial_ad:
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            self.interstitial_ad.show(activity)
            self.interstitial_ad = None
        else:
            self.update_status("No Ad Loaded")

if __name__ == "__main__":
    MainApp().run()
    
