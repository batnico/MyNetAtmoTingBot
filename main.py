import tingbot
from tingbot import *
#import os,sys
import time


import lnetatmo

screen.fill(color='white')
screen.text('Bienvenue sur l\'application MyNetatmoTingBot',color='blue',align='bottom',font_size=15)
screen.image("Logo_netatmo_2020.png")

import lnetatmo

authorization = lnetatmo.ClientAuth()
devList = lnetatmo.WeatherStationData(authorization)

variation = { 'prec' : 0}

bouton = 1

@every(seconds=20)
def refresh_data():
    parcours(bouton)

def parcours(bouton):
    authorization = lnetatmo.ClientAuth()
    devList = lnetatmo.WeatherStationData(authorization)
    
    device = tingbot.app.settings['Module']["P"+str(bouton)][3]
    logo = tingbot.app.settings['Module']["P"+str(bouton)][2]
    titre = tingbot.app.settings['Module']["P"+str(bouton)][1]
    value = devList.lastData('MeteoNicho')[tingbot.app.settings['Module']["P"+str(bouton)][3]][tingbot.app.settings['Module']["P"+str(bouton)][4]]
    temp = str(devList.lastData('MeteoNicho')[tingbot.app.settings['Module']["P"+str(bouton)][3]][tingbot.app.settings['Module']["P"+str(bouton)][4]]) + " " + tingbot.app.settings['Module']["P"+str(bouton)][5]
    

        
    if tingbot.app.settings['Module']["P"+str(bouton)][4] == "Temperature":
        if value > 20:
            couleur = "red"
        else:
            couleur = "green"
        
    if tingbot.app.settings['Module']["P"+str(bouton)][4] == "Humidity":
        if value > 80:
            couleur = "red"
        elif value < 40:
            couleur = "green"
        else:
            couleur = "orange"
    
    screen.fill(color='white')
    
    # Partie concernant la variation de temperature par rapport a la precedente
    
    #screen.text(str(value) + str(variation['prec']), xy=(190,180), font_size=25, color='black')
    
    if value > variation['prec']:
        screen.text("Hausse !", xy=(220,180), font_size=25, color='black')
    elif value < variation['prec']:
        screen.text("Baisse !", xy=(220,180), font_size=25, color='black')
    else:
        screen.text("Stable", xy=(220,180), font_size=25, color='black')
    
    variation['prec'] = value
    
    screen.image(logo,xy=(140,180),max_width=60,max_height=100)
    screen.text(titre,xy=(160,20),color='black', font_size=25)
    screen.text(temp,xy=(155,100),color=couleur,font_size=80)
    
    temps = time.gmtime()
    #local_time = time.ctime(seconds)
    screen.update()
    
    screen.text("Update : " + str(temps.tm_mday) + "/" + str(temps.tm_mon) + " " + str(temps.tm_hour+2) + "h" + str(temps.tm_min) , color='blue',xy=(255,235),font_size=10)
    
    screen.text(' A propos de NetAtmoTingBot',xy=(70,235),font_size=10, color='red')
    screen.update()
    
@after(seconds=3)
def on_start():
    parcours(1)
    
@right_button.press
def on_press_right():
    global bouton
    if bouton < 5:
        bouton = bouton + 1
    else:
        bouton = 5 
    parcours(bouton)
    
@left_button.press
def on_press_left():
    global bouton
    if bouton >= 2:
        bouton = bouton - 1
    else:
        bouton = 1
    parcours(bouton)
    
def about():
    screen.fill(color='white')
    screen.image('Nicholas.jpg',xy=(60,50))
    screen.text('Created by Nicolas ETIENNE - 2020', xy=(160,200), color='black', font_size=15)


@touch(xy=(40,235), align="center", size=(60,60))
def on_touch(xy, action):
    if action == 'down':
        about()
        #screen.text('On sort !', xy=(20,20), font_size=10)
        #os.system("sudo shutdown -h now")

tingbot.run()
