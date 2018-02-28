import RPi.GPIO as GPIO
import time
#import datetime
import os
import sys
import socket
#import getopt
from decimal import Decimal
#from platform import system as sys_name
from threading import Thread

resultados = {} #Diccionario donde se guardan los resultados
puertos = {}

threadsA = []
threadsB = []

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 16

GPIO.setup(led, GPIO.OUT)

def mask():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    if len(ip_address) > 15:
        sys.exit()
    count = 1
    puntos = 0
    mask = []
    while count < len(ip_address):
        if ip_address[count] == ".":
            puntos += 1
            if puntos == 3:
                return str(mask)
        else:
            mask[count] = ip_address[count]
        count += 1

def scan(host,port):
	s = socket.socket()
	result = s.connect_ex((host,port))
	#print('working on port > '+(str(port)))      
	addr = str(host) + ":" + str(port)
	if result == 0:
		puertos[addr] = "Abierto"
		#print((str(port))+' -> open') 
		s.close()
	else:
		puertos[addr] = "Cerrado"
		#print((str(port))+' -> close') 
		s.close()

def file_n():
	fm = "pinglog.txt"
	return fm

"""
def usage():
       
       print("Uso: Ping")
       print("")
       print("-i Inicio")
       print("-f Fin")
       print("-d Direccion")
       print("-h info de ayuda")

try:
       opts, args = getopt.getopt(sys.argv[1:], "i:f:d:h")

except getopt.GetoptError as err:
       print("Error: "+str(err)+", Intente -h para ayuda\n\n")
       usage()
       sys.exit(2)

for o, a in opts:
       if o in ("-h"):
              usage()
              sys.exit()
       if o in ("-i"):
              y = Decimal(a)
       if o in ("-f"):
              x = Decimal(a)
       if o in ("-d"):
              d = a
"""

dirin = int(input("Direccion Inicio: "))
dirfin = int(input("Direccion Fin: "))
portev = int(input("Puerto a evaluar: "))
test = mask()
print(test)
a = "192.168.1"

def iptest(y):
     
       direc = a + "." + str(y)
       response = os.system("ping -c 1 " + direc)
       #response = os.system("ping " + parameters + direc)
       if response == 0:
              pingstatus = "Ususario Activo"
              resultados[y] = pingstatus
              #print("Usuario: " + direc + " Activo")
       else:
              pingstatus = "Usuario no Activo"
              #print("Usuario: " + direc + " No Activo")

GPIO.output(led,1)

for i in range(dirin, dirfin+1):
	t1 = Thread(target=iptest, args=(i,))
	threadsA.append(t1)
	t1.start()
	
[x.join() for x in threadsA]

for k in resultados:
	host1 = a + "." + str(k)
	t2 = Thread(target=scan, args=(host1,portev,))
	threadsB.append(t2)
	t2.start()	    

[z.join() for z in threadsB]
		    
pinglog = open(file_n(),"w")
pinglog.write("Analisis IPs\n")
for k in resultados:
	pinglog.write("Estado " + str(k) + ": " + str(resultados[k]) + " ;)\n")
pinglog.write("Analisis Puertos\n")
for k in puertos:
	pinglog.write("Puerto " + str(k) + " estado: " + str(puertos[k]) + " ;)\n")
pinglog.close()

GPIO.output(led,0)

"""
for k in resultados:
	test = a + "." + str(k)
	scan(test,p)
	
pinglog = open(file_n(),"a")
for k in puertos:
	pinglog.write("Puerto " + str(k) + " estado: " + str(puertos[k]) + " ;)\n")
pinglog.close()
"""
