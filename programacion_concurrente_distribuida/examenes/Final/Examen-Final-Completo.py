#PARTE ESCRITA
# Escribe un programa que cuente números, de uno en uno, en un servidor.
# El programa tendrá un cliente en un subproceso (cliente) que se comunicará con el servidor mediante sockets.
# El cliente enviará una cierta cantidad de números aleatorios. Tras cada envío, recibirá un OK cuando el servidor haya sumado el número.
# Cuando termine de enviar todos los números, enviará un mensaje FIN, cerrará la conexión y finalizará.


#PARTE DIGITAL
# Escribe uno o varios programas que cuenten numeros en paralelo, de uno en uno, hasta un valor maximo configurable.

# El sistema tendra un servidor, y varios clientes(al menos dos), que se comunicaran por sockets con el servidor.

# Cada cliente tendrá que abrir una conexion con el servidor, enviar un numero y esperar un OK como respuesta
# antes de enviar el siguiente numero. Cuando se termina de enviar numeros, se envia un FIN. Tras el FIN se esperara
# el valor de la suma de lo snumeros enviados y cerrará la conexion. Si en un lugar de un OK se recibe un MAX, enviara
# un FIN automaticamnete y esperara un ultimo valor con el maximo valor sumado.

# El servidor tendra que aceptar conexiones, esperar numeros y sumarlos a una lista, deodne cada coenxin sumara numeros
# siempre en la misma posicion de la lista. Despues de cada suma, se esperara entre 2 y 5 segundos para devolver un OK
# Si en lugar de un numero se recibe un FIN, se devolvera el valor sumado hasta el momento. Si alguna de las conexiones
# llega(o se pasa) del numero maximo, se devolvera un mensaje MAX

# Despues de las acciones tras un FIN, ambos lados cerraran la conexion afectada

# Disea el program cliente en un sencillo modelo de N capas, donde en la capa de datos se realicen las conexion, envio y 
# recepcion de mensajes y en la capa de usuario se le muestre al usuairo  las respuestas del servidor, se le preungte al 
# usuaio que numero quiere enviar y se le de la opcion de mandar un FIN. El diseño de la capa de negio debera comunicar
# debidamente el resto de capas.

#se puede implete todo en un solo progrma o en dos, uno para el servidor y otro spara los clientes

