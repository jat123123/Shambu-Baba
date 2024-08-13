from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder
from kivymd.toast.kivytoast.kivytoast import toast
import requests
import webbrowser
kv='''
Manager:
    Fir:
    Sec:

<Fir>:
    name:'home'
    id:screen1
    MDTextField:
        id:t1
        hint_text:'ENTER CITY'
        size_hint_x:1
        pos_hint:{'center_x':0.5,'center_y':0.8}
        text_color_normal: 0,0,0,1
      
        
    MDFloatingActionButton:
        id:fb1
        icon:'magnify'       
        pos_hint:{'center_x':0.5,'center_y':0.7}
        size_hint_x:1
        on_press:
            app.wh()
    
    
    

    
    MDLabel:
        id:l1
        text:'WHEATHER STATUS'
        pos_hint:{'center_x':0.3,'center_y':0.6}
        size_hint_x:0.5
        bold:True
        
                                           
    MDLabel:
        id:l2
        text:'TEMPERATURE'
        pos_hint:{'center_x':0.3,'center_y':0.5}
        size_hint_x:0.5   
        bold:True
        
    MDLabel:
        id:l3
        text:'PRESSURE'
        pos_hint:{'center_x':0.3,'center_y':0.4}
        size_hint_x:0.5   
        bold:True                               
                    
    MDLabel:
        id:l4
        text:'WIND SPEED'
        pos_hint:{'center_x':0.3,'center_y':0.3}
        size_hint_x:0.5   
        bold:True                               
    MDLabel:
        id:l5
        text:'DESCRIPTION'
        pos_hint:{'center_x':0.3,'center_y':0.2}
        size_hint_x:0.5   
        bold:True    
        
    MDLabel:
        id:al1
        text:'---------------'
        pos_hint:{'center_x':0.8,'center_y':0.6}
        size_hint_x:0.5   
        bold:True                                    
                                      
    MDLabel:
        id:al2
        text:'---------------'
        pos_hint:{'center_x':0.8,'center_y':0.5}
        size_hint_x:0.5   
        bold:True            

    MDLabel:
        id:al3
        text:'---------------'
        pos_hint:{'center_x':0.8,'center_y':0.4}
        size_hint_x:0.5   
        bold:True          

  

    MDLabel:
        id:al4
        text:'---------------'
        pos_hint:{'center_x':0.8,'center_y':0.3}
        size_hint_x:0.5   
        bold:True          

    MDLabel:
        id:al5
        text:'---------------'
        pos_hint:{'center_x':0.8,'center_y':0.2}
        size_hint_x:0.5   
        bold:True   
        
    MDTopAppBar:
        id:mt1
        title:'WHEATHER CHECKER'
        pos_hint:{'top':1}
        left_action_items:[['menu',lambda x:n1.set_state('open')]]                       
                      
                                    

    MDNavigationDrawer:
        id:n1
        MDList:
            pos_hint:{'top':1}
            OneLineIconListItem:
                text:'YOUTUBE'
                md_bg_color:'black'
                on_press:
                    app.yc()
                    
                IconLeftWidget:
                    icon:'youtube'
                    md_bg_color:'red'
                    on_press:
                        app.yv()
                   
 

               
                      
                             
                                           

'''


class Fir(Screen):
    pass
    
    
class Sec(Screen):
    pass
    
    
class Manager(ScreenManager):
    pass


class Demo(MDApp):
    def build(self):
        self.u=Builder.load_string(kv)
        return self.u

    def wh(self):
        city=self.u.get_screen('home').ids.t1.text
    
        self.r=requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d122001753e3d91ae8aeb85e48687d80').json()                    
        self.code=self.r['cod']
          
        try:              
            sta=self.r['weather'][0]['main'].upper()
            temp=str(int(self.r['main']['temp_max']-273.15)).upper()
            
            pre=str(self.r['main']['pressure'])
            
            ws=str(int(self.r['wind']['speed']*18/5))
            des=self.r['weather'][0]['description'].upper()
            
            self.u.get_screen('home').ids.al1.text=sta
            
            self.u.get_screen('home').ids.al2.text=f'{temp}°C'
            
            self.u.get_screen('home').ids.al3.text=pre
            
            self.u.get_screen('home').ids.al4.text=f'{ws}km/h'
            
            self.u.get_screen('home').ids.al5.text=des
            
          
                                              
              
        except:
            if self.code=='404':
                toast('CITY NOT FOUND')
                self.u.get_screen('home').ids.al1.text='---------------'
                self.u.get_screen('home').ids.al2.text='---------------'
                self.u.get_screen('home').ids.al3.text='---------------'
                self.u.get_screen('home').ids.al4.text='---------------'
                self.u.get_screen('home').ids.al5.text='---------------'
                
                
            else:
                toast('ERROR HAPPENED')    
                self.u.get_screen('home').ids.al1.text='---------------'
                self.u.get_screen('home').ids.al2.text='---------------'
                self.u.get_screen('home').ids.al3.text='---------------'
                self.u.get_screen('home').ids.al4.text='---------------'
                self.u.get_screen('home').ids.al5.text='---------------'
                 

    def yv(self):
        webbrowser.open('https://youtube.com/shorts/kKQv_wpl4vM?si=82XHYveNVQ4HFMmO')               
                
    def yc(self):
        webbrowser.open('https://youtube.com/@ffgaming-su2eu?si=qofaL1xbplXI2Yx-')                                                       
                                
                                        
                                                        
        

Demo().run()