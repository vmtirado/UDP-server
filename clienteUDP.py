import socket
import logging
import time
import hashlib
from _thread import *
from threading import Thread

def main():
    # Se inicializa el log
    logging.basicConfig(filename="clientLog.log", level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )

    #Numero de thread de cliente que se van a crear
    numt=int(input("Cuantos threads de cliente quiere correr?"))
    for i in range(numt):
        #Crea el hash del thread
        m=hashlib.sha256()
        try:
            #Crea el objeto thread
            thread= Thread(target = threaded, args = (m,i))

            #Se inicia el objeto thred
            thread.start()
        except:
            logging.warning("Error al invocar el thread")


def threaded(m,i):
    start_time=time.time()
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    #Define the port where you want to connect
    port=6666
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Se conecta al servidor
    s.connect((host, port))
    print("Thread #%d listo para recibir informacion" %i)
    logging.info("CLIENTE Thread #%d ready to receive info" %i)
    s.sendto("listo".encode(),(host,port))
    #Se empieza a recibir informacion
    cont=0
    num_paquetes=0
    f = open("ctext.txt", 'wb')
    while True:
        data,adrr=s.recvfrom(1024)
        num_paquetes+=1
        f.write(data)
        #print(data)
        #print(type(data))
        #print("Cont esta en ",cont)
        #print(data)
        if (data.__contains__(b"HASH")):
            print("Encontre el hash")
            i=data.find(b"HASH")
            m.update(data[:i])
            hash_recibido = data[i+4:]
            print("El hash recibido es ", hash_recibido)
            print("El hash calculado es",m.hexdigest())
            if m.hexdigest()== hash_recibido.decode():
                print("Hash correcto :)")
                logging.info("Hash correcto")
                print("El numero de paquetes recibidos es de ", num_paquetes)
            else:
                print("Hash incorrecto :'(")
                logging.info("Hash incorrecto")
                print("El numero de paquetes recibidos es de ", num_paquetes)
            if not data:
                break
        m.update(data)
        cont+=1

    logging.info("CLIENTE Tiempo del envio %s", (time.time() - start_time))
    logging.info("---------------------------------------------")

    s.close()


main()






