from dataclasses import dataclass
from multiprocessing import connection
import obd
import pyrebase
from firebase import firebase
from firebase.firebase import FirebaseApplication
from firebase.firebase import FirebaseAuthentication

obd.logger.setLevel(obd.logging.DEBUG)

print("----------")

config = {
  "apiKey": "JWLCh2cap9Srbfn3NQVGdvIf1LCMWjaLzih1JRYd",
  "authDomain": "raspberrypi-8f9b4.firebaseapp.com",
  "databaseURL": "https://https://raspberrypi-8f9b4-default-rtdb.firebaseio.com/",
  "storageBucket": "raspberrypi-8f9b4.appspot.com"
}

#firebase = pyrebase.initialize_app(config)
#userEmail = 'thorfun.chin@gmail.com'
#userPass = 'Akmink57'
#auth = firebase.auth()
#user = auth.sign_in_with_email_and_password(userEmail,userPass)
#db = firebase.database()

connection = obd.Async(protocol="6", baudrate="115200", fast=False, timeout = 30)
#firebase = firebase.FirebaseApplication('https://raspberrypi-8f9b4-default-rtdb.firebaseio.com/', None)
firebaseApp = firebase.FirebaseApplication('https://raspberrypi-8f9b4-default-rtdb.firebaseio.com/',authentication =None)

#Continuously query until the amount of supported commands is greater than 100
while len(connection.supported_commands) < 100:
    connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="115200", fast=False, timeout = 30)

#Initial values
status = 0
engine_load = 0
coolant_temp = 0
fuel_pres = 0
rpm = 0
speed = 0
run_time = 0
distance_w_mil = 0
fuel_level = 0
baro_pres = 0
cmVolt = 0

#Commands to query for data
c_status = obd.commands.STATUS
c_engine_load = obd.commands.ENGINE_LOAD
c_coolant_temp = obd.commands.COOLANT_TEMP
c_fuel_pres = obd.commands.FUEL_PRESSURE
c_rpm = obd.commands.RPM
c_speed = obd.commands.SPEED
c_run_time = obd.commands.RUN
c_distance_w_mil = obd.commands.DISTANCE_W_MIL
c_fuel_level = obd.commands.FUEL_LEVEL
c_baro_pres = obd.commands.	BAROMETRIC_PRESSURE
c_cmVolt = obd.commands.CONTROL_MODULE_VOLTAGE

#Tracks the values of speed, rpm, and load since they will be constantly changing as you drive
def statusTracker(stt):
    global status
    if not stt.is_null():
        status = int(stt.value.magnitude)

def engine_loadTracker(egl):
    global engine_load
    if not egl.is_null():
        engine_load = int(egl.value.magnitude)

def coolant_tempTracker(clt):
    global coolant_temp
    if not clt.is_null():
        coolant_temp = int(clt.value.magnitude)

def fuel_presTracker(fep):
    global fuel_pres
    if not fep.is_null():
        fuel_pres = int(fep.value.magnitude * .621)

def rpmTracker(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.magnitude)

def speedTracker(s):
    global speed
    if not s.is_null():
        speed = int(s.value.magnitude * .621)

def run_timeTracker(rt):
    global run_time
    if not rt.is_null():
        run_time = int(rt.value.magnitude)

def distance_w_milTracker(dtwm):
    global distance_w_mil
    if not dtwm.is_null():
        distance_w_mil = int(dtwm.value.magnitude)

def fuel_levelTracker(felv):
    global fuel_level
    if not felv.is_null():
        fuel_level = int(felv.value.magnitude)

def baro_presTracker(brp):
    global baro_pres
    if not brp.is_null():
        baro_pres = int(brp.value.magnitude)

def cmVoltTracker(cmV):
    global cmVolt
    if not cmV.is_null():
        cmVolt = int(cmV.value.magnitude)

#Watches the data extracted by the obd adapter        
connection.watch(c_status , callback=statusTracker)
connection.watch(c_engine_load, callback=engine_loadTracker)
connection.watch(c_coolant_temp, callback=coolant_tempTracker)
connection.watch(c_fuel_pres, callback=fuel_presTracker)
connection.watch(c_rpm, callback=rpmTracker)
connection.watch(c_speed, callback=speedTracker)
connection.watch(c_run_time, callback=run_timeTracker)
connection.watch(c_distance_w_mil, callback=distance_w_milTracker)
connection.watch(c_fuel_level, callback=fuel_levelTracker)
connection.watch(c_baro_pres, callback=baro_presTracker)
connection.watch(c_cmVolt, callback=cmVoltTracker)
connection.start()

running = True

def update_firebase():
    
	DATA = {
        "status": str(status), 
        "engine_load": str(engine_load),
        "coolant_temp": str(coolant_temp),
        "fuel_pres": str(fuel_pres),
        "rpm": str(rpm),
        "speed": str(speed),
        "run_time": str(run_time),
        "distance_w_mil": str(distance_w_mil),
        "fuel_level": str(fuel_level),
        "baro_pres": str(baro_pres),
        "cmVolt": str(cmVolt)
    } 
firebaseApp.post("/obd", data)
#results = db.child("obd").push(DATA, user['JWLCh2cap9Srbfn3NQVGdvIf1LCMWjaLzih1JRYd'])       
#print(results)
	
print("----------")

while True:
	update_firebase()
