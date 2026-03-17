from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
import threading

# Android specific imports
if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    
    # Java Classes
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
    AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    InterstitialAd = autoclass('com.google.android.gms.ads.interstitial.InterstitialAd')
    InterstitialAdLoadCallback = autoclass('com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
else:
    # Desktop par error na aaye isliye dummy decorator
    def run_on_ui_thread(func):
        return func

# --- GLOBAL AD LOGIC ---
_interstitial_ad = None
TEST_ID = "ca-app-pub-3940256099942544/1033173712" # Google Test Interstitial ID

class MyAdLoadCallback(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/ads/interstitial/InterstitialAdLoadCallback']
    __javacontext__ = 'app'

    @java_method('(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V')
    def onAdLoaded(self, interstitialAd):
        global _interstitial_ad
        _interstitial_ad = interstitialAd
        Clock.schedule_once(lambda x: toast("Ad Loaded & Ready"))

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        global _interstitial_ad
        _interstitial_ad = None
        error_msg = str(loadAdError.toString())
        Clipboard.copy(error_msg)
        Clock.schedule_once(lambda x: toast("Ad Load Failed (Copied to Clipboard)"))

@run_on_ui_thread
def load_interstitial():
    try:
        activity = PythonActivity.mActivity
        # Initialize Mobile Ads (Sirf ek baar zaroori hai)
        MobileAds.initialize(activity)
        
        builder = AdRequestBuilder()
        request = builder.build()
        
        callback = MyAdLoadCallback()
        InterstitialAd.load(activity, TEST_ID, request, callback)
    except Exception as e:
        Clipboard.copy("Load Error: " + str(e))
        print(str(e))

@run_on_ui_thread
def show_interstitial():
    global _interstitial_ad
    try:
        if _interstitial_ad:
            _interstitial_ad.show(PythonActivity.mActivity)
            _interstitial_ad = None # Reset after showing
            load_interstitial()     # Load next one
        else:
            toast("Ad not loaded yet. Loading now...")
            load_interstitial()
    except Exception as e:
        Clipboard.copy("Show Error: " + str(e))
        print(str(e))

# --- KIVY UI ---
kv = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        
        MDLabel:
            text: "Interstitial Ad Test"
            halign: "center"
            pos_hint: {"center_y": .7}
            font_style: "H5"
            
        MDRaisedButton:
            text: "SHOW AD (Every 3rd Click)"
            pos_hint: {"center_x": .5, "center_y": .5}
            size_hint_x: .7
            on_release: app.handle_ad_click()
            
        MDLabel:
            id: counter_lbl
            text: "Clicks: 0"
            halign: "center"
            pos_hint: {"center_y": .4}
'''

class MainScreen(Screen):
    pass

class TestAdApp(MDApp):
    def build(self):
        try:
            self.click_count = 0
            return Builder.load_string(kv)
        except Exception as e:
            Clipboard.copy("Build Error: " + str(e))

    def on_start(self):
        # App start hote hi ad load karna shuru karein
        if platform == "android":
            load_interstitial()

    def handle_ad_click(self):
        try:
            self.click_count += 1
            self.root.get_screen('main').ids.counter_lbl.text = f"Clicks: {self.click_count}"
            
            if self.click_count % 3 == 0:
                if platform == "android":
                    show_interstitial()
                else:
                    toast("Ad only works on Android!")
        except Exception as e:
            Clipboard.copy("Click Logic Error: " + str(e))

if __name__ == '__main__':
    TestAdApp().run()
    
