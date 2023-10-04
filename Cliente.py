
#from socket import *
#import os
#import threading
#import queue
#import tkinter as tk
#from tkinter import scrolledtext, Entry, Button
#import sys

#class Cliente:
    #def __init__(self, host, port, nombre, mensajes_queue):
     #   self.socketCliente = socket(AF_INET, SOCK_STREAM)
      #  self.socketCliente.connect((host, port))
       # self.nombre = nombre
        #self.mensajes_queue = mensajes_queue

        #self.root = tk.Tk()
        #self.root.title(f"Cliente Chat - {self.nombre}")

        #self.mensaje_entry = Entry(self.root)
        #self.mensaje_entry.pack()

        #self.enviar_boton = Button(self.root, text="Enviar Mensaje", command=self.enviar_mensaje)
        #self.enviar_boton.pack()

        #self.archivo_entry = Entry(self.root)
        #self.archivo_entry.pack()

        #self.enviar_archivo_boton = Button(self.root, text="Enviar Archivo", command=self.enviar_archivo)
        #self.enviar_archivo_boton.pack()

        #self.mensajes_texto = scrolledtext.ScrolledText(self.root)
        #self.mensajes_texto.pack()

        #self.hilo_recepcion = threading.Thread(target=self.recibir_mensajes)
        #self.hilo_recepcion.start()

        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    #def enviar_mensaje(self):
     #   mensajeEnviar = self.mensaje_entry.get()
      #  mensaje_con_nombre = f"{self.nombre}: {mensajeEnviar}"
       # self.socketCliente.send(mensaje_con_nombre.encode())
        #self.mensaje_entry.delete(0, tk.END)
       # if mensajeEnviar == 'adios':
        #    self.root.destroy()

    #def enviar_archivo(self):
     #   filename = self.archivo_entry.get()
      #  try:
       #     file_size = os.path.getsize(filename)
        #except OSError:
         #   print("Archivo no encontrado.")
          #  return

        #self.socketCliente.send(filename.encode())
        #self.socketCliente.send(str(file_size).encode())

        #with open(filename, 'rb') as file:
         #   for data in iter(lambda: file.read(1024), b''):
          #      self.socketCliente.send(data)

        #print("Archivo enviado.")

    #def recibir_mensajes(self):
     #   while True:
      #      try:
       #         mensajeRecibido = self.socketCliente.recv(1024).decode()
        #        if not mensajeRecibido:
         #           break
          #      self.mensajes_queue.put(mensajeRecibido)
           # except ConnectionAbortedError:
            #    break

    #def on_closing(self):
     #   self.socketCliente.close()
      #  sys.exit(0)

#class Aplicacion:
   # def __init__(self, root):
    #    self.root = root
     #   self.clientes = []

      #  self.agregar_cliente_boton = Button(self.root, text="Agregar Cliente", command=self.agregar_cliente)
       # self.agregar_cliente_boton.pack()

    #def agregar_cliente(self):
     #   nombre_cliente = input("Ingrese su nombre: ")
      #  mensajes_queue = queue.Queue()
       # nuevo_cliente = Cliente('localhost', 8000, nombre_cliente, mensajes_queue)
        #self.clientes.append((nuevo_cliente, mensajes_queue))
        #hilo_mostrar_mensajes = threading.Thread(target=self.mostrar_mensajes, args=(nuevo_cliente,))
        #hilo_mostrar_mensajes.start()

    #def mostrar_mensajes(self, cliente):
     #   while True:
      #      mensajeRecibido = cliente.mensajes_queue.get()
       #     self.root.after(0, cliente.mensajes_texto.insert, tk.END, mensajeRecibido + "\n")

#def iniciar_aplicacion():
   # root = tk.Tk()
    #root.title("Aplicación de Chat Múltiple")

    #app = Aplicacion(root)

    #root.mainloop()

#if __name__ == "__main__":
    #iniciar_aplicacion()


from socket import *
import os
import threading
import queue
import tkinter as tk
from tkinter import scrolledtext, Entry, Button
import sys

