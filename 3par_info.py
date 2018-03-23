##############
# Al pulsar el boton: Lanza comandos a la cabina 3PAR para sacar informacion
##############

from Tkinter import *
import tkMessageBox
import tempfile
import paramiko, os, string, pprint, socket, traceback, sys

# Variables GLOBALES
nbytes = 4096
port = 22
hostname = ''    # Introduce tu IP o Nombre de tu cabina
username = ''    # Introduce tu usuario
password = ''    # Introduce tu password
command = ''      
stdout_data = []
stderr_data = []

# ---- Funcion que realiza la conexion ssh y lanza el comando, la salida la guarda en la lista stdout_data y stderr_data
def conexion_ssh(command):
	print "Conectando a la cabina...."

	client = paramiko.Transport((hostname, port))
	client.connect(username=username, password=password)
	
	session = client.open_channel(kind='session')
	session.exec_command(command)

	while True:
		if session.recv_ready():
			stdout_data.append(session.recv(nbytes))
		if session.recv_stderr_ready():
			stderr_data.append(session.recv_stderr(nbytes))
		if session.exit_status_ready():
			break

	session.close()
	client.close()

# ---- Funcion para listar todas las vlun de la cabina
def lista_all_vluns():
	command = 'showvv'
	conexion_ssh(command)
	print ''.join(stdout_data)
	
# ---- Funcion para sacar todas las vLuns que no tienen compresion activada
def lista_all_vluns_compresion_no():
	command = 'showvv -showcols Id,Name,Compr,Compression,VSize_MB -p -compr No'
	conexion_ssh(command)
	print ''.join(stdout_data)


# ###########################
# ### VENTANAS Y BOTONES ####
# ###########################
# # ventana principal
root = Tk()
root.title('HP 3PAR info')

## Etiquetas superiores e inferiores
logo = PhotoImage(file="buitre.gif")
label_logo = Label(root, image=logo)
label_logo.grid(row=0,column=4)

label_acciones = Label(root, text="Acciones:", justify=LEFT, font = "Helvetica 16 bold")
label_acciones.grid(row=0,column=0)

## BOTONES
boton1 = Button(root,text="Lista vLuns", command=lista_all_vluns)
boton1.grid(row=4,column=0)

boton2 = Button(root,text="Lista vLuns Compresion NO ", command=lista_all_vluns_compresion_no)
boton2.grid(row=4,column=1)

root.mainloop()
