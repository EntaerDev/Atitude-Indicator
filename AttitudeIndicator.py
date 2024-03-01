import pygame
pygame.init()
import geopandas as gpd
import geobr
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.backends.backend_agg as agg
import contextily
import math
from shapely.geometry import Polygon
from shapely.geometry import LineString
#constants
EARTHCOLOR = (190,90,60)
SKYCOLOR = (15,62,255)
HORIZONCOLOR = (255,255,255)
WHITE = (255,255,255)
KEYCOLOR =(0,0,0)
BLACK=(0,0,0)
VELBACKGROUND = (0,62,135,0)
VELCOLOR = (255,255,255)
GREEN = (0,128,0)
RED = (153,0,0)
GOLD = (255,255,0)
GOLD2 = (230,200,100)
COMPASSBACKGROUND = (120,80,90,250)
FPS=60 # Velocidad de reproduccion 
WIDTH=(700)
HEIGTH=(500)
MAXVEL = 400
MAXHEIGTH = 400
FONT = "consolas"

ventana = pygame.display.set_mode((WIDTH,HEIGTH))

clock = pygame.time.Clock()
skyimg = pygame.image.load("C:/Users/b2ml/Documents/Python/Garmin Simulator/Afinador/gpsangle.png")
pointerimg = pygame.image.load("C:/Users/b2ml/Documents/Python/Garmin Simulator/Afinador/pointer.png")
# # Set the size for the image
# DEFAULT_IMAGE_SIZE = (700, 240)
# gpsframe = pygame.transform.scale(skyimg, DEFAULT_IMAGE_SIZE)
gpsframerect = skyimg.get_rect()
pointerrect = pointerimg.get_rect()
#skyimg.center = (250,125)
earth= pygame.Surface((700,500))
earth.fill(EARTHCOLOR)
earth.set_colorkey(KEYCOLOR)
earthrect = earth.get_rect()
earthrect.center = (250,125)
sky= pygame.Surface((700,500))
sky.fill(SKYCOLOR)
sky.set_colorkey(KEYCOLOR)
skyrect = sky.get_rect()
skyrect.center = (250,0)
horizon= pygame.Surface((700,50))
horizon.fill(HORIZONCOLOR)
horizon.set_colorkey(KEYCOLOR)
horizonrect = horizon.get_rect()
horizonrect.center = (250,250)
mapwindow= pygame.Surface((200,200))
mapwindow.set_colorkey(KEYCOLOR)
mapwindowrect = mapwindow.get_rect()
mapwindowrect.center = (250,250)
mapcover= pygame.Surface((700,500))
mapcover.fill(EARTHCOLOR)
mapcover.set_colorkey(KEYCOLOR)
mapcoverearthrect = earth.get_rect()
mapcoverearthrect.center = (250,125)
pointerRectangle= pygame.Surface((15,5))
pointerRectangle.fill(HORIZONCOLOR)
pointerRectangle.set_colorkey(KEYCOLOR)
velscreen= pygame.Surface((WIDTH*0.1,HEIGTH*0.4), pygame.SRCALPHA)
navcreen= pygame.Surface((WIDTH,HEIGTH))
#FUNCIONES 
def draw_velpanel (surface, vel , size, x, y):
    VELBACKGROUND= (0,62,135,92)
    surface.fill(VELBACKGROUND)
    surfacerect = surface.get_rect()
    surfacerect.center = (x,y)
    
    pygame.draw.polygon(ventana,WHITE,[(x-35,y-100),(x-35,y+100),(x+35,y+100),(x+35,y-100)],1)
    pygame.draw.polygon(ventana,GREEN,[(x+25,y-100),(x+25,y+100),(x+30,y+100),(x+30,y-100)])
    if vel > MAXVEL and vel < 500:
        pygame.draw.polygon(ventana,RED,[(x+25,y-100),(x+25,y-100+((vel-MAXVEL))),(x+30,y-100+((vel-MAXVEL))),(x+30,y-100)])
    elif vel > 500:
        pygame.draw.polygon(ventana,RED,[(x+25,y-100),(x+25,y+100),(x+30,y+100),(x+30,y-100)])
    ventana.blit(surface,surfacerect)
    
