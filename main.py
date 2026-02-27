from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.toast import toast
from kivy.core.clipboard import Clipboard

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread

KV = '''
MDScreen:
    MDRaisedButton:
        text: "Show Reward Ad"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_ad()
'''

if platform == "android":

    class RewardCallback(PythonJavaClass):
        __javainterfaces__ = [
            'com/google/android/gms/ads/OnUserEarnedRewardListener'
        ]
        __javacontext__ = 'app'

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
        def onUserEarnedReward(self, rewardItem):
            toast("Reward mil gaya 🎉")


class RewardApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ad = None   # 🔥 important (crash avoid)

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            self.init_ads()

    @run_on_ui_thread
    def init_ads(self):
        try:
            MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            MobileAds.initialize(activity)

            self.load_ad()

        except Exception as e:
            Clipboard.copy("INIT ERROR:\n" + str(e))

    @run_on_ui_thread
    def load_ad(self):
        try:
            RewardedAd = autoclass(
                'com.google.android.gms.ads.rewarded.RewardedAd'
            )
            AdRequest = autoclass(
                'com.google.android.gms.ads.AdRequest$Builder'
            )
            activity = autoclass(
                'org.kivy.android.PythonActivity'
            ).mActivity

            self.ad = RewardedAd(
                activity,
                "ca-app-pub-3940256099942544/5224354917"
            )

            self.ad.loadAd(AdRequest().build())

        except Exception as e:
            Clipboard.copy("LOAD ERROR:\n" + str(e))
            self.ad = None

    @run_on_ui_thread
    def show_ad(self):
        try:
            if platform != "android":
                Clipboard.copy("NOT ANDROID PLATFORM")
                return

            if not self.ad:
                Clipboard.copy("AD OBJECT NONE")
                return

            activity = autoclass(
                'org.kivy.android.PythonActivity'
            ).mActivity

            self.ad.show(activity, RewardCallback())

        except Exception as e:
            Clipboard.copy("SHOW ERROR:\n" + str(e))


RewardApp().run()
