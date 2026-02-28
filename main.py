from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.logger import Logger

# --- Step 1: Android Java Bridge (Python mein hi) ---
if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method, cast
    from android.runnable import run_on_ui_thread

    # Android AdMob Classes
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    
    # Ye class handle karegi ki ad load hua ya nahi
    class RewardedAdLoadCallback(PythonJavaClass):
        __javainterfaces__ = ['com.google.android.gms.ads.rewarded.RewardedAdLoadCallback']
        __javacontext__ = 'app'

        def __init__(self, app_instance):
            super().__init__()
            self.app = app_instance

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
        def onAdLoaded(self, rewardedAd):
            Logger.info("KivMob: Ad Loaded Successfully!")
            self.app.mRewardedAd = rewardedAd
            self.app.root.ids.status.text = "Ad Loaded! Press Show."

        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onAdFailedToLoad(self, loadAdError):
            Logger.info("KivMob: Ad Failed to Load")
            self.app.mRewardedAd = None
            self.app.root.ids.status.text = "Failed to Load Ad."

    # Ye class handle karegi reward milne ko
    class OnUserEarnedRewardListener(PythonJavaClass):
        __javainterfaces__ = ['com.google.android.gms.ads.OnUserEarnedRewardListener']
        __javacontext__ = 'app'

        def __init__(self, app_instance):
            super().__init__()
            self.app = app_instance

        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
        def onUserEarnedReward(self, rewardItem):
            amount = rewardItem.getAmount()
            type = rewardItem.getType()
            self.app.give_reward(amount, type)

else:
    # PC par error na aaye isliye dummy function
    def run_on_ui_thread(x):
        return x

# --- Step 2: UI Design ---
KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "20dp"
        padding: "20dp"

        MDLabel:
            text: "KivMob Python-Only Ad"
            halign: "center"
            font_style: "H4"
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: status
            text: "Status: Ready"
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            text: "1. LOAD REWARDED AD"
            pos_hint: {"center_x": .5}
            on_release: app.load_rewarded_ad()

        MDFillRoundFlatButton:
            text: "2. SHOW AD & GET COINS"
            pos_hint: {"center_x": .5}
            on_release: app.show_rewarded_ad()
'''

# --- Step 3: Main Logic ---
class MainApp(MDApp):
    mRewardedAd = None # Ad object yahan save hoga

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        if platform == "android":
            self.activity = PythonActivity.mActivity
            MobileAds.initialize(self.activity)
        return Builder.load_string(KV)

    @run_on_ui_thread
    def load_rewarded_ad(self):
        if platform != "android":
            self.root.ids.status.text = "PC: Simulating Load..."
            return

        self.root.ids.status.text = "Loading..."
        ad_unit_id = "ca-app-pub-3940256099942544/5224354917" # Test ID
        ad_request = AdRequestBuilder().build()
        
        # Callback instance
        load_callback = RewardedAdLoadCallback(self)
        
        RewardedAd.load(
            self.activity, 
            ad_unit_id, 
            ad_request, 
            load_callback
        )

    @run_on_ui_thread
    def show_rewarded_ad(self):
        if platform == "android":
            if self.mRewardedAd:
                reward_listener = OnUserEarnedRewardListener(self)
                self.mRewardedAd.show(self.activity, reward_listener)
            else:
                self.root.ids.status.text = "Ad not loaded yet!"
        else:
            # PC testing logic
            self.give_reward(10, "Test-Coins")

    def give_reward(self, amount, type):
        self.root.ids.status.text = f"SUCCESS! You got {amount} {type}"
        self.root.ids.status.theme_text_color = "Primary"

if __name__ == "__main__":
    MainApp().run()
    
