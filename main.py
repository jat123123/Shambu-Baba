from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
import threading

# Android imports
if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    RewardedAdLoadCallback = autoclass('com.google.android.gms.ads.rewarded.RewardedAdLoadCallback')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
else:
    def run_on_ui_thread(func): return func

# --- GLOBAL REWARDED LOGIC ---
_rewarded_ad = None
# Google Test Rewarded Ad ID
TEST_REWARDED_ID = "ca-app-pub-3940256099942544/5224354917"

# Callback for Loading
class MyRewardedLoadCallback(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/rewarded/RewardedAdLoadCallback']
    __javacontext__ = 'app'

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
    def onAdLoaded(self, rewardedAd):
        global _rewarded_ad
        _rewarded_ad = rewardedAd
        Clock.schedule_once(lambda x: toast("Video Ad Loaded! Click again to watch."))

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        global _rewarded_ad
        _rewarded_ad = None
        err = loadAdError.toString()
        Clipboard.copy(err)
        Clock.schedule_once(lambda x: toast("Load Failed: Error copied to clipboard"))

# Callback for Earning Reward (Interface)
class MyRewardListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/OnUserEarnedRewardListener']
    __javacontext__ = 'app'

    @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
    def onUserEarnedReward(self, rewardItem):
        # Yahan user ko coins dein
        amount = rewardItem.getAmount()
        Clock.schedule_once(lambda x: MDApp.get_running_app().add_coins(amount))

@run_on_ui_thread
def load_rewarded_video():
    try:
        activity = PythonActivity.mActivity
        MobileAds.initialize(activity)
        
        builder = AdRequestBuilder()
        request = builder.build()
        
        load_callback = MyRewardedLoadCallback()
        RewardedAd.load(activity, TEST_REWARDED_ID, request, load_callback)
    except Exception as e:
        Clipboard.copy("Load Exception: " + str(e))

@run_on_ui_thread
def show_rewarded_video():
    global _rewarded_ad
    try:
        if _rewarded_ad:
            activity = PythonActivity.mActivity
            reward_listener = MyRewardListener()
            _rewarded_ad.show(activity, reward_listener)
            _rewarded_ad = None
            load_rewarded_video() # Reload for next time
        else:
            toast("Ad not ready, loading now...")
            load_rewarded_video()
    except Exception as e:
        Clipboard.copy("Show Exception: " + str(e))

# --- KIVY UI ---
kv = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        
        MDLabel:
            text: "REWARDED VIDEO AD TEST"
            halign: "center"
            font_style: "H5"
            bold: True

        MDCard:
            size_hint: (1, 0.3)
            elevation: 4
            radius: [20,]
            padding: dp(15)
            MDRelativeLayout:
                MDLabel:
                    id: coin_lbl
                    text: "Your Coins: 0"
                    font_style: "H6"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    halign: "center"
                
                MDFillRoundFlatButton:
                    text: "Watch Video (+10 Coins)"
                    pos_hint: {"center_x": .5, "center_y": .2}
                    on_release: app.play_video()
'''

class MainApp(MDApp):
    def build(self):
        self.coins = 0
        return Builder.load_string(kv)

    def on_start(self):
        if platform == "android":
            load_rewarded_video()

    def play_video(self):
        if platform == "android":
            show_rewarded_video()
        else:
            self.add_coins(10) # For testing on PC
            toast("On PC: Added fake coins")

    def add_coins(self, amount):
        try:
            self.coins += amount
            self.root.ids.coin_lbl.text = f"Your Coins: {self.coins}"
            toast(f"Congratulations! You earned {amount} coins")
        except Exception as e:
            Clipboard.copy("Coin Logic Error: " + str(e))

if __name__ == '__main__':
    MainApp().run()
    
