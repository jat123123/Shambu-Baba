from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

if platform == "android":
    try:
        from jnius import autoclass, cast
        from android.runnable import run_on_ui_thread
    
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
        AdRequest = autoclass("com.google.android.gms.ads.AdRequest$Builder")
        InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")
    except Exception as e:
        print(f"Import Error: {e}")
        Clipboard.copy(f'platform :- {e}')

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDTopAppBar:
            title: "Simple Interstitial"

        MDRaisedButton:
            text: "LOAD "
            pos_hint: {"center_x": .5}
            on_release: app.load_and_show()
        MDRaisedButton:
            text: "SHOW AD"
            pos_hint: {"center_x": .8}
            on_release: app.show_ad_only()       

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
            try:
                activity = cast("android.app.Activity", PythonActivity.mActivity)
                MobileAds.initialize(activity)
            except Exception as e:
                self.update_status(f"Init Error: {e}")

    def update_status(self, text):
        self.root.ids.status_label.text = f"Status: {text}"

    def load_and_show(self):
        if platform == "android":
            self.update_status("Loading Ad (Wait 5s)...")
            # Step 1: Ad load karo
            self.load_ad_only()
            # Step 2: 5 second baad show karo
        else:
            self.update_status("Desktop: Not Supported")

    @run_on_ui_thread
    def load_ad_only(self, *args):
        try:
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            ad_req = AdRequest().build()
            test_id = "ca-app-pub-3940256099942544/1033173712"
            
            # Ad load request (Bina callback ke)
            # Note: Kuch versions mein 4th parameter 'None' dena padta hai
            InterstitialAd.load(activity, test_id, ad_req, None)
            
        except Exception as e:
            self.update_status(f"Load Error: {e}")
            Clipboard.copy(f'load_ad_only :- {e}')

    @run_on_ui_thread
    def show_ad_only(self,*args):
        try:
            # Yahan hum assume kar rahe hain ki ad load ho gaya hoga
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            
            # Show karne ki koshish (Directly call)
            # Agar self.interstitial_ad handle nahi ho raha toh 
            # ye tabhi kaam karega jab InterstitialAd static object ho
            self.update_status("Trying to Show...")
            
            # Warning: Bina callback ke object reference milna mushkil hota hai
            # Par aap ise test kar sakte hain
        except Exception as e:
            self.update_status(f"Show Error: {e}")
            Clipboard.copy(f'show_ad_only :- {e}')

if __name__ == "__main__":
    MainApp().run()
    
