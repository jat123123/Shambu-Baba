from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock

if platform == "android":
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
    AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
    InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDTopAppBar:
            title: "Stable Interstitial"

        MDRaisedButton:
            text: "LOAD & SHOW AD"
            pos_hint: {"center_x": .5}
            on_release: app.load_and_show()

        MDLabel:
            id: status_label
            text: "Status: Ready"
            halign: "center"
'''

class MainApp(MDApp):

    def build(self):
        self.interstitial_ad = None
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            MobileAds.initialize(activity)

    def update_status(self, text):
        self.root.ids.status_label.text = f"Status: {text}"

    def load_and_show(self):
        if platform == "android":
            self.update_status("Loading Ad...")
            Clock.schedule_once(self.load_ad, 0.2)
        else:
            self.update_status("Desktop Mode")

    if platform == "android":
        @run_on_ui_thread
        def load_ad(self, dt):
            activity = cast("android.app.Activity", PythonActivity.mActivity)

            ad_request = AdRequestBuilder().build()
            test_unit_id = "ca-app-pub-3940256099942544/1033173712"

            # Simple load without PythonJavaClass
            self.interstitial_ad = InterstitialAd(activity)
            self.interstitial_ad.load(ad_request)

            self.update_status("Ad Requested (Test Mode)")
            
            # 1 sec baad show karne ki try
            Clock.schedule_once(self.show_ad, 1)

        @run_on_ui_thread
        def show_ad(self, dt):
            try:
                if self.interstitial_ad:
                    activity = cast("android.app.Activity", PythonActivity.mActivity)
                    self.interstitial_ad.show(activity)
                    self.update_status("Ad Showing")
                else:
                    self.update_status("Ad Not Ready")
            except Exception as e:
                self.update_status(str(e))


if __name__ == "__main__":
    MainApp().run()
