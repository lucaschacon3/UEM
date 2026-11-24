from cliente_datos import connectar
from cliente_conexion import enviar_numer , enviar_fin_get_suma
import random

import socket

ip = "localhost"
port = 1234


def main():

    conn,address = connectar(ip,port)

    flag =True

    while flag:

            user = input("INGRESAR   START : ").upper()

            for _ in range(5):

                if user != "START":
                    fin = enviar_fin_get_suma(conn,address)
                    print(f"enviamos fin... {fin}")
    
                else:
                    if user == "START":
                        n = random.randint(1,9)
                        print(f"Numeros =>{n}")
                        print(f"Enviamos OK{n}")
                    else:
                            user =="FIN"
                            otroFin = enviar_fin_get_suma(conn,address)
                            print(f"ENVIAMOS FIN Y LA SUMA {otroFin}")
                            flag = False

                       

main()





        

            


