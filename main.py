from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.toast.kivytoast.kivytoast import toast
import requests
import webbrowser
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image,AsyncImage,CoreImage
from kivymd.uix.textfield import MDTextField
from kivy.uix.videoplayer import VideoPlayer
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton, MDFillRoundFlatButton, MDFillRoundFlatIconButton, MDRoundFlatIconButton, MDRoundFlatButton, MDFloatingActionButton, MDIconButton
from kivy.metrics import dp,sp
import requests
import time
import mimetypes
import random
from android.permissions import request_permissions, Permission
from kivy.animation import Animation
from kivy.utils import platform
from android.storage import primary_external_storage_path
from kivy.core.clipboard import Clipboard
import os
import re
import datetime
import time
import sqlite3
from kivy.clock import Clock
import io
import base64
import webbrowser
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from jnius import JavaException
from kivy.animation import Animation
import threading

#kv file start
kv='''
Manager:
    Login:
    Fir:
    Sec:

<Login>:
    name:'login'

    #FloatLayout For Animation
    MDFloatLayout:
        id:fll1
        MDFloatLayout:
            id:fl1
            size_hint_y:0.58
            pos_hint:{'center_y':1.8}          
            canvas:
                Color:
                    rgba:1,0,0,1
                Rectangle:
                    size:self.size
                    pos:self.pos
        MDFloatLayout:
            id:fl2
            size_hint_y:0.3
            pos_hint:{'center_y':1.8}          
            canvas:
                Color:
                    rgba:1,0,0,1
                Ellipse:
                    size:self.size
                    pos:self.pos

        MDIconButton:
            id:i1
            icon:'account-circle'   
            pos_hint:{'center_x':0.5,'center_y':0.8}              
            theme_text_color:'Custom'   
            text_color:1,1,1,1
            
        MDLabel:
            id:l1
            text:'LOGIN PAGE'
            markup:True
            font_style:'H5'
            halign:'center'
            pos_hint:{'center_y':0.9}               
            opacity:0
            bold:True

    #__________________TextLayout______
        MDTextField:
            id:tf1
            pos_hint:{'center_x':0.5,'center_y':0.7}
            size_hint_x:0.7
            hint_text: "ENTER USERNAME"
            mode: "rectangle"
            line_color_normal: 0.2, 0.3, 0.4, 1
            hint_text_color_normal: 0.6, 0.6, 0.6, 1
            

        MDTextField:
            id:tf2
            password:True
            pos_hint:{'center_x':0.5,'center_y':0.6}
            size_hint_x:0.7          
            hint_text: "ENTER PASSWORD"
            mode: "rectangle"
            line_color_normal: 0.2, 0.3, 0.4, 1
            hint_text_color_normal: 0.6, 0.6, 0.6, 1
 #_BUTTTON_______
        MDIconButton:
            id:eyeb1
            icon: "eye"        
            pos_hint: {'center_x':0.8,"center_y":0.6}
            size_hint_x:0.1             
            on_release:app.eyep(root.ids.tf2,self)                      

#__________Buttons___________
        MDFillRoundFlatButton:
            id:b2
            text: "Log in"
            font_size: dp(16)
            pos_hint: {'center_x':0.5,"center_y":0.5}
            size_hint_x:0.5
            md_bg_color: 0, 0.4, 1, 1
            on_press:app.login_check()
            
        MDLabel:
            id:l2            
            text:'new_user'
            pos_hint:{'center_x':0.52,'center_y':0.4}        
            size_hint:0.5,0.02
            bold:True

        MDFlatButton:
            id:b3
            text: "Sign up?"
            pos_hint: {"center_x": .5,'center_y':0.4}
            theme_text_color: "Custom"
            text_color: 0,0,0,1
            font_name:'Roboto-Bold'
            on_release:app.sign_up()

#FIR SCREEN
<Fir>:
    name:'home'
    
#Bottom Navigation
    MDBottomNavigation:
        id:hbn1
        panel_color:1,1,1,1       
        MDBottomNavigationItem:
            name:'hbni1'
            icon:'home'
            text:'home'
            Image:
                source:'asstes/homebanner.png'
                allow_stretch:True
                keep_ratio:False
                size_hint:1,0.1
                pos_hint:{'center_x':0.5,'center_y':0.95}
    
            MDLabel:
                id:hl1
                text:''
                pos_hint:{'center_x':0.25,'center_y':0.86}        
                adaptive_width:True
                adaptive_height:True
                bold:True
                font_style:'H5'
                font_size:sp(30)
            MDBoxLayout:
                id:hbox1
                adaptive_height:True
                adaptive_width:True
                orientation:'horizontal'
                pos_hint:{'center_x':0.7,'center_y':0.86}
                
                MDIcon:
                    id:hicon1
                    icon:'star'
                    #opacity:0                     
                    adaptive_width:True
                    adaptive_height:True
                    theme_text_color:'Custom'   
                    text_color:0.5,0.5,0.5,1             
                    font_size:sp(30)    
                    canvas.before:
                        Color:
                            rgba:0,0,0,1
                        Line:
                            rectangle:self.x,self.y,self.width,self.height
                            width:1.2          
                MDLabel:
                    id:hl2
                    text:''
                    opacity:0                         
                    adaptive_width:True
                    adaptive_height:True
                    bold:True                
                    font_size:sp(30)    
                    canvas.before:
                        Color:
                            rgba:0,0,0,1
                        Line:
                            rectangle:self.x,self.y,self.width,self.height
                            width:1.2
                                               
            MDCard:
                id:hmdc1
                size_hint:1,0.3
                pos_hint:{'center_x':0.5,'center_y':0.65}
                elevation:10
                MDCarousel:
            		id:hmdca1
            		direction:'right'
            		loop:False
            		size_hint:1,1
            		pos_hint:{'center_x':0.5,'center_y':0.5}
          
        MDBottomNavigationItem:
            name:'hbni2'
            icon:'bank-transfer-out'
            text:'withdraw'                










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
            activity=PythonActivity.mActivity
            MobileAds.initialize(activity)
            ad_view = AdView(activity)
            ad_view.setAdSize(AdSize.BANNER)
            ad_view.setAdUnitId("ca-app-pub-3940256099942544/6300978111")
            builder = AdRequestBuilder()
            request = builder.build()
            ad_view.loadAd(request)
            params = LayoutParams(
                LayoutParams.MATCH_PARENT,
                LayoutParams.WRAP_CONTENT
            )
            params.gravity = Gravity.Top
            activity.addContentView(ad_view, params)
            
            
        except Exception as e:
            Clipboard.copy(str(e))


#Manager Class
class Manager(ScreenManager):
    pass


#Login Screen class                
class Login(Screen):
    pass

#Fir screen class        
class Fir(Screen):
    pass

#Sec screen class
class Sec(Screen):
    pass


#APP CLASS
class App(MDApp):
    def build(self):
        self.eye=False
        self.b=Builder.load_string(kv)
        self.id=''
        
        return self.b


#On Start Fun

    def on_start(self):
        try:
            threading.Thread(target=self.img_info,daemon=True).start()
            fl1=self.b.get_screen('login').ids.fl1
            fl2=self.b.get_screen('login').ids.fl2
            i1=self.b.get_screen('login').ids.i1
            l1=self.b.get_screen('login').ids.l1
            
            anim1=Animation(pos_hint={'center_y':1.18},duration=1)
            anim1.start(fl1)
            
            anim2=Animation(pos_hint={'center_y':0.9},duration=1)
            anim2.start(fl2)
            
            anim3=Animation(pos_hint={'center_y':0.9},icon_size=sp(60),duration=1)
            anim3.start(i1)
            
            anim4=Animation(pos_hint={'center_y':0.85},opacity=1,duration=1)
            anim4.start(l1)
        
        except Exception as e:
            toast('SOMETHING WENT WRONG')
            
# SIGN_UP POP UP            
    def sign_up(self,*args):
        try:
            if hasattr(self,"mc1") and self.mc1 and self.mc1.parent:
                pass
            
            else:
                self.mc1 = MDCard(
                    size_hint=(0.9,0.9),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}, 
                    md_bg_color=(1, 1, 1, 1),
                    elevation=10000000,
                    radius=[24],
                    orientation="vertical",
                    padding="12dp",
                    opacity=0,                
                )     
                self.b.get_screen('login').add_widget(self.mc1)                          
                float1=MDFloatLayout(size_hint=(1,1))        
                self.mc1.add_widget(float1) 
#IMAGE BANNER                
                img=Image(source='assets/signup.png',size_hint=(1,0.2),allow_stretch=True,keep_ratio=False,pos_hint={'center_x':0.5,'center_y':0.9})
                float1.add_widget(img)
#DISSMISS BUTTON                
                b1=MDIconButton(icon='close',pos_hint={'center_x':0.95,'center_y':0.99},theme_text_color='Custom',text_color=(1,0,0,1))      
                b1.bind(on_release=self.d_signup)   
                float1.add_widget(b1)      
#TEXT FIELD
                self.tff1=MDTextField(pos_hint={'center_x':0.5,'center_y':0.7},size_hint_x=0.7,mode='rectangle',hint_text='ENTER USERNAME')         
                float1.add_widget(self.tff1) 
#TEXT FIELD2  
                self.tff2=MDTextField(pos_hint={'center_x':0.5,'center_y':0.6},size_hint_x=0.7,mode='rectangle',hint_text='ENTER PASSWORD',password=True)         
                float1.add_widget(self.tff2)  
#MDButton2
                b2=MDFillRoundFlatButton(text='Sign_up',pos_hint={'center_x':0.5,'center_y':0.5},size_hint_x=0.5) 
                b2.bind(on_release=self.signup_check)
                float1.add_widget(b2)               
#MD Button3
                b3=MDFlatButton(text='Already have an account? ',pos_hint={'center_x':0.5,'center_y':0.4},size_hint_x=0.5,font_name='Roboto-Bold') 
                b3.bind(on_release=self.d_signup)
                float1.add_widget(b3)                                                
#Button 4
                b4=MDIconButton(icon='eye',pos_hint={'center_x':0.8,'center_y':0.6},size_hint_x=0.1)      
                b4.bind(on_release=lambda x,x1=self.tff2,x2=b4:self.eyep(x1,x2))   
                float1.add_widget(b4)                                           
#CALL ANIMATION                  
                self.anim()  
        
        
        except Exception as e:
            toast(str(e))

#SIGN_UP ANIMATION
    def anim(self,*a):
        try:
            anim=Animation(pos_hint={'center_x':0.5,'center_y':0.5},opacity=1,duration=0.5)
            anim.start(self.mc1)
            
            
            
            
            
        except Exception as e:
            pass

#______Dissmiss_sign_up
    def d_signup(self,*a):
        try:
            if hasattr(self,'mc1') and self.mc1 and self.mc1.parent:
                anim=Animation(opacity=0,duration=0.5)
                anim.bind(on_complete=lambda *args:self.b.get_screen('login').remove_widget(self.mc1))    
                anim.start(self.mc1)       
                
                
          
            
            
        except Exception as e:
            pass

#EYE PROTECTION 
    def eyep(self,our,our2):
        try:
            our.password = not our.password
            our2.icon='eye-off' if not our.password else 'eye'
 
          

        except Exception as e:
            pass

# sign_up check
    def signup_check(self,*a):
        try:           
            tf1=self.tff1.text
            tf2=self.tff2.text
            #Condition Making                        
            if tf1.strip()=='' or tf2.strip()=='':
                toast('PLEASE ENTER DETAIL FIRST')
            elif '.' in tf1 or '/' in tf1 or '\\' in tf1 or '[' in tf1 or '#' in tf1 or ']' in tf1 or '$' in tf1  or '.' in tf2 or '/' in tf2 or '\\' in tf2:
                toast('PLEASE DONT ENTER [.,[,[,/,$,#]]] IN FIELDS')
            else:
                threading.Thread(target=self.signup_thread,args=(tf1,tf2),daemon=True).start()
          
                 
                
                            
            
        except Exception as e:
            pass

#signup check by threading

    def signup_thread(self,t1,t2):
        try:               
            url='https://earning-app-96740-default-rtdb.firebaseio.com/.json'
            api='1BBR2jWgSrHZfIqNi7lJKifpcjaQcL9oGwaBzVT7'
            full_url=f'{url}?auth={api}'
            response1=requests.get(full_url).json()
            if response1 != None:               
                if t1  in response1:                    
                    Clock.schedule_once(lambda x :toast('Already signed up')) 
                else:
                    f_url=f'https://earning-app-96740-default-rtdb.firebaseio.com/{t1}.json?auth={api}'                   
                    jsn={'password':t2,'coin':'0','time':str(f'{time.strftime("%d-%m-%y")}')}
                    requests.patch(url=f_url,json=jsn)
                    Clock.schedule_once(lambda x :toast('Sign_up Sucessfully')) 
                    self.d_signup()
                    
            
            else:                           
                f_url=f'https://earning-app-96740-default-rtdb.firebaseio.com/bhavi.json?auth={api}'
                jsn={'password':'123','coin':'0','time':f'{time.strftime("%d-%m-%y")}'}
                requests.patch(url=f_url,json=jsn)
                Clock.schedule_once(lambda x :toast('Filling')) 
                
          
                 
                
                            
            
        except Exception as e:
            Clock.schedule_once(lambda x:toast(str(re)))         
        
#Login checker
    def login_check(self,*a):
        try:
            t1=self.b.get_screen('login').ids.tf1.text
            t2=self.b.get_screen('login').ids.tf2.text
            if t1.strip()=='' or t2.strip()=='':
                toast('ENTER DETAIL FIRST')
            else:
                threading.Thread(target=self.login_thread,args=(t1,t2),daemon=True).start()

                                  
           
        except Exception as e:
            toast(str(e))
        
#Login check Threading

    def login_thread(self,t1,t2):
        try:
            url='https://earning-app-96740-default-rtdb.firebaseio.com/.json'
            api='1BBR2jWgSrHZfIqNi7lJKifpcjaQcL9oGwaBzVT7'
            full_url=f'{url}?auth={api}'
            data=requests.get(full_url).json()
            if data != None:
                if t1 in data:
                    if t2 == data[t1]['password']:                   
                        Clock.schedule_once(lambda x:self.go_home(t1))
                        
                    else:
                        Clock.schedule_once(lambda x:toast('Sorry wrong password'))
                        
                else:
                    Clock.schedule_once(lambda x:toast(str('WRONG USERNAME SIGN UP FIRST')))
            else:
                pass
                               
            
            
        except Exception as e:
            Clock.schedule_once(lambda x:toast(str(re)))
            Clipboard.copy(str(e))
            
#go home
    def go_home(self,t1,*a):
        show_banner()
        self.b.current='home'
        self.b.transition.direction='left'
        self.id=t1
        self.b.get_screen('login').ids.tf1.text=''
        self.b.get_screen('login').ids.tf2.text=''
        self.b.get_screen('home').ids.hl1.text=f'Hello,\n{self.id}'
        threading.Thread(target=self.coin_adder,daemon=True).start()
      
#coin adder

    def coin_adder(self,*a):
        try:
            url=f'https://earning-app-96740-default-rtdb.firebaseio.com/{self.id}.json'
            api='1BBR2jWgSrHZfIqNi7lJKifpcjaQcL9oGwaBzVT7'
            full_url=f'{url}?auth={api}'
            data=requests.get(full_url).json()
            self.b.get_screen('home').ids.hl2.text=data['coin']
            anim=Animation(opacity=1,duration=1).start(self.b.get_screen('home').ids.hl2)
            
                                            
        except Exception as e:
            Clock.schedule_once(lambda x: toast(str(re)))
                
#img_info from db
    def img_info(self,*a):
        try:
            url='https://imgupdater-default-rtdb.firebaseio.com/img.json'
            api='kumGyE0MqendNrWPqHp27Q7RFqeFdVG1LiKkqVRb'
            full_url=f'{url}?auth={api}'
            data=requests.get(full_url).json()
            a=[]         
            if data!=None:                
                for k,v in data.items():                    
                    de=base64.b64decode(v.get('img'))
                    buf=io.BytesIO(de)
                    a.append(buf)
                    
                Clock.schedule_once(lambda x: self.add_img(a))                                     
            else:
               Clock.schedule_once(lambda x: toast('sorry'))                 
                                                     
        except Exception as e:
            pass
#img_add
    def add_img(self,a):
        try:       
            for i in a:
                c=CoreImage(i,ext='png').texture
                img=Image(texture=c,allow_stretch=True,keep_ratio=False) 
                self.b.get_screen('home').ids.hmdca1.add_widget(img)                                           
                                             
                             
        except Exception as e:
            toast(str(e))
            
App().run()