def draw_vel (surface, vel, size, x, y):
    pygame.draw.polygon(ventana,BLACK,[(x-35,y-20),(x-35,y+20),(x+10,y+20),(x+10,y+35),(x+30,y+35),(x+30,y-35),(x+10,y-35),(x+10,y-20)])
    pygame.draw.polygon(ventana,WHITE,[(x-35,y-20),(x-35,y+20),(x+10,y+20),(x+10,y+35),(x+30,y+35),(x+30,y-35),(x+10,y-35),(x+10,y-20)],1)
    font = pygame.font.SysFont("arial", size-5 )
    v="0"
    v= str(vel+1)[-1]
    upvel_surface = font.render(v, True, VELCOLOR)
    upvel_rect = upvel_surface.get_rect()
    upvel_rect.midtop = (x+20,y-35)
    surface.blit(upvel_surface, upvel_rect)
    font = pygame.font.SysFont("arial", size+5)
    v="0"
    v= str(vel)[-1]
    centervel_surface = font.render(v, True, VELCOLOR)
    centervel_rect = centervel_surface.get_rect()
    centervel_rect.midtop = (x+20,y-18)
    surface.blit(centervel_surface, centervel_rect)
    font = pygame.font.SysFont("arial", size-5)
    v="0"
    v= str(vel-1)[-1]
    downvel_surface = font.render(v, True, VELCOLOR)
    downvel_rect = downvel_surface.get_rect()
    downvel_rect.midtop = (x+20,y+10)
    surface.blit(downvel_surface, downvel_rect)
    font = pygame.font.SysFont("arial", size)
    v="00"
    if vel >0:
        if vel < 10: 
            v = "00"
        elif vel > 10 and vel <100: 
            v = "0"+str(vel//10)
        elif vel > 100 and vel < 1000: 
            v = str(vel//10)
        elif vel >1000:
            v = str(vel//10)
    text_surface = font.render(v, True, VELCOLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y-15)
    surface.blit(text_surface, text_rect)
def draw_radiopanel (surface, size, x, y, n1, n2):
    pygame.draw.polygon(ventana,BLACK,[(0,y*0.1),(0,0),(x,0),(x,y*0.1)])
    pygame.draw.polygon(ventana,WHITE,[(0,y*0.1),(0,0),(x,0),(x,y*0.1)],1)
    pygame.draw.polygon(ventana,WHITE,[(x*0.3,y*0.1),(x*0.3,0),(x*0.7,0),(x*0.7,y*0.1)],1)
    pygame.draw.line(ventana,WHITE,(x*0.3,y*0.05),(x*0.7,y*0.05),2)
    pygame.draw.line(ventana,WHITE,(x*0.5,y*0.05),(x*0.5,y*0.1),2)
    pygame.draw.line(ventana,WHITE,(x*0.4,y*0.05),(x*0.4,y*0.1),2)
    pygame.draw.line(ventana,WHITE,(x*0.55,y*0),(x*0.55,y*0.05),2)
    font = pygame.font.SysFont(FONT, size )
    nav1="NAV1 "+str(n1)
    nav2="NAV1 "+str(n2) + " PAE"
    navtype = " ISLE"
    nav1_surface = font.render(nav1, True, WHITE)
    nav1_rect = nav1_surface.get_rect()
    nav1_rect.midtop = (x*0.09,y*0.01)
    ventana.blit(nav1_surface, nav1_rect)
    font = pygame.font.SysFont(FONT, size )
    navtype_surface = font.render(navtype, True, GREEN)
    navtype_rect = navtype_surface.get_rect()
    navtype_rect.midtop = (x*0.21,y*0.01)
    ventana.blit(navtype_surface, navtype_rect)
    font = pygame.font.SysFont(FONT, size)
    nav2_surface = font.render(nav2, True, WHITE)
    nav2_rect = nav2_surface.get_rect()
    nav2_rect.midtop = (x*0.12,y*0.05)
    ventana.blit(nav2_surface, nav2_rect)
def draw_heigthpanel (surface, heigth , size, x, y):
    VELBACKGROUND= (0,62,135,92)
    surface.fill(VELBACKGROUND)
    surfacerect = surface.get_rect()
    surfacerect.center = (x,y)
    
    pygame.draw.polygon(ventana,WHITE,[(x-35,y-100),(x-35,y+100),(x+35,y+100),(x+35,y-100)],1)
    pygame.draw.polygon(ventana,GREEN,[(x+25,y-100),(x+25,y+100),(x+30,y+100),(x+30,y-100)])
    if heigth > MAXHEIGTH and heigth < 500:
        pygame.draw.polygon(ventana,RED,[(x+25,y-100),(x+25,y-100+((heigth-MAXVEL))),(x+30,y-100+((heigth-MAXVEL))),(x+30,y-100)])
    elif vel > 500:
        pygame.draw.polygon(ventana,RED,[(x+25,y-100),(x+25,y+100),(x+30,y+100),(x+30,y-100)])
    ventana.blit(surface,surfacerect)
def draw_heigth (surface, heigth, size, x, y):
    pygame.draw.polygon(ventana,BLACK,[(x-35,y-20),(x-35,y+20),(x+10,y+20),(x+10,y+35),(x+30,y+35),(x+30,y-35),(x+10,y-35),(x+10,y-20)])
    pygame.draw.polygon(ventana,WHITE,[(x-35,y-20),(x-35,y+20),(x+10,y+20),(x+10,y+35),(x+30,y+35),(x+30,y-35),(x+10,y-35),(x+10,y-20)],1)
    font = pygame.font.SysFont("arial", size-5 )
    v="00"
    v= str(heigth+1)[-1]
    upvel_surface = font.render(v, True, VELCOLOR)
    upvel_rect = upvel_surface.get_rect()
    upvel_rect.midtop = (x+20,y-35)
    surface.blit(upvel_surface, upvel_rect)
    font = pygame.font.SysFont("arial", size+5)
    v="00"
    v= str(heigth)[-1]
    centervel_surface = font.render(v, True, VELCOLOR)
    centervel_rect = centervel_surface.get_rect()
    centervel_rect.midtop = (x+20,y-18)
    surface.blit(centervel_surface, centervel_rect)
    font = pygame.font.SysFont("arial", size-5)
    v="00"
    v= str(heigth-1)[-1]
    downvel_surface = font.render(v, True, VELCOLOR)
    downvel_rect = downvel_surface.get_rect()
    downvel_rect.midtop = (x+20,y+10)
    surface.blit(downvel_surface, downvel_rect)
    font = pygame.font.SysFont("arial", size)
    v="000"
    if heigth >0:
        if heigth < 10: 
            v = "000"
        elif heigth > 10 and vel <100: 
            v = "00"+str(vel//10)
        elif heigth > 100 and vel < 1000: 
            v = "0"+str(vel//10)
        elif heigth >1000:
            v ="0"+ str(vel//10)
    text_surface = font.render(v, True, VELCOLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x-10,y-15)
    surface.blit(text_surface, text_rect)
def draw_compass (surface, compass, size, x, y):
    pygame.draw.circle(ventana, COMPASSBACKGROUND, (x*.5,y*0.8), 75)
    pygame.draw.polygon(ventana,BLACK,[(x*0.46,y*0.65),(x*0.46,y*0.59),(x*0.54,y*0.59),(x*0.54,y*0.65)])
    pygame.draw.polygon(ventana,WHITE,[(x*0.46,y*0.65),(x*0.46,y*0.59),(x*0.54,y*0.59),(x*0.54,y*0.65)],1)
    VELBACKGROUND= (0,62,135,92)
    pygame.draw.circle(ventana, COMPASSBACKGROUND, (x*.5,y*0.8), 75)
    
    c= "00"+str(compass)[-1]
    if compass >360:
        compass = compass-360
    if compass >0:
        if compass < 10: 
            c = "00"+str(compass)
        elif compass > 10 and compass <100: 
            c = "0"+str(compass)
        elif compass > 100 and compass <= 360: 
            c = str(compass)
        
    font = pygame.font.SysFont("arial", size )
    compass_surface = font.render(c, True, WHITE)
    compass_rect = compass_surface.get_rect()
    compass_rect.midtop = (x*0.5,y*0.59)
    surface.blit(compass_surface, compass_rect)


    #pygame.draw.arc(surface,BLACK,(x*0.485,HEIGTH*0.6,y*0.6,y*0.6),-(rad-0),-(rad-6.28319))
    
    #pygame.draw.circle(ventana,BLACK,[(x,y)],10)
    #surface.blit(surface, surfacerect)
   
    
#muni = geobr.read_municipality(code_muni=3550308, year=2010)

#states = geobr.read_state(year=2020) # Todos os estados

states = geobr.read_state(code_state="SP",year=2020)
#states.boundary()
#units = geobr.read_conservation_units(date = 201909)
#urban = geobr.read_urban_area(year = 2015)
#schools = geobr.read_schools(year = 2020)
#s = geopandas.GeoSeries(
    # [
        #Polygon([(-47, -22), (-48, -22), (-48, -23), (-47, -23)]),
        #Polygon([(10, 0), (10, 5), (0, 0)]),
        #Polygon([(0, 0), (2, 2), (2, 0)]),
        #LineString([(0, 0), (1, 1), (0, 1)]),
        #Point(0, 1)
#     ]
# )

fig, ax = plt.subplots(figsize=(500, 500), dpi=100)
#@states.plot(facecolor="#32C964", edgecolor="#F71F07", ax=ax)
#s.plot(facecolor="#0000CD", edgecolor="#FF00FF", ax=ax)
#units.plot(facecolor="#2C9E9E", edgecolor="#9E6C2C", ax=ax)
#urban.plot(facecolor="#A66F6F", edgecolor="#C9BFB3", ax=ax)
#schools.plot(facecolor="#32C964", edgecolor="#F71F07", ax=ax)



# ax.set_title("States", fontsize=20)
# ax.axis("off")
# plt.show(block=False)
# plt.pause(30)
# plt.close()

MAPIMAGEWIDTH= WIDTH*0.15
MAPIMAGEHEIGTH = HEIGTH*0.15
#ventanamap = pygame.display.set_mode((MAPIMAGEWIDTH,MAPIMAGEHEIGTH))
#gpsframerect = map.get_rect()
#mapsframe = pygame.transform.scale(map, (MAPIMAGEWIDTH,MAPIMAGEHEITGH))


jugando = True
angle = 0
vel = 0
compass = 0
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
    angle = angle
    # Compruebo si se ha pulsado alguna tecla
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle -= 0.5
    if keys[pygame.K_PAGEUP]:
        vel += 1
    if keys[pygame.K_PAGEDOWN]:
        if vel > 0:
            vel -= 1
    if keys[pygame.K_l]:
        compass += 1
    if keys[pygame.K_r]:
        if compass > 0:
            compass -= 1
    if keys[pygame.K_RIGHT]:
        angle += 0.5
    if keys[pygame.K_ESCAPE]:
        jugando = False
    clock.tick(FPS)
    ventana.fill((252, 243, 207))
    # img2 = pygame.transform.rotate(sky, angle)
    # imgrect2 = img2.get_rect()
    # imgrect2.center = (250,0)    
    # ventana.blit(img2, imgrect2)
    # img4 = pygame.transform.rotate(skyimg, angle)
    # imgrect4 = img4.get_rect()
    # imgrect4.center = (250,200)    
    # ventana.blit(img4, imgrect4)    
    # img1 = pygame.transform.rotate(earth, angle)
    # imgrect1 = img1.get_rect()
    # imgrect1.center = (250,502)    
    # ventana.blit(img1, imgrect1)
    
    # img3 = pygame.transform.rotate(horizon, angle)
    # imgrect3 = img3.get_rect()
    # imgrect3.center = (250,248)    
    # ventana.blit(img3, imgrect3)
    # img5 = pygame.transform.rotate(pointerimg, angle)
    # imgrect5 = img5.get_rect()
    # imgrect5.center = (250,180)    
    # ventana.blit(img5, imgrect5)
    #mapa com Geopandas
    
    rad = math.radians(angle)
    sen = math.sin(rad)
    cos = math.cos(rad)
    angleunit = math.acos(cos)*180/math.pi
    angleunit= angle
    xv= WIDTH*math.sin(rad)
    yv= WIDTH*math.cos(rad)
    xh =0
    yh=0
    x= 0
    earthleft =(0, HEIGTH)
    earthrigth =(WIDTH, HEIGTH)
    skyleft = (0,0)
    skyuprigth = (0,0)
    skyupleft = (0,0)
    skyrigth =(WIDTH,HEIGTH )
    lineleft = (0, 0)
    linerigth =(WIDTH, 0)   
    if angleunit >=-45 and angleunit< 45:
        y= (HEIGTH/90)*(angle+45)
        earthleft =(0, HEIGTH)
        earthupleft = (WIDTH*0,HEIGTH-y)
        earthupref = earthupleft
        earthcenter =(WIDTH*0.5, HEIGTH*0.5)
        earthuprigth = (WIDTH*1, y) 
        earthrigth =(WIDTH, HEIGTH)
        lineleft = earthupleft
        linerigth =earthuprigth
    if angleunit >45 and angleunit<= 135:
        x= (WIDTH/90.0)*(angle-45)
        earthleft =(0,HEIGTH)
        earthupleft = (0,0)
        earthupref = (x,0)
        earthcenter =(WIDTH*0.5, HEIGTH*0.5)
        earthuprigth = (WIDTH-x, HEIGTH)
        earthrigth =(WIDTH -x, HEIGTH)
        lineleft = earthupref
        linerigth = earthrigth
    if angleunit >135 and angleunit<= 225:
        y= (HEIGTH/90.0)*(angle-135)
        earthleft =(0,HEIGTH- y)
        earthupleft = (WIDTH*0,0)
        earthupref = earthupleft
        earthcenter =(WIDTH-x,0 )
        earthuprigth = (WIDTH -x,y )
        earthrigth =(WIDTH*0.5, HEIGTH*0.5)
        lineleft = earthleft
        linerigth =earthuprigth
    if angleunit >225 and angleunit<= 315:
        x= (WIDTH/90.0)*(angle-225)
        earthleft =(x,0)
        earthupleft =(WIDTH,0) 
        earthupref = earthupleft
        earthcenter =(WIDTH , HEIGTH)
        earthuprigth = (WIDTH-x, HEIGTH)
        earthrigth =(WIDTH*0.5, HEIGTH*0.5)
        lineleft = earthleft
        linerigth =earthuprigth
    if angleunit >315 and angleunit<= 360:
        y= (HEIGTH/90)*(angle-315)
        earthleft =(0, HEIGTH)
        earthupleft = (WIDTH*0,HEIGTH- y)
        earthupref = earthupleft
        earthcenter =(WIDTH*0.5, HEIGTH*0.5)
        earthuprigth = (WIDTH*1, y) 
        earthrigth =(WIDTH, HEIGTH)
        lineleft = earthupleft
        linerigth = earthuprigth
    if angleunit >=-135 and angleunit<-45:
        x= (WIDTH/90.0)*(angle+135)
        earthleft =(x,0)
        earthupleft =(WIDTH,0) 
        earthupref = earthupleft
        earthcenter =(WIDTH , HEIGTH)
        earthuprigth = (WIDTH-x, HEIGTH)
        earthrigth =(WIDTH*0.5, HEIGTH*0.5)
        lineleft = earthleft
        linerigth =earthuprigth
    if angleunit >=-225 and angleunit< -135:
        y= (HEIGTH/90.0)*(angle+225)
        earthleft =(0,HEIGTH- y)
        earthupleft = (WIDTH*0,0)
        earthupref = earthupleft
        earthcenter =(WIDTH-x,0 )
        earthuprigth = (WIDTH -x,y )
        earthrigth =(WIDTH*0.5, HEIGTH*0.5)
        lineleft = earthleft
        linerigth =earthuprigth
    if angleunit >=-315 and angleunit< -225:
        x= (WIDTH/90.0)*(angle+315)
        earthleft =(0,HEIGTH)
        earthupleft = (0,0)
        earthupref = (x,0)
        earthcenter =(WIDTH*0.5, HEIGTH*0.5)
        earthuprigth = (WIDTH-x, HEIGTH)
        earthrigth =(WIDTH -x, HEIGTH)
        lineleft = earthupref
        linerigth = earthrigth
    if angleunit >=-360 and angleunit< -315:
        y= (HEIGTH/45)*(angle+360)
        earthleft =(0, HEIGTH)
        earthupleft = (WIDTH*0,HEIGTH- y)
        earthupref = earthupleft
        earthcenter =(WIDTH*0.5, HEIGTH*0.5)
        earthuprigth = (WIDTH*1, y) 
        earthrigth =(WIDTH, HEIGTH)
        lineleft = earthupleft
        linerigth =earthuprigth    # if angle>45:
    #    xv= WIDTH*math.cos(rad)
    #    yv= WIDTH*math.sin(rad)
    pygame.draw.rect(ventana,SKYCOLOR,[skyleft,skyrigth])
    pygame.draw.polygon(ventana,EARTHCOLOR,[earthleft,earthupleft,earthupref, earthcenter,earthuprigth,earthrigth])
    pygame.draw.line(ventana,HORIZONCOLOR,lineleft,linerigth,2)
    pygame.draw.polygon(ventana,HORIZONCOLOR,[(WIDTH//2-6,HEIGTH*0.27),(WIDTH//2,HEIGTH*0.23),(WIDTH//2+6,HEIGTH*0.27)])
    pygame.draw.arc(ventana,HORIZONCOLOR,(WIDTH//2-150,HEIGTH*0.22,300,300),-(rad-0.77),-(rad-0.77*3),1)
    pygame.draw.rect(ventana,GOLD,[(WIDTH*0.31,HEIGTH*0.5),(WIDTH*0.07,HEIGTH*0.01)])
    pygame.draw.rect(ventana,GOLD,[(WIDTH*0.63,HEIGTH*0.5),(WIDTH*0.07,HEIGTH*0.01)])
    pygame.draw.polygon(ventana,GOLD,[(WIDTH*0.43,HEIGTH*0.56),(WIDTH*0.5,HEIGTH*0.5),(WIDTH*0.58,HEIGTH*0.56), (WIDTH*0.5,HEIGTH*0.52)])
    pygame.draw.polygon(ventana,GOLD2,[(WIDTH*0.43,HEIGTH*0.56),(WIDTH*0.5,HEIGTH*0.52),(WIDTH*0.58,HEIGTH*0.56), (WIDTH*0.5,HEIGTH*0.54)])
    pointerRectangleimagerect = pointerRectangle.get_rect()
    pointerRectangleimagerect.center = (WIDTH//2,HEIGTH*0.28)    
    ventana.blit(pointerRectangle, pointerRectangleimagerect)
    # VELOCIDADES 
    draw_velpanel(velscreen, vel, 25, WIDTH//5,HEIGTH*0.5)
    draw_vel(ventana, vel, 25, WIDTH//5,HEIGTH*0.5)
    nav1 = 117.5
    nav2 =110.60
    draw_radiopanel(navcreen,18, WIDTH,HEIGTH,nav1, nav2 )
    #ALTITUD
    draw_heigthpanel(velscreen, vel, 25, WIDTH*0.83,HEIGTH*0.5)
    draw_heigth(ventana, vel, 25, WIDTH*0.83,HEIGTH*0.5)
    draw_compass(ventana, compass, 25, WIDTH,HEIGTH)

    
 
    #pygame.draw.rect(ventana,VELCOLOR,[(400,125),(402,126)])

    # fonte = pygame.font.SysFont("'Arial'", 15, True, True)
    # mensagem = "Pontuação: {vel}" 
    # vel= vel + 1
    # formatacao_texto = fonte.render(mensagem, False, (255, 255, 255))
    # ventana.blit(formatacao_texto, (200, 40))
    # FIN 

    # canvas = agg.FigureCanvasAgg(fig)
    # canvas.draw()
    # renderer = canvas.get_renderer()
    # raw_data = renderer.buffer_rgba()
    # size = canvas.get_width_height()
    # mapimg = pygame.image.frombuffer (raw_data, size, "RGBA")
    # mapimg = pygame.transform.scale(mapimg, (MAPIMAGEWIDTH,MAPIMAGEHEIGTH))
    #mapimg = pygame.transform.rotate(mapimg, angle)
    #mapimg = mapimg.get_rect()
    #mapimg.center = (30,400)
    # center = (20,380)    
    # ventana.blit(mapimg, center)
    #earthref=pygame.draw.rect(ventana,SKYCOLOR,[(350,300),(100,100)])
    

    
    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()