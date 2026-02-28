from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock

# ---------------- ANDROID PART ----------------
if platform == "android":
    from jnius import autoclass, cast, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread

    # Java Classes
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
    AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
    InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")

    # ----------- CORRECT CALLBACK -----------
    class AdLoadCallback(PythonJavaClass):
        __javaclass__ = "com/google/android/gms/ads/interstitial/InterstitialAdLoadCallback"
        __javacontext__ = "app"

        def __init__(self, app_instance):
            super().__init__()
            self.app_instance = app_instance

        @java_method("(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V")
        def onAdLoaded(self, interstitialAd):
            print("Ad Loaded")
            self.app_instance.update_status("Ad Loaded! Showing...")
            self.app_instance.show_ad(interstitialAd)

        @java_method("(Lcom/google/android/gms/ads/LoadAdError;)V")
        def onAdFailedToLoad(self, loadAdError):
            print("Ad Failed")
            self.app_instance.update_status("Ad Failed To Load")


# ---------------- KV UI ----------------
KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDTopAppBar:
            title: "Interstitial Final Fix"

        MDRaisedButton:
            text: "LOAD & SHOW AD"
            pos_hint: {"center_x": .5}
            on_release: app.start_ad()

        MDLabel:
            id: status_label
            text: "Status: Ready"
            halign: "center"
'''


# ---------------- MAIN APP ----------------
class MainApp(MDApp):

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            MobileAds.initialize(activity)
            print("MobileAds Initialized")

    def update_status(self, text):
        self.root.ids.status_label.text = f"Status: {text}"

    def start_ad(self):
        if platform == "android":
            self.update_status("Requesting Ad...")
            Clock.schedule_once(self.load_ad, 0.3)
        else:
            self.update_status("Desktop - Ads Not Supported")

    # -------- LOAD ON UI THREAD --------
    if platform == "android":
        @run_on_ui_thread
        def load_ad(self, dt):
            try:
                activity = cast("android.app.Activity", PythonActivity.mActivity)

                ad_request = AdRequestBuilder().build()
                test_unit_id = "ca-app-pub-3940256099942544/1033173712"

                callback = AdLoadCallback(self)

                InterstitialAd.load(
                    activity,
                    test_unit_id,
                    ad_request,
                    callback
                )

            except Exception as e:
                self.update_status(f"Error: {str(e)}")

        # -------- SHOW ON UI THREAD --------
        @run_on_ui_thread
        def show_ad(self, interstitialAd):
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            interstitialAd.show(activity)


if __name__ == "__main__":
    MainApp().run()
