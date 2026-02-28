from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivy.clock import Clock

# --- Android Specific Pyjnius Logic ---
if platform == 'android':
    from jnius import autoclass, cast, PythonJavaClass, java_method
    
    # Java Classes
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    InterstitialAd = autoclass('com.google.android.gms.ads.interstitial.InterstitialAd')
    
    # Ye hai "Genius" part: Java Callback ko Python mein handle karna
    class AdLoadCallback(PythonJavaClass):
        __javainterfaces__ = ['com/google/android/gms/ads/interstitial/InterstitialAdLoadCallback']
        __javacontext__ = 'app'

        def __init__(self, app_instance):
            super().__init__()
            self.app_instance = app_instance

        @java_method('(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V')
        def onAdLoaded(self, interstitialAd):
            print("Ad Loaded Successfully!")
            self.app_instance.update_status("Ad Loaded! Showing now...")
            # Ad load hote hi show kar do
            current_activity = cast('android.app.Activity', PythonActivity.mActivity)
            interstitialAd.show(current_activity)

        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onAdFailedToLoad(self, loadAdError):
            print("Ad Failed to Load")
            self.app_instance.update_status("Ad Failed to Load.")

KV = '''
MDScreenManager:
    FirstScreen:

<FirstScreen>:
    name: "first"
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"
        
        MDTopAppBar:
            title: "PyJNIus Full Ad Fix"

        MDFloatLayout:
            MDRaisedButton:
                text: "LOAD & SHOW INTERSTITIAL"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: app.start_ad_process()

            MDLabel:
                id: status_label
                text: "Status: Ready"
                halign: "center"
                pos_hint: {"center_y": .3}
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def update_status(self, text):
        self.root.get_screen('first').ids.status_label.text = f"Status: {text}"

    def start_ad_process(self):
        if platform == 'android':
            self.update_status("Initializing & Requesting Ad...")
            Clock.schedule_once(self.load_ad, 0.5)
        else:
            self.update_status("Desktop: Ads not supported")

    def load_ad(self, dt):
        try:
            activity = cast('android.app.Activity', PythonActivity.mActivity)
            
            # 1. Initialize SDK
            MobileAds.initialize(activity)
            
            # 2. Setup Ad Request
            ad_request = AdRequest().build()
            unit_id = "ca-app-pub-3940256099942544/1033173712" # Test ID
            
            # 3. Callback Instance
            callback = AdLoadCallback(self)
            
            # 4. Load Call (Ye Java method hai jo callback mangta hai)
            InterstitialAd.load(activity, unit_id, ad_request, callback)
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

if __name__ == "__main__":
    MainApp().run()
    
