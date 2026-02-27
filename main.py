from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.uix.button import MDRaisedButton

if platform == "android":
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

KV = '''
MDScreen:
    MDRaisedButton:
        text: "Show Reward Ad"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_reward()
'''

class RewardApp(MDApp):

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            self.load_reward()

    @run_on_ui_thread
    def load_reward(self):
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
        RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')

        activity = autoclass('org.kivy.android.PythonActivity').mActivity

        # Test Reward Ad Unit ID
        self.ad = RewardedAd(activity, 
            "ca-app-pub-7264801834502563/8870022221")

        request = AdRequest().build()
        self.ad.loadAd(request)

        print("Reward Ad Loaded")

    @run_on_ui_thread
    def show_reward(self):
        if platform == "android" and self.ad.isLoaded():
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.ad.show(activity)
        else:
            print("Ad not loaded yet")

RewardApp().run()
