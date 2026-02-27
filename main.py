from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.clipboard import Clipboard

# Toast ke liye direct KivyMD toast use kar rahe hain
from kivymd.toast import toast as t

KV = '''
MDScreen:
    md_bg_color: 1, 1, 1, 1

    MDLabel:
        text: "Simple KivyMD AdMob App"
        halign: "center"
        pos_hint: {"center_y": 0.6}
        theme_text_color: "Primary"

    MDLabel:
        text: "Banner Ad will show at bottom"
        halign: "center"
        pos_hint: {"center_y": 0.5}
'''

if platform == "android":
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    try:

    # Zaroori Classes ko load karna (Path check karein)
        AdView = autoclass('com.google.android.gms.ads.AdView')
        AdSize = autoclass('com.google.android.gms.ads.AdSize')
        AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
        AdRequestBuilder = autoclass('com.google.android.gms.ads.AdRequest$Builder')
        MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Gravity = autoclass('android.view.Gravity')
        LayoutParams = autoclass('android.widget.FrameLayout$LayoutParams')
        
    except Exception as e:
        Clipboard.copy(str(e))        

    @run_on_ui_thread
    def show_banner():
        try:
            activity = PythonActivity.mActivity
            
            # Mobile Ads Initialize
            MobileAds.initialize(activity)
            
            # AdView Object banana
            ad_view = AdView(activity)
            ad_view.setAdSize(AdSize.BANNER)
            
            # ✅ Test Banner ID (Aapka ID bhi replace kar sakte hain)
            ad_view.setAdUnitId("ca-app-pub-3940256099942544/6300978111")
            
            # Ad Request Build karna
            builder = AdRequestBuilder()
            request = builder.build()
            
            # Ad Load karna
            ad_view.loadAd(request)
            
            # Layout set karna (Ad ko screen ke bottom mein rakhne ke liye)
            params = LayoutParams(
                LayoutParams.MATCH_PARENT,
                LayoutParams.WRAP_CONTENT
            )
            params.gravity = Gravity.BOTTOM
            
            # Activity mein ad add karna
            activity.addContentView(ad_view, params)
            
        except Exception as e:
            print(f"AdMob Error: {str(e)}")
            Clipboard.copy(str(e))

class AdApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        if platform == "android":
            show_banner()

if __name__ == "__main__":
    AdApp().run()
    
