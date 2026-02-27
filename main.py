from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.toast import toast

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

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            self.init_ads()

    @run_on_ui_thread
    def init_ads(self):
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        MobileAds.initialize(activity)

        self.load_ad()

    @run_on_ui_thread
    def load_ad(self):
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

    @run_on_ui_thread
    def show_ad(self):
        if self.ad:
            activity = autoclass(
                'org.kivy.android.PythonActivity'
            ).mActivity

            self.ad.show(activity, RewardCallback())
        else:
            toast("Ad not ready")

RewardApp().run()
