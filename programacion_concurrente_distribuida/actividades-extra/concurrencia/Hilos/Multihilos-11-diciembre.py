import os
import multiprocessing


processid = os.fork()
print( processid)
if processid > 0:
    print("Soy el proceso padre")
    print("ID proceso.:", os .getpid())
    print("ID  hijo", os .getppid())
else:
    print("Proceso hijo")
    print("ID proceso.:", os .getpid())
    print("ID padre:", os .getppid())


print(multiprocessing.get_all_start_methods())
multiprocessing.set_start_method("fork", force=True)

##CODIGO JUST FOR MAC 
