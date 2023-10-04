
from socket import *
import threading
import datetime

dire_server = 'localhost'
puerto_server = 8000

clientes_conectados = {}
contador_clientes = 1  # Contador para asignar identificadores únicos a los clientes

def manejar_cliente(socketConexion, addr):
    global contador_clientes
    
    cliente_id = contador_clientes
    contador_clientes += 1
    
    print(f"Conectado un cliente {cliente_id} desde {addr}")
    clientes_conectados[cliente_id] = socketConexion
    
    # Crear un archivo de log para el cliente
    log_filename = f"conversaciones_cliente_{cliente_id}.log"
    
    while True:
        mensajeRecibido = socketConexion.recv(1024).decode()
        print(f"Mensaje recibido de {cliente_id}: {mensajeRecibido}")
        
        if mensajeRecibido == 'adios':
            break
        
        # Registrar el mensaje en el archivo de log del cliente
        with open(log_filename, "a") as log_file:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - De Cliente {cliente_id}: {mensajeRecibido}\n")
        
        # Retransmitir mensaje a todos los clientes conectados
        for id_cliente, cliente in clientes_conectados.items():
            if id_cliente != cliente_id:
                mensaje_con_identificador = f"Cliente {cliente_id}: {mensajeRecibido}"
                try:
                    cliente.send(mensaje_con_identificador.encode())
                except:
                    del clientes_conectados[id_cliente]
    
    print(f'Desconectado el cliente {cliente_id} desde {addr}')
    socketConexion.close()
    del clientes_conectados[cliente_id]

socketServidor = socket(AF_INET, SOCK_STREAM)
socketServidor.bind((dire_server, puerto_server))
socketServidor.listen()

print("Esperando conexiones...")

while True:
    socketConexion, addr = socketServidor.accept()
    cliente_thread = threading.Thread(target=manejar_cliente, args=(socketConexion, addr))
    cliente_thread.start()
