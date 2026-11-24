import threading 
import time



def imprimirA():
    while True:
        print("A");
        time.sleep(2);

def imprimirB():
    while True:
        print("B")
        time.sleep(3)



h1 =  threading.Thread(target = imprimirA);
h2 = threading.Thread(target = imprimirB)

h1.start();
h2.start();

h1.join();
h2.join();