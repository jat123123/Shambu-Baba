from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivmob import KivMob, TestIds

class AdMobApp(MDApp):
    def build(self):
        # Test ID use karein development ke waqt
        self.ads = KivMob(TestIds.APP_ID)
        self.ads.load_rewarded_ad(TestIds.REWARDED_ID)
        
        screen = MDScreen()
        btn = MDRaisedButton(
            text="Show Reward Ad",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.show_ad
        )
        screen.add_widget(btn)
        return screen

    def show_ad(self, *args):
        # Ad show karne se pehle check karein ki load hua ya nahi
        if self.ads.is_rewarded_ad_loaded():
            self.ads.show_rewarded_ad()
        else:
            print("Ad abhi load nahi hua hai...")
            self.ads.load_rewarded_ad(TestIds.REWARDED_ID)

if __name__ == "__main__":
    AdMobApp().run()
    
