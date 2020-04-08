import socket
import time
from threading import Thread
import hashlib


def main():
    host='localhost'
    port=6666
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Crea el servidor
    s.bind((host,port))

    print("El servidor esta escuchando en el puerto %d" %port)
    texto=int (input("\n Que texto desea enviar?"
                     "\n 1. 100 mib"
                     "\n 2. 250 mib"))
    if texto==1:
        f="file1"
    else:
        f="file2.txt"
    global file
    file=f
    print("Archivo seleccionado: ",file)
    num_conn= int( input('\n Cuantas conexiones desea recibir?' ))

    print("Esperando conexiones")
    cont=0
    while cont<num_conn:

        #establish connection with client
        # c is a socket object to send and receive messages
        #print("cont=",cont)
        data,adrr=s.recvfrom(1024)
        print("Recibi conexion",cont)
        #Crea el thread para manejar la conexion
        thread=Thread(target= start_thread, args=(s,adrr))
        thread.start()
        cont+=1

def start_thread(s,adrr):
    start_time=time.time
    m=hashlib.sha256()

    num_paquetes=0
    with open(file,'rb') as f:
        while True:
            data=f.read(1024)
            if not data:
                print ("termine de leer")
                #envio del hash
                h=str(m.hexdigest())
                print("El digest que mando es"+h)
                s.sendto(("HASH"+h).encode(),adrr)
                print("El numero de paquetes eviados es de ",num_paquetes)
                break
            #print(len(data))
            #print(data)
            # start=0
            # end=1024
            # while True:
            #     #print("end esta en ", end)
            #     sent_data = data[start:end]
            #     start = end+1
            #     if end+1025<len(data):
            #         end+=1025
            #     else:
            #         size=len(data)-end
            #         end=size
            #     m.update(sent_data)
            #     #print(sent_data)
            #     s.sendto(sent_data, adrr)
            #     if not sent_data:
            #         print("Termine de partir los fragmentos")
            #         break
            m.update(data)
            s.sendto(data,adrr)
            num_paquetes+=1

main()