class Cliente:
    def __init__(self, host, port, nombre, mensajes_queue):
        self.socketCliente = socket(AF_INET, SOCK_STREAM)
        self.socketCliente.connect((host, port))
        self.nombre = nombre
        self.mensajes_queue = mensajes_queue

        self.root = tk.Tk()
        self.root.title(f"Cliente Chat - {self.nombre}")
        self.root.configure(bg="#87CEEB") 
        self.mensaje_entry = Entry(self.root, font=("Helvetica", 12), bg="darkblue", fg="white", borderwidth=2, relief="solid" )
        self.mensaje_entry.pack()

        self.enviar_boton = Button(self.root, text="Enviar Mensaje", command=self.enviar_mensaje, font=("Helvetica", 12, "bold"), bg="green", fg="white", borderwidth=2, relief="solid")
        self.enviar_boton.pack(padx=10, pady=10)

        self.archivo_entry = Entry(self.root, font=("Helvetica", 12), bg="darkblue", fg="white", borderwidth=2, relief="solid")
        self.archivo_entry.pack()

        self.enviar_archivo_boton = tk.Button(self.root, text="Enviar Archivo", command=self.enviar_archivo, font=("Helvetica", 12, "bold"), bg="green", fg="white", borderwidth=2, relief="solid")
        self.enviar_archivo_boton.pack(padx=10, pady=10)

        
        self.mensajes_texto = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Helvetica", 12), bg="black", fg="white")
        self.mensajes_texto.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.hilo_recepcion = threading.Thread(target=self.recibir_mensajes)
        self.hilo_recepcion.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def enviar_mensaje(self):
        mensajeEnviar = self.mensaje_entry.get()
        mensaje_con_nombre = f"{self.nombre}: {mensajeEnviar}"
        self.socketCliente.send(mensaje_con_nombre.encode())
        self.mensaje_entry.delete(0, tk.END)
        if mensajeEnviar == 'adios':
            self.root.destroy()
    """
    def enviar_archivo(self):
        filename = self.archivo_entry.get()
        try:
            file_size = os.path.getsize(filename)
        except OSError:
            print("Archivo no encontrado.")
            return

        self.socketCliente.send(filename.encode())
       # self.socketCliente.send(str(file_size).encode())

        with open(filename, 'rb') as file:
            for data in iter(lambda: file.read(1024), b''):
                self.socketCliente.send(data)

        # Enviar un mensaje al widget de mensajes_texto para indicar que el archivo se ha enviado
        self.mensajes_queue.put("Archivo enviado")

        print("Archivo enviado.")
    """
    def enviar_archivo(self):
        filename = self.archivo_entry.get()
        try:
            file_size = os.path.getsize(filename)
        except OSError:
            print("Archivo no encontrado.")
            return

        self.socketCliente.send(filename.encode())
       # self.socketCliente.send(str(file_size).encode())

        with open(filename, 'rb') as file:
            for data in iter(lambda: file.read(1024), b''):
                self.socketCliente.send(data)

        print("Archivo enviado.")

    def recibir_mensajes(self):
        while True:
            try:
                mensajeRecibido = self.socketCliente.recv(1024).decode()
                if not mensajeRecibido:
                    break
                self.mensajes_queue.put(mensajeRecibido)
            except ConnectionAbortedError:
                break

    def on_closing(self):
        self.socketCliente.close()
        sys.exit(0)

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.clientes = []

        self.agregar_cliente_boton = Button(self.root, text="Agregar Cliente", command=self.agregar_cliente)
        self.agregar_cliente_boton.pack()

    def agregar_cliente(self):
        nombre_cliente = input("Ingrese su nombre: ")
        mensajes_queue = queue.Queue()
        nuevo_cliente = Cliente('localhost', 8000, nombre_cliente, mensajes_queue)
        self.clientes.append((nuevo_cliente, mensajes_queue))
        hilo_mostrar_mensajes = threading.Thread(target=self.mostrar_mensajes, args=(nuevo_cliente,))
        hilo_mostrar_mensajes.start()

    def mostrar_mensajes(self, cliente):
        while True:
            mensajeRecibido = cliente.mensajes_queue.get()
            self.root.after(0, cliente.mensajes_texto.insert, tk.END, mensajeRecibido + "\n")

def iniciar_aplicacion():
    root = tk.Tk()
    root.title("Aplicación de Chat Múltiple")

    app = Aplicacion(root)

    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()
