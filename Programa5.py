# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:09:04 2024

@author: ferna
"""

#from itertools import cycle
import tkinter as tk
import random
posiciones = "   1      2       3       4       5       6      7      8      9    10     11     12     13    14    15    16    17     18     19    20"


size_conteiner = 20
conteiner = ["___"] * size_conteiner
#circularList = cycle(range(len(conteiner)))

last_position_productor = -1
last_position_consumidor = -1

cant_productor = 0
cant_consumidor = 0

proceso_en_curso = False


def dormir(tiempo, funcion):
    root.after(tiempo, funcion)

def produccion_consumo():
    if proceso_en_curso:
        return
    tiempo_productor = random.randint(1000, 3000) 
    tiempo_consumidor = random.randint(1000, 3000)
    
    tiempo_productor_label.set(f"Tiempo Productor: {tiempo_productor} ms")
    tiempo_consumidor_label.set(f"Tiempo Consumidor: {tiempo_consumidor} ms")
    
    if tiempo_productor < tiempo_consumidor:
        if espacio_productor():
            dormir(tiempo_productor, ini_productor)
        else: 
            produccion_consumo()
    else:
        if espacio_consumidor():
            dormir(tiempo_consumidor, ini_consumidor)
        else: 
            produccion_consumo()

def espacio_productor():
    return "___" in conteiner

def espacio_consumidor():
    return "*" in conteiner

def ini_productor():
    global proceso_en_curso, cant_productor
    if proceso_en_curso:
        return
 
    proceso_en_curso = True
    cant_productor = random.randint(3, 6)
    cantidad_productor_label.set(f"Cantidad Productor: {cant_productor}")
    productor()

def productor():
    global last_position_productor, cant_productor, proceso_en_curso
    if cant_productor > 0 and espacio_productor():
        if last_position_productor == -1:
            current_position = 0
        else:
            current_position = (last_position_productor + 1) % len(conteiner)   
        
        if conteiner[current_position] == "___":  
            conteiner[current_position] = "*"
            last_position_productor = current_position
            cant_productor -= 1
            estado_conteiner.set(vista_conteiner(conteiner)) 
            root.after(1000, productor)
    else:
        proceso_en_curso = False  
        produccion_consumo()
                
        
def ini_consumidor():
    global proceso_en_curso, cant_consumidor
    if proceso_en_curso:
        return
    
    proceso_en_curso = True
    cant_consumidor = random.randint(3, 6)
    cantidad_consumidor_label.set(f"Cantidad Consumidor: {cant_consumidor}")
    consumidor()
    
def consumidor():
    global last_position_consumidor, cant_consumidor, proceso_en_curso
    if cant_consumidor > 0 and espacio_consumidor():
        if last_position_consumidor == -1:
            current_position = 0
        else:
            current_position = (last_position_consumidor + 1) % len(conteiner)   
        
        if conteiner[current_position] == "*":
            conteiner[current_position] = "___"
            last_position_consumidor = current_position
            cant_consumidor -= 1
            estado_conteiner.set(vista_conteiner(conteiner)) 
            root.after(1000, consumidor)
    else:
        proceso_en_curso = False
        produccion_consumo()

def vista_conteiner(conteiner):
    vista = "|"
    for item in conteiner:
        if item == "___":
            vista += "⬜|"
        else:
            vista += "⬛|"
    return vista

def salir(event=None):
    root.quit()  
    root.destroy()


# Crear la ventana principal
root = tk.Tk()
root.title("Productor y Consumidor")

root.bind("<Escape>", salir)

tiempo_productor_label = tk.StringVar()
tiempo_consumidor_label = tk.StringVar()
cantidad_productor_label = tk.StringVar()
cantidad_consumidor_label = tk.StringVar()

# Agregar el título
title = tk.Label(root, text="Producto - Consumidor", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='we')

# Estado del contenedor
estado_conteiner = tk.StringVar()
estado_conteiner.set("Estado del contenedor: " + vista_conteiner(conteiner))
label = tk.Label(root, textvariable=estado_conteiner, font=("Helvetica", 16))
label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')

# Posiciones del contenedor
pos_label = tk.Label(root, text=posiciones, font=("Helvetica", 12))  # Muestra la variable posiciones
pos_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')

# Etiquetas para tiempos y cantidades
label_tiempo_productor = tk.Label(root, textvariable=tiempo_productor_label, font=("Helvetica", 10))
label_tiempo_productor.grid(row=3, column=0, padx=5, pady=5, sticky='w')

label_tiempo_consumidor = tk.Label(root, textvariable=tiempo_consumidor_label, font=("Helvetica", 10))
label_tiempo_consumidor.grid(row=3, column=1, padx=5, pady=5, sticky='w')

label_cantidad_productor = tk.Label(root, textvariable=cantidad_productor_label, font=("Helvetica", 10))
label_cantidad_productor.grid(row=4, column=0, padx=5, pady=5, sticky='w')

label_cantidad_consumidor = tk.Label(root, textvariable=cantidad_consumidor_label, font=("Helvetica", 10))
label_cantidad_consumidor.grid(row=4, column=1, padx=5, pady=5, sticky='w')

# Iniciar la simulación
produccion_consumo()

# Ejecutar la aplicación
root.mainloop() 