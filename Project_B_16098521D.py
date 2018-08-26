
# COMP1001 - Project B - 16098521d - CHENG Yiran
__author__="CHENG Yiran"
__version__="1.0"

import threading
from graphics import *
import time
from math import cos,sin,pi,modf
import calendar
import winsound
import datetime

# Init the points
# =======================================================
screencentre=Point(320,240)
centrex=screencentre.getX()
centrey=screencentre.getY()
screen2centre=Point(160,120)
centre2x=screen2centre.getX()
centre2y=screen2centre.getY()

win=GraphWin("Clock",centrex*2,centrey*2)
win2=GraphWin("Calendar",centre2x*2,centre2y*2)
win2.close()
win3=win3=GraphWin("Alarm Reminder",320,240)
win3.close()

# Current time
# [Y2016, M11, D18, Hr17, Min47, Sec44, Fri4, No323, Decimal_Sec0.97]
ct=[2000,1,1,0,0,0,1,1,0]

# Init the color themes
# =======================================================
bluedict=dict()
bluedict["M"]="DeepSkyBlue" # The mid-deep color
bluedict["XS"]="Azure"
bluedict["S"]="LightSkyBlue"
bluedict["L"]="DodgerBlue"
bluedict["XL"]="RoyalBlue"
bluedict["BG"]="Snow" # The background color

violetdict=dict()
violetdict["M"]="Plum"
violetdict["XS"]="LavenderBlush"
violetdict["S"]="Thistle"
violetdict["L"]="MediumOrchid"
violetdict["XL"]="DarkViolet"
violetdict["BG"]="MistyRose"

yellowdict=dict()
yellowdict["M"]="Gold"
yellowdict["XS"]="LemonChiffon"
yellowdict["S"]="Khaki"
yellowdict["L"]="Goldenrod"
yellowdict["XL"]="DarkGoldenrod"
yellowdict["BG"]="Ivory"

graydict=dict()
graydict["M"]="DarkGray"
graydict["XS"]="Gainsboro"
graydict["S"]="Silver"
graydict["L"]="Gray"
graydict["XL"]="DimGray"
graydict["BG"]="WhiteSmoke"

colors=[bluedict,violetdict,yellowdict,graydict] # colors[nowc]["M"]
nowc=0


# Init the timezone
# =======================================================
zones=[]
zones.append(("Hong Kong",0))
zones.append(("London",-8))
zones.append(("Astana",-2))
zones.append(("Jakarta",-1))
zones.append(("Bei Jing",0))
zones.append(("Soul",1))
zones.append(("Tokyo",1))
zones.append(("Sydney",2))
zones.append(("Honolulu",-18))
zones.append(("San Francisco",-16))
zones.append(("New York",-13))
timezone=0
# zones[timezone][0]='HK',zones[timezone][1]=0


# Init the buttons' position
# =======================================================
# (The x1,y1 must be over and left of x2,y2)
skinbtx1=40
skinbty1=360
skinbtx2=120
skinbty2=390
skinfont=14

quitbtx1=520
quitbty1=360
quitbtx2=600
quitbty2=390
quitfont=14

timrbtx1=480
timrbty1=400
timrbtx2=600
timrbty2=430
timrfont=14

zonebtx1=480
zonebty1=20
zonebtx2=600
zonebty2=50
zonefont=12

calendx1=40
calendy1=20
calendx2=140
calendy2=120

alarmx1=40
alarmy1=400
alarmx2=160
alarmy2=430
alarfont=14


# Init the elements' size
# =======================================================
secsize=22
clocksize=180

