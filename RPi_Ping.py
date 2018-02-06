import RPi.GPIO as GPIO
import time
import os
import sys
import socket
#import getopt
from decimal import Decimal
from platform import system as sys_name

resultados = {} #Diccionario donde se guardan los resultados
puertos = {}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 16

GPIO.setup(led, GPIO.OUT)

def scan(host,port):
	s = socket.socket()
	result = s.connect_ex((host,port))
	print('working on port > '+(str(port)))      
	if result == 0:
		puertos[port] = "Open"
		print((str(port))+' -> open') 
		s.close()
	else:
		puertos[port] = "Close"
		print((str(port))+' -> close') 
		s.close()

#def usage():
       
       #print("Uso: Ping")
       #print("")
       #print("-i Inicio")
       #print("-f Fin")
       #print("-d Direccion")
       #print("-h info de ayuda")

#try:
       #opts, args = getopt.getopt(sys.argv[1:], "i:f:d:h")

#except getopt.GetoptError as err:
       #print("Error: "+str(err)+", Intente -h para ayuda\n\n")
       #usage()
       #sys.exit(2)

#for o, a in opts:
       #if o in ("-h"):
              #usage()
              #sys.exit()
       #if o in ("-i"):
              #y = Decimal(a)
       #if o in ("-f"):
              #x = Decimal(a)
       #if o in ("-d"):
              #d = a
y = Decimal(input("Direccion Inicio: "))
x = Decimal(input("Direccion Fin: "))
p = Decimal(input("Puerto: "))
a = "192.168.1"
parameters = "-n 1 " if sys_name().lower()=="windows" else "-c 1 "
while y <= x:
       GPIO.output(led,1)
       direc = a + "." + str(y)
       #response = os.system("ping -c 1 " + direc)
       response = os.system("ping " + parameters + direc)
       if response == 0:
              pingstatus = "Ususario Activo"
              resultados[y] = pingstatus
              print("Usuario: " + direc + " Activo")
       else:
              pingstatus = "Usuario no Activo"
              print("Usuario: " + direc + " No Activo")
       y=y+1
GPIO.output(led,0)
pinglog = open("pinglog.txt","a")
for k in resultados:
       pinglog.write("Usuario: " + a + "." + str(k) + " Activo\n")
       test = a + "." + str(k)
       scan(test,p)
       #print("Usuario: " + a + "." + str(k) + " Activo")
pinglog.close()
