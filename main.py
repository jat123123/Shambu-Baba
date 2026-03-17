from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder').new().build()
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    # Yahan hum Abstract Class ko direct load karenge
    RewardedAdLoadCallback = autoclass('com.google.android.gms.ads.rewarded.RewardedAdLoadCallback')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')

# --- REWARD LISTENER (Yeh Interface hai, ye work karega) ---
class MyRewardListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/OnUserEarnedRewardListener']
    __javacontext__ = 'app'

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
    def onUserEarnedReward(self, rewardItem):
        amount = rewardItem.getAmount()
        Clock.schedule_once(lambda x: MDApp.get_running_app().add_coins(amount))

# --- LOAD CALLBACK (FIXED: Not using PythonJavaClass for Abstract Class) ---
# Hum iska ek "Proxy" banate hain ya direct implement karne ki koshish karte hain
class MyLoadCallback(PythonJavaClass):
    __javainterfaces__ = [] # Khali rakhein kyunki ye interface nahi hai
    __javacontext__ = 'app'

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
    def onAdLoaded(self, rewardedAd):
        MDApp.get_running_app().rewarded_ad = rewardedAd
        Clock.schedule_once(lambda x: toast("Video Ready!"))

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        err = loadAdError.getMessage()
        Clipboard.copy(err)
        Clock.schedule_once(lambda x: toast(f"Error: {err}"))

class MainApp(MDApp):
    rewarded_ad = None

    def build(self):
        return Builder.load_string('''
MDScreen:
    MDFillRoundFlatButton:
        text: "WATCH VIDEO FOR COINS"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.show_ad()
''')

    @run_on_ui_thread
    def load_ad(self):
        try:
            activity = PythonActivity.mActivity
            MobileAds.initialize(activity)
            
            # Test Rewarded ID
            unit_id = "ca-app-pub-3940256099942544/5224354917"
            builder = autoclass('com.google.android.gms.ads.AdRequest$Builder')()
            request = builder.build()
            
            callback = MyLoadCallback()
            RewardedAd.load(activity, unit_id, request, callback)
        except Exception as e:
            Clipboard.copy(str(e))

    @run_on_ui_thread
    def show_ad(self):
        if self.rewarded_ad:
            self.rewarded_ad.show(PythonActivity.mActivity, MyRewardListener())
            self.rewarded_ad = None
            self.load_ad()
        else:
            toast("Loading ad... please wait")
            self.load_ad()

    def add_coins(self, amount):
        toast(f"Earned {amount} coins!")

    def on_start(self):
        if platform == "android":
            self.load_ad()

MainApp().run()