# Init the variables for calendar
# =======================================================
#cale=0
calfont0=32
calfont1=13
calfont2=12
months=["Error","Jan.","Feb.","Mar.","Apr.","May.","June","July","Aug.","Sep.","Ouc.","Nov.","Dec."]
days=["Error","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
nowy=ct[0]
nowm=ct[1]

# Init the current minutes and hours
# =======================================================
curh=0
curm=0
lasttext=""
timefont=24
timefont2=14
lastfont=timefont
t2=Text(Point((zonebtx1+zonebtx2)/2,(zonebty1+zonebty2)/2+50),lasttext)
t2.draw(win)

# Init the alarm time
# =======================================================
alarmh=88
alarmm=88
alarmstatus=False
e1=-1
e2=-1
e3=-1
timeryear=2016
timermonth=1
timerday=1
timerhour=0
timerminute=0
timersecond=0
timer=0


def getpoint(a=0,r=clocksize,centrepoint=screencentre):# x=0~360
    """Given angle and radius to get the point on the circle."""
    cx=centrepoint.getX()
    cy=centrepoint.getY()
    alpha=(a-90)/180*pi
    x=cx+r*cos(alpha)
    y=cy+r*sin(alpha)
    return Point(x,y)


def getdelttime(year1,month1,day1,hour1,minute1,second1=0,ms1=0):
    """Calculate the delta of given time and current time."""
    d0=datetime.datetime.now()
    d1=datetime.datetime(year1,month1,day1,hour1,minute1,second1,ms1)
    s=(d0-d1).seconds
    h=s//3600
    s=s%3600
    m=s//60
    s=s%60
    return (h,m,s)


def digitcell(x=10,y=10,width=10,length=40,ver_hor='v',color="Red"): # x,y is the centre of the circle
    """Draw a capsule shape for further use.
    Arguments: x,y-the center of the first circle; width; length; ver_hor-set the direction of the shape; color"""
    o1=Point(x,y)
    if(ver_hor=='v'):
        p1=Point(x-width/2,y)
        p2=Point(x+width/2,y+length)
        o2=Point(x,y+length)
    else:
        o2=Point(x+length,y)
        p1=Point(x,y-width/2)
        p2=Point(x+length,y+width/2)
    cir1=Circle(o1,width/2)
    cir1.setFill(color)
    cir1.setOutline(color)
    cir1.draw(win)
    cir2=Circle(o2,width/2)
    cir2.setFill(color)
    cir2.setOutline(color)
    cir2.draw(win)
    rec1=Rectangle(p1,p2)
    rec1.setFill(color)
    rec1.setOutline(color)
    rec1.draw(win)
    return True


def rrectangle(x1,y1,x2,y2,r,col=colors[nowc]["S"]):
    """Draw a round-angle rectangle."""
    digitcell(x1+r,y1+r,r*2,x2-x1-r*2,"h",col)
    digitcell(x1+r,y2-r,r*2,x2-x1-r*2,"h",col)
    rec1=Rectangle(Point(x1,y1+r),Point(x2,y2-r))
    rec1.setFill(col)
    rec1.setOutline(col)
    rec1.draw(win)
    return


def drawhand(a=0,length=clocksize*0.8,width=4,color='M',centrepoint=screencentre):
    """Draw the clock's hand with given arguments."""
    p1=getpoint(a-90,width/2)
    p2=getpoint(a+90,width/2)
    dx=p1.getX()-centrepoint.getX()
    dy=p1.getY()-centrepoint.getY()
    o1=getpoint(a,length)
    p3=Point(o1.getX()+dx,o1.getY()+dy)
    p4=Point(o1.getX()-dx,o1.getY()-dy)
    pol1=Polygon(p1,p2,p4,p3)
    pol1.setFill(colors[nowc][color])
    pol1.setOutline(colors[nowc][color])

    r1=width*0.7
    cir1=Circle(o1,r1)
    cir1.setFill(colors[nowc][color])
    cir1.setOutline(colors[nowc][color])

    tp=getpoint(a,length+r1*0.5)
    p5=Point(tp.getX()+dx*(r1/width*2)*0.866,tp.getY()+dy*(r1/width*2)*0.866)
    p6=Point(tp.getX()-dx*(r1/width*2)*0.866,tp.getY()-dy*(r1/width*2)*0.866)
    tri1=Polygon(p5,p6,getpoint(a,length+r1*(0.5+1.732)))
    tri1.setFill(colors[nowc][color])
    tri1.setOutline(colors[nowc][color])

    cir2=Circle(centrepoint,clocksize/16)
    cir2.setFill(colors[nowc][color])
    cir2.setOutline(colors[nowc][color])
    
    pol1.draw(win)
    cir1.draw(win)
    tri1.draw(win)
    cir2.draw(win)
    return


def checktimrbutton(p1):
    """Check the timer button and call timer."""
    global timer
    global timeryear,timermonth,timerday,timerhour,timerminute,timersecond
    ct2=list(time.localtime(time.time()))
    if timer==0:
        timrtext=Text(Point((timrbtx1+timrbtx2)/2,(timrbty1+timrbty2)/2),"Timer Start")
    if timer==1:
        timrtext=Text(Point((timrbtx1+timrbtx2)/2,(timrbty1+timrbty2)/2),"Timer Stop")
    if timer==2:
        timrtext=Text(Point((timrbtx1+timrbtx2)/2,(timrbty1+timrbty2)/2),"Timer Reset")
        
    if p1.getX()==0 and p1.getY()==0:
        timrtext.setStyle("bold")
        timrtext.setSize(timrfont)
        timrtext.setTextColor(colors[nowc]["BG"])
        timrtext.draw(win)
        return
    
    if p1.getX()>timrbtx1 and p1.getX()<timrbtx2 and p1.getY()>timrbty1 and p1.getY()<timrbty2:
        timrtext.setStyle("bold")
        timrtext.setSize(timrfont)
        timrtext.setTextColor(colors[nowc]["S"])
        timrtext.draw(win)
        
        timer=timer+1
        timer=timer%3
        
        if timer==0:
            timrtext=Text(Point((timrbtx1+timrbtx2)/2,(timrbty1+timrbty2)/2),"Timer Start")
        if timer==1:
            timrtext=Text(Point((timrbtx1+timrbtx2)/2,(timrbty1+timrbty2)/2),"Timer Stop")
            timeryear=ct2[0]
            timermonth=ct2[1]
            timerday=ct2[2]
            timerhour=ct2[3]
            timerminute=ct2[4]
            timersecond=ct2[5]
        if timer==2:
            timrtext=Text(Point((timrbtx1+timrbtx2)/2,(timrbty1+timrbty2)/2),"Timer Reset")
            timeryear=2016
            timermonth=1
            timerday=1
            timerhour=0
            timerminute=0
            timersecond=0
        timrtext.setStyle("bold")
        timrtext.setSize(timrfont)
        timrtext.setTextColor(colors[nowc]["BG"])
        timrtext.draw(win)
        
        updigi()
    return
    

def checkquitbutton(p1):
    """Check the quit button.
    To init the quit button, call checkskinbutton(Point(0,0))."""
    global quitfont
    # set the text of the button
    if p1.getX()==0 and p1.getY()==0:
        quittext=Text(Point((quitbtx1+quitbtx2)/2,(quitbty1+quitbty2)/2),"Quit")
        quittext.setStyle("bold")
        quittext.setSize(quitfont)
        quittext.setTextColor(colors[nowc]["BG"])
        quittext.draw(win)
    
    if p1.getX()>quitbtx1 and p1.getX()<quitbtx2 and p1.getY()>quitbty1 and p1.getY()<quitbty2:
        win.close()
        print("Quit")
        return True
    return False


def checkskinbutton(p1):
    """Check the skin button and change the colour.
    To init the skin button, call checkskinbutton(Point(0,0))."""
    global nowc
    global skinfont
    # set the text of the button
    skintext=Text(Point((skinbtx1+skinbtx2)/2,(skinbty1+skinbty2)/2),"Sky")
    if nowc==0:
        skintext.setText("Sky")
    if nowc==1:
        skintext.setText("Violet")
    if nowc==2:
        skintext.setText("Sunshine")
        skinfont=12
    if nowc==3:
        skintext.setText("Silver")        
    skintext.setStyle("bold")
    skintext.setSize(skinfont)
    skintext.setTextColor(colors[nowc]["BG"])
    if p1.getX()==0 and p1.getY()==0:
        skintext.draw(win)
    
    if p1.getX()>skinbtx1 and p1.getX()<skinbtx2 and p1.getY()>skinbty1 and p1.getY()<skinbty2:
        nowc=nowc+1
        nowc=nowc%len(colors)
        skintext.undraw()
        skinfont=14
        if nowc==0:
            skintext.setText("Sky")
        if nowc==1:
            skintext.setText("Violet")
        if nowc==2:
            skintext.setText("Sunshine")
            skinfont=12
        if nowc==3:
            skintext.setText("Silver")
        skintext.setTextColor(colors[nowc]["BG"])
        skintext.setSize(skinfont)
        skintext.draw(win)
        print("Change Theme!")
        return True
    return False


def checkzonebutton(p1):
    """check the zone button and init the digital time.
    To init the zone button, call checkzonebutton(Point(0,0))."""
    global timezone
    global zonefont
    # set the text of the button
    zonetext=Text(Point((zonebtx1+zonebtx2)/2,(zonebty1+zonebty2)/2),zones[timezone][0])
    zonetext.setSize(zonefont)

    if p1.getX()==0 and p1.getY()==0:
        zonetext.setTextColor(colors[nowc]["BG"])
        zonetext.setStyle("bold")
        zonetext.draw(win)
        
    
    if p1.getX()>zonebtx1 and p1.getX()<zonebtx2 and p1.getY()>zonebty1 and p1.getY()<zonebty2:
        zonetext=Text(Point((zonebtx1+zonebtx2)/2,(zonebty1+zonebty2)/2),zones[timezone][0])
        zonetext.setTextColor(colors[nowc]["S"])
        zonetext.setSize(zonefont)
        zonetext.setStyle("bold")
        zonetext.draw(win)
        
        timezone=timezone+1
        timezone=timezone%len(zones)

        zonetext=Text(Point((zonebtx1+zonebtx2)/2,(zonebty1+zonebty2)/2),zones[timezone][0])
        zonetext.setTextColor(colors[nowc]["BG"])
        zonetext.setSize(zonefont)
        zonetext.setStyle("bold")
        zonetext.draw(win)
        print("Change Timezone:",zones[timezone][0],zones[timezone][1]+8)
        return True
    return False


def ring():
    """The alarm rings."""
    print("Ring!")
    while not win3.closed:
        winsound.Beep(523,300)
        winsound.Beep(659,300)
        winsound.Beep(784,300)
        winsound.Beep(1046,600)
        winsound.Beep(1046,300)
        winsound.Beep(659,300)
        winsound.Beep(523,300)
        winsound.Beep(392,600)


def checkalarm():
    """Check the time for alarm rings."""
    global win3
    if alarmm==ct[4] and alarmh==ct[3]:
        win3=GraphWin("Alarm Reminder",320,240)
        t1=Text(Point(160,120),"TIME's up. :)")
        win3.setBackground(colors[nowc]["BG"])
        t1.setSize(28)
        t1.setStyle("bold")
        t1.setTextColor(colors[nowc]["L"])
        t1.draw(win3)
        ringthread=threading.Thread(target=ring)
        ringthread.start()


def checkalarbutton(p1):
    """Check the alarm button for setting time."""
    global alarmstatus
    global e1
    global e2
    global e3
    global alarmh
    global alarmm
    if p1.getX()==0 and p1.getY()==0: # Init
        tmp_wid=alarmy2-alarmy1
        tmp_x=alarmx1+tmp_wid/2
        tmp_y=alarmy1+tmp_wid/2
        tmp_len=alarmx2-alarmx1-tmp_wid
        digitcell(tmp_x,tmp_y,tmp_wid,tmp_len,'h',colors[nowc]["S"])
        
        alartext=Text(Point((alarmx1+alarmx2)/2,(alarmy1+alarmy2)/2),"Alarm")
        alartext.setTextColor(colors[nowc]["BG"])
        alartext.setSize(alarfont)
        alartext.setStyle("bold")
        alartext.draw(win)
    
    if p1.getX()>alarmx1 and p1.getX()<alarmx2 and p1.getY()>alarmy1 and p1.getY()<alarmy2:
        tmp_wid=alarmy2-alarmy1
        tmp_x=alarmx1+tmp_wid/2
        tmp_y=alarmy1+tmp_wid/2
        tmp_len=alarmx2-alarmx1-tmp_wid
        digitcell(tmp_x,tmp_y,tmp_wid,tmp_len,'h',colors[nowc]["S"])

        if alarmstatus:
            flag=True
            alarmstatus=False
            t1=e1.getText()
            t2=e2.getText()
            try:
                alarmh=int(t1)
            except ValueError:
                flag=False
            try:
                alarmm=int(t2)
            except ValueError:
                flag=False
            if flag==False:
                alarmh=88
                alarmm=88
            e1.undraw()
            e2.undraw()
            e3.undraw()
            alartext=Text(Point((alarmx1+alarmx2)/2,(alarmy1+alarmy2)/2),"Alarm")
            alartext.setTextColor(colors[nowc]["BG"])
            alartext.setSize(alarfont)
            alartext.setStyle("bold")
            alartext.draw(win)
        else:
            alarmstatus=True
            e1=Entry(Point((alarmx1+alarmx2)/2-25,(alarmy1+alarmy2)/2),3)
            e1.setFill(colors[nowc]["S"])
            e1.setTextColor(colors[nowc]["L"])
            e1.setStyle("bold")
            e1.setText("0"*(2-len(str(alarmh)))+str(alarmh))

            e2=Entry(Point((alarmx1+alarmx2)/2+25,(alarmy1+alarmy2)/2),3)
            e2.setFill(colors[nowc]["S"])
            e2.setTextColor(colors[nowc]["L"])
            e2.setStyle("bold")
            e2.setText("0"*(2-len(str(alarmm)))+str(alarmm))

            e3=Entry(Point((alarmx1+alarmx2)/2,(alarmy1+alarmy2)/2),1)
            e3.setFill(colors[nowc]["S"])
            e3.setTextColor(colors[nowc]["L"])
            e3.setStyle("bold")
            e3.setText(":")

            e2.draw(win)
            e3.draw(win)
            e1.draw(win)
            
    return True


def drawinterface():
    """Draw the interface of the clock."""
    win.setBackground(colors[nowc]["BG"])
    bgrec=Rectangle(Point(0,0),Point(640,480))
    bgrec.setFill(colors[nowc]["BG"])
    bgrec.setOutline(colors[nowc]["BG"])
    bgrec.draw(win)

    # Draw clock
    clock_o1=screencentre
    r1=clocksize+15
    clock_o2=screencentre
    r2=clocksize-15
    clock_o3=screencentre
    r3=25
    
    clock_cir1=Circle(clock_o1,r1)
    clock_cir1.setFill(colors[nowc]["M"])
    clock_cir1.setOutline(colors[nowc]["M"])
    clock_cir2=Circle(clock_o2,r2)
    clock_cir2.setFill(colors[nowc]["XS"])
    clock_cir2.setOutline(colors[nowc]["XS"])
    clock_cir3=Circle(clock_o3,r3)
    clock_cir3.setFill(colors[nowc]["M"])
    clock_cir3.setOutline(colors[nowc]["M"])
    clock_cir1.draw(win)
    clock_cir2.draw(win)
    
    for i in range(0,360,6):
        if i%90==0:
            cir4=Circle(getpoint(i),8)
        elif i%30==0:
            cir4=Circle(getpoint(i),4)
        else:
            cir4=Circle(getpoint(i),2)
        cir4.setFill(colors[nowc]["S"])
        cir4.setOutline(colors[nowc]["S"])
        cir4.draw(win)

    # Draw and initialize buttons
    tmp_wid=skinbty2-skinbty1
    tmp_x=skinbtx1+tmp_wid/2
    tmp_y=skinbty1+tmp_wid/2
    tmp_len=skinbtx2-skinbtx1-tmp_wid
    digitcell(tmp_x,tmp_y,tmp_wid,tmp_len,'h',colors[nowc]["S"])
    checkskinbutton(Point(0,0))

    tmp_wid=zonebty2-zonebty1
    tmp_x=zonebtx1+tmp_wid/2
    tmp_y=zonebty1+tmp_wid/2
    tmp_len=zonebtx2-zonebtx1-tmp_wid
    digitcell(tmp_x,tmp_y,tmp_wid,tmp_len,'h',colors[nowc]["S"])
    checkzonebutton(Point(0,0))

    tmp_wid=quitbty2-quitbty1
    tmp_x=quitbtx1+tmp_wid/2
    tmp_y=quitbty1+tmp_wid/2
    tmp_len=quitbtx2-quitbtx1-tmp_wid
    digitcell(tmp_x,tmp_y,tmp_wid,tmp_len,'h',colors[nowc]["S"])
    checkquitbutton(Point(0,0))

    upcalendar(Point(0,0))

    checkalarbutton(Point(0,0))
    
    tmp_wid=timefont+20
    tmp_x=zonebtx1+tmp_wid/2
    tmp_y=(zonebty1+zonebty2)/2+50
    tmp_len=zonebtx2-zonebtx1-tmp_wid
    digitcell(tmp_x,tmp_y,tmp_wid,tmp_len,'h',colors[nowc]["S"])
    updigi(True)

    tmp_wid=timrbty2-timrbty1
    tmp_x=timrbtx1+tmp_wid/2
    tmp_y=timrbty1+tmp_wid/2
    tmp_len=timrbtx2-timrbtx1-tmp_wid
    digitcell(tmp_x,tmp_y,tmp_wid,tmp_len,'h',colors[nowc]["S"])
    checktimrbutton(Point(0,0))
    


def getmonth(y,m):
    """Get the calender of a month and correct its format."""
    s=calendar.month(y,m)
    l=s.split("\n")
    s1=""
    for i in range(len(l)-2):
        s1=s1+l[i]+"\n"
    s1=s1+l[len(l)-2]+" "*(20-len(l[len(l)-2]))+"\n"
    return s1


def checkcalendar(p2):
    """Check the click on the calendar and change the month of the calendar."""
    global nowm
    global nowy
    rec1=Rectangle(Point(0,0),Point(centre2x*2,centre2y*2))
    rec1.setFill(colors[nowc]["XS"])
    rec1.setOutline(colors[nowc]["XS"])
    rec1.draw(win2)
    if p2.getX()==0:
        nowm=nowm
    elif p2.getX()>centre2x:
        nowm=nowm+1
        if nowm>12:
            nowm=1
            nowy=nowy+1
    elif p2.getX()<centre2x:
        nowm=nowm-1
        if nowm<1:
            nowm=12
            nowy=nowy-1
    t2=Text(Point(160,120),getmonth(nowy,nowm))
    t2.setSize(calfont2)
    t2.setFace('courier')
    t2.setTextColor(colors[nowc]["L"])
    t2.draw(win2)
    return True


def upcalendar(p1):
    """Draw the date display"""
    global win2
    global nowm
    global nowy
    if p1.getX()==0 and p1.getY()==0:
        rrectangle(calendx1,calendy1,calendx2,calendy2,15,colors[nowc]["S"])

        t1=Text(Point((calendx1+calendx2)/2,calendy1+calfont1),months[ct[1]]) # Month
        t1.setTextColor(colors[nowc]["BG"])
        t1.setSize(calfont1)
        t1.setStyle("bold")
        t1.draw(win)

        t2=Text(Point((calendx1+calendx2)/2,calendy2-calfont1),days[ct[6]]) # Day
        t2.setTextColor(colors[nowc]["BG"])
        t2.setSize(calfont1)
        t2.setStyle("bold")
        t2.draw(win)

        t3=Text(Point((calendx1+calendx2)/2,(calendy1+calendy2)/2),ct[2])
        t3.setTextColor(colors[nowc]["L"])
        t3.setSize(calfont0)
        t3.setStyle("bold")
        t3.draw(win)
    
    if p1.getX()>calendx1 and p1.getX()<calendx2 and p1.getY()>calendy1 and p1.getY()<calendy2:
        monthc=getmonth(ct[0],ct[1])
        t4=Text(Point(160,120),monthc)
        t4.setSize(calfont2)
        t4.setFace('courier')
        t4.setTextColor(colors[nowc]["L"])
        win2.close()
        win2=GraphWin("Calendar",320,240)
        win2.setBackground(colors[nowc]["XS"])
        nowm=ct[1]
        nowy=ct[0]
        t4.draw(win2)
    return
    

def uphm():
    """Refresh the hour and minute."""
    global curm
    global curh

    drawhand(curh,clocksize*0.5,12,'XS')
    drawhand(curm*6,clocksize*0.7,8,'XS')

    drawhand(ct[4]*6,clocksize*0.7,8,'XL')
    curm=ct[4]

    drawhand(30*ct[3]+0.5*ct[4],clocksize*0.5,12,'L')
    curh=30*ct[3]+0.5*ct[4]
    # curh has different meaning with curm!
    return


def updigi(init=False): # timer:1 begin,2 stop
    """Refresh the digital time."""
    global lasttext
    global lastfont
    global timer
    global t2
    if timer==2:
        return
    if timer:
        delta=getdelttime(timeryear,timermonth,timerday,timerhour,timerminute,timersecond)
        curtext="0"*(1-delta[0]//10)+str(delta[0])+":"+"0"*(1-delta[1]//10)+str(delta[1])+":"+"0"*(1-delta[2]//10)+str(delta[2])
    else:
        curtext="0"*(1-ct[3]//10)+str(ct[3])+":"+"0"*(1-ct[4]//10)+str(ct[4])
    if curtext!=lasttext or timer or init:
        t2.setText(curtext)
        t2.setStyle("bold")
        if timer:
            t2.setSize(timefont2)
            lastfont=timefont2
        else:
            t2.setSize(timefont)
            lastfont=timefont
        t2.setTextColor(colors[nowc]["L"])
        t2.undraw()
        t2.draw(win)
        lasttext=curtext
    return


def upsec():
    """Draw the second hand and call updigi() to refresh the digital time."""
    global lasttext
    o1=getpoint((ct[5])*6)
    o1=getpoint((ct[5]+ct[8])*6)
    c1=Circle(o1,secsize/2)
    c1.setFill(colors[nowc]["XS"])
    c1.setOutline(colors[nowc]["XS"])
    c1.draw(win)
    
    t1=Text(o1,ct[5])
    t1.setStyle("bold")
    t1.setSize(12)
    t1.setTextColor(colors[nowc]["L"])
    t1.draw(win)

    time.sleep(0.1)
    c1.undraw()
    t1.undraw()
    return


def uptime():
    """Update the time every moment and call all check button functions."""
    global ct
    flag=False
    while True:
        ct=list(time.localtime(time.time()))
        ct[8]=modf(time.time())[0] # get the decimal part of the second
        ct[3]=ct[3]+zones[timezone][1]
        if (ct[3]>23):
            ct[3]=ct[3]-24
            ct[2]=ct[2]+1
            if (ct[2]>calendar.monthrange(ct[0],ct[1])[1]):
                ct[2]=1
                ct[1]=ct[1]+1
                if (ct[1]>12):
                    ct[1]=ct[1]-12
                    ct[0]=ct[0]+1
        if ct[3]<0:
            ct[3]=ct[3]+24
            ct[2]=ct[2]-1
            if ct[2]<1:
                ct[1]=ct[1]-1
                if ct[1]<1:
                    ct[0]=ct[0]-1
                    ct[1]=ct[1]+12
                ct[2]=ct[2]+calendar.monthrange(ct[0],ct[1])[1]
        
        p1=win.checkMouse()
        if not win2.closed:
            p2=win2.checkMouse()
            if p2:
                checkcalendar(p2)
        if flag:
            upcalendar(Point(0,0))
            flag=False
        if(p1):
            if checkskinbutton(p1):
                drawinterface()
                uphm()
            if checkzonebutton(p1):
                flag=True
                continue
            checkalarbutton(p1)
            upcalendar(p1)
            checktimrbutton(p1)
            if checkquitbutton(p1):
                if not win.closed:
                    win.close()
                if not win2.closed:
                    win2.close()
                if not win3.closed:
                    win3.close()
                return
        upsec()
        updigi()
        if curm!=ct[4] or curh!=(30*ct[3]+0.5*ct[4]):
            uphm()
            checkalarm()
    return

    
def init():
    """Initialize the time at the beginning."""
    global ct
    ct=list(time.localtime(time.time()))
    ct[8]=modf(time.time())[0] # get the decimal part of the second
    ct[3]=ct[3]+zones[timezone][1]
    # hour>24 or hour<0 are not OK.
    if (ct[3]>24):
        ct[3]=ct[3]-24
        ct[2]=ct[2]+1
        if (ct[2]>calendar.monthrange(ct[0],ct[1])[1]):
            ct[2]=1
            ct[1]=ct[1]+1
            if (ct[1]>12):
                ct[1]=ct[1]-12
                ct[0]=ct[0]+1
    if ct[3]<0:
        ct[3]=ct[3]+24
        ct[2]=ct[2]-1
        if ct[2]<1:
            ct[1]=ct[1]-1
            if ct[1]<1:
                ct[0]=ct[0]-1
                ct[1]=ct[1]+12
            ct[2]=ct[2]+calendar.monthrange(ct[0],ct[1])[1]
    drawinterface()
    return
    

def main():
    init()
    print("Here~")
    uptime()
    return 0


main()
