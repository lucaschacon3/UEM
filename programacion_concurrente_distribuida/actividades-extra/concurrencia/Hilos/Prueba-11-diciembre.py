import time 
import threading 
import multiprocessing

SLEEP = 10

def esperar(sec):
    processName = multiprocessing.current_process().name
    threadName = threading.current_thread().name
    print(f"{processName} * {threadName} AHH DORMIRR")

    time.sleep(sec)

    print(f"{processName} * {threadName} ... YA HE DESPERTADO")

    print(multiprocessing.get_all_start_methods())
    # NO LLAMAR set_start_method AQUÍ
    # multiprocessing.set_start_method("fork", force=True)

if __name__ == "__main__":
    multiprocessing.set_start_method("fork", force=True)  
    p = multiprocessing.Process(target=esperar, args=(SLEEP,))
    p.start()
    p.join()
