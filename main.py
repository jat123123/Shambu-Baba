from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread

KV = '''
MDScreen:
    md_bg_color: 0.1, 0.1, 0.1, 1

    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "20dp"
        pos_hint: {"center_y": .5}

        MDLabel:
            id: coin_label
            text: "Coins: 0"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 1,1,1,1

        MDRaisedButton:
            text: "Watch Ad & Earn Coins"
            pos_hint: {"center_x": .5}
            on_release: app.show_rewarded()

        MDRaisedButton:
            text: "Load Ad"
            pos_hint: {"center_x": .5}
            on_release: app.load_rewarded()
'''

if platform == "android":
    try:
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
        RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
        RewardedAdLoadCallback = autoclass(
            'com.google.android.gms.ads.rewarded.RewardedAdLoadCallback'
        )
        OnUserEarnedRewardListener = autoclass(
            'com.google.android.gms.ads.OnUserEarnedRewardListener'
        )
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except Exception as e:
        pass


    class RewardLoadCallback(PythonJavaClass):
        try:
            __javaclass__ = 'com/google/android/gms/ads/rewarded/RewardedAdLoadCallback'
    
            def __init__(self, app):
                super().__init__()
                self.app = app
    
            @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
            def onAdLoaded(self, rewardedAd):
                self.app.rewarded_ad = rewardedAd
                print("Ad Loaded")
                Clock.schedule_once(lambda dt: toast("Ad Loaded"))
    
            @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
            def onAdFailedToLoad(self, error):
                print("Failed:", error.toString())
                Clock.schedule_once(lambda dt: toast("Ad Failed"))
        except Exception as e:
            Clipboard.copy(f'adload :- {e}') 


    class RewardListener(PythonJavaClass):
        try:
            __javaclass__ = 'com/google/android/gms/ads/OnUserEarnedRewardListener'
    
            def __init__(self, app):
                super().__init__()
                self.app = app
    
            @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
            def onUserEarnedReward(self, rewardItem):
                amount = rewardItem.getAmount()
                Clock.schedule_once(lambda dt: self.app.give_reward(amount))
        except Exception as e:
            Clipboard.copy(f'listner :- {e}')                


class RewardApp(MDApp):

    def build(self):
        self.coins = 0
        self.rewarded_ad = None
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            try:
                MobileAds.initialize(PythonActivity.mActivity)
                self.load_rewarded()
            except Exception as e:
                Clipboard.copy(f'on_start:- {e}')

    def load_rewarded(self):
        if platform == "android":
            try:          
                ad_request = AdRequest.Builder().build()
        
                # Google test rewarded ad ID (safe)
                test_ad_id = "ca-app-pub-3940256099942544/5224354917"
        
                RewardedAd.load(
                    PythonActivity.mActivity,
                    test_ad_id,
                    ad_request,
                    RewardLoadCallback(self)
            )
            except Exception as e:
                Clipboard.copy(f'calling :- {e}')         

    @run_on_ui_thread
    def show_rewarded(self):
        if platform != "android":
            return

        if self.rewarded_ad:
            self.rewarded_ad.show(
                PythonActivity.mActivity,
                RewardListener(self)
            )
            self.rewarded_ad = None
            self.load_rewarded()  # preload next ad
        else:
            toast("Ad not ready")

    def give_reward(self, amount):
        self.coins += amount
        self.root.ids.coin_label.text = f"Coins: {self.coins}"
        toast(f"You earned {amount} coins!")


RewardApp().run()
