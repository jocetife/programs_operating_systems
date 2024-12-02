# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:05:36 2024

@author: jocel
"""

import queue
import random
import tkinter as tk
from tkinter import ttk #no reemplaza los widgets tk

class Process:
    def __init__(self, operator, op1, op2, TME, ide):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.TME = TME
        self.ide = ide
        self.quantum = 0
        self.TT = 0
        self.TR = TME
        self.TRB = 7
        self.TLlegada = 0
        self.TFin = 0
        self.TEspera = 0
        self.TRetorno = 0
        self.TRespuesta = 0
        self.estado = "nuevo"
        self.interrupted = False
        self.has_error =  False
        self.first_execution = True
    def operation(self):
        if self.operator=="+":
            return self.op1 + self.op2
        elif self.operator=="-":
            return self.op1 - self.op2
        elif self.operator=="/":
            return self.op1/self.op2
        elif self.operator=="*":
            return self.op1 * self.op2
        elif self.operator=="%":
            return self.op1%self.op2
        

def events(event):
    global paused
    if event.char == ("p"):#----------------------------------------------
        paused = True
        title_runningprocess.config(text="Proceso en Pausa")
    if event.char == ("c"):#----------------------------------------------
        paused = False
        text_BCP.delete(1.0, tk.END)
        title_runningprocess.config(text="Proceso en Ejecución")
    if event.char == ("i"):#----------------------------------------------
        if paused or len(running) == 0:
            return
        else:
            blocked.append(running.pop())
    if event.char == ("e"):#----------------------------------------------
        if paused or len(running) == 0: #cuando esta en pausa no hacer nd
            return
        else:
            #se llena automaticamente por el len(running) == 0
            process_exe.has_error = True
            process_exe.TFin = global_counter
            process_exe.TRetorno = process_exe.TFin - process_exe.TLlegada
            process_exe.TEspera = process_exe.TRetorno - process_exe.TT
            finished.append(running.pop())
    if event.char == ("n"):#----------------------------------------------
        if paused:
            return
        else:
            process_creation()
            #pone los procesos en listos
            while len(ready) + len(blocked) < dp-1 and not qt.empty():#!!!!!!!!!!!!! se puede hasta cuatro, arreglao
                process = qt.get()
                process.TLlegada = global_counter
                ready.append(process)
            #actualizar listos
            printReady = "ID\tTME\tTT"
            for i in ready:
                printReady += "\n"+str(i.ide)+"\t"+str(i.TME)+"\t"+str(i.TT)
            text_readyprocess.delete(1.0, tk.END)
            text_readyprocess.insert(tk.END, printReady)
            
            process_counter = qt.qsize() #actualiza de inmediato
            label_newprocess.config(text="Procesos restantes: "+ str(process_counter)+"\tQ:"+str(quantum))
    if event.char == ("b"):#----------------------------------------------
        paused = True
        title_runningprocess.config(text="Proceso en Pausa")
        BCP()

def BCP():
    
    all_processes = list(qt.queue) + ready + blocked + running + finished
    all_processes.sort(key=lambda p: p.ide)
    
    bcp = ("  ID  Operacion\t\tRes\tTLl\tTF\tTS\tTRet\tTE\tTRes\tTME\tEstado \n"+
            "--------------------------------------------------------------------------------------------------------------------------------\n")
    
    for p in all_processes:
        resultado = round(p.operation(), 3) if not p.has_error else "Error"
        # Procesos nuevos
        if p in list(qt.queue):
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\tN/A\tN/A\tN/A\t0\tN/A\tN/A\tN/A\t{p.TME}\tNuevo\n"
        # Procesos en listo
        elif p in ready:
            p.TEspera = global_counter - p.TLlegada - p.TT if p.TT > 0 else global_counter - p.TLlegada
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\tN/A\t{p.TLlegada}\tN/A\t{p.TT}\tN/A\t{p.TEspera}\t{'N/A' if p.first_execution == True else p.TRespuesta}\t{p.TME}\tListo\n"
        # Procesos bloqueados    
        elif p in blocked:
            p.TEspera = global_counter - p.TLlegada - p.TT if p.TT > 0 else global_counter - p.TLlegada
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\tN/A\t{p.TLlegada}\tN/A\t{p.TT}\tN/A\t{p.TEspera}\t{p.TRespuesta}\t{p.TME}\tBloqueado\tTRB = {p.TRB+1}\n"            
        # Procesos en ejecucion    
        elif p in running:
            p.TEspera = p.TRespuesta if p.TT == 0 else global_counter - p.TLlegada - p.TT
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\tN/A\t{p.TLlegada}\tN/A\t{p.TT-1}\tN/A\t{p.TEspera}\t{p.TRespuesta}\t{p.TME}\tEjecutando\tTR = {p.TR+1}    Q = {p.quantum-1}\n"    
        # Procesos terminados    
        elif p in finished:
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\t{resultado}\t{p.TLlegada}\t{p.TFin}\t{p.TT}\t{p.TRetorno}\t{p.TEspera}\t{p.TRespuesta}\t{p.TME}\tTerminado\n"
    
    text_BCP.delete(1.0, tk.END)
    text_BCP.insert(tk.END, bcp)
    
def enterProcess(event):
    global process, i, quantum
    process = int(entry_enterprocess.get()) 
    quantum = int(entry_quantum.get())
    while i <= process:
        process_creation()
    window_enterprocess.destroy()

def process_creation():
    global qt, i
    
    operators = ["+", "-", "*", "/", "%"]
    operator = random.choice(operators)
    op1 = random.randint(1,100)
    op2 = random.randint(1,100)
    TME = random.randint(5,25)
    ide = i
    process_obj= Process(operator, op1, op2, TME, ide)
    qt.put(process_obj)
    i+=1

def update():
    global ready, running, finished, blocked, global_counter, dp, first_filling, qt, process, paused, process_exe
    
    #PAUSA
    if paused:
        window_FCFS.after(1000, update)
        return
    #LISTOS
    if len(running) == 0:
        #llenar por primera vez todos lo espacios
        if first_filling:
            while len(ready) < dp and not qt.empty():
                process = qt.get()
                process.TLlegada = global_counter
                ready.append(process)
            first_filling = False
        #llenar de uno en uno
        
        elif len(ready) + len(blocked) < dp and not qt.empty():#!!!!!!!!!!!!!!!!!!!!!!!!
            process = qt.get()
            process.TLlegada = global_counter
            ready.append(process)   
        #sacar un proceso a ejecucion
        if len(ready) > 0:
            process_exe = ready.pop(0)
            running.append(process_exe)
        printReady = "ID\tTME\tTT"
        for i in ready:
            printReady += "\n"+str(i.ide)+"\t"+str(i.TME)+"\t"+str(i.TT)
        
        text_readyprocess.delete(1.0, tk.END)
        text_readyprocess.insert(tk.END, printReady)   
    
    #TERMINADOS
        
        printFinished = "ID\tOperacion\t     Resultado"
        for i in finished:
            if i.has_error:
                printFinished += "\n"+str(i.ide)+"\t"+str(i.op1)+ str(i.operator)+str(i.op2)+"\t      Error"
            else:
                printFinished += "\n"+str(i.ide)+"\t"+str(i.op1)+ str(i.operator)+str(i.op2)+"\t      "+ str(round(i.operation(), 3))
        
        text_finishedprocess.delete(1.0, tk.END)
        text_finishedprocess.insert(tk.END, printFinished)
        #mensaje de terminado
        if qt.empty() and len(running) == 0 and len(blocked) == 0:
            end = "\n\n\n\n            Procesos terminados.\n            Contador global: " + str(global_counter)
            text_runningprocess.delete(1.0, tk.END)
            text_runningprocess.insert(tk.END, end)
            BCP()
            paused = True
    #BLOQUEADOS                                                                 si estan llenos los bloqueados, el proceso nulo
    if len(blocked) > 0:
        block = ""
        for i in blocked[:]: #una copia para que no haya problemas en la impresion 
            if i.TRB == 0:
                i.TRB = 7
                i.quantum = 0
                if len(running) == 0:   #si no hay proceso en ejecucion
                    running.append(i)
                else:                   #si hay, se pone en listos
                    ready.append(i)
                blocked.remove(i)
            else:
                block += "ID: " + str(i.ide) + "\nTRB: " + str(i.TRB) + "\n"
                i.TRB -= 1
                
        text_blockedprocess.delete(1.0, tk.END)
        text_blockedprocess.insert(tk.END, block)
        
        #actualizar listos cuando salga un bloqueado
        printReady = "ID\tTME\tTT"
        for i in ready:
            printReady += "\n"+str(i.ide)+"\t"+str(i.TME)+"\t"+str(i.TT)
        text_readyprocess.delete(1.0, tk.END)
        text_readyprocess.insert(tk.END, printReady)
    
    #EJECUCION
    print(len(running))
    if len(running) > 0: #si hay un proceso en ejecucion 
        for i in running:
            if i.first_execution:
                i.TRespuesta = global_counter - i.TLlegada
                i.first_execution = False
            printExe = ("ID:\t" + str(i.ide) + "\n" +
            "Operacion:\t" + str(i.operator) + "\n" +
            "TME:\t" + str(i.TME)+ "\n" +
            "Quan:\t" + str(i.quantum)+ "\n"
            "TT:\t" + str(i.TT) + "\n" +
            "TR:\t"+ str(i.TR) + "\n" +
            "\n\n~~~~~~~~Contador global: " + str(global_counter))
        
            i.TT += 1
            i.TR -= 1
            i.quantum += 1
            global_counter += 1
        
            if i.TR == 0:
                i.TFin = global_counter
                i.TRetorno = i.TFin - i.TLlegada
                i.TEspera = i.TRetorno - i.TT
                finished.append(running.pop())
            elif i.quantum == quantum:          #para que no haga pop a una lista vacia
                i.quantum = 0
                ready.append(running.pop())
            
            text_runningprocess.delete(1.0, tk.END)
            text_runningprocess.insert(tk.END, printExe)
                
                
    if len(running) == 0 and len(ready) == 0 and len(blocked)>0:# ejecucion proceso nulo
        printNull = ("ID:\tNull\n" +"Operacion:\t\n" +"TME:\t\n" +"TT:\t\n" +"TR:\t\n" +
        "\n\n~~~~~~~~Contador global: " + str(global_counter))
        global_counter += 1
        text_runningprocess.delete(1.0, tk.END)
        text_runningprocess.insert(tk.END, printNull)
    
    #procesos nuevos
    process_counter = qt.qsize()
    label_newprocess.config(text="Procesos restantes: "+ str(process_counter)+"\tQ:"+str(quantum))
    window_FCFS.after(1000, update)

#-------------------------------------------------------------------------------------------------------------

qt = queue.Queue()
ready = []
running = []
finished = []
blocked = []
global_counter = 0
dp = 5
first_filling = True
exe = False
process_exe = None #necesario para el evento de error
process = None
paused = False
quantum = None
i = 1

#-------------------------------------------------------------------------------------------------------------
window_enterprocess = tk.Tk()
window_enterprocess.title("Procesamiento FCFS")
window_enterprocess.geometry("355x120")

style = ttk.Style()
style.configure('TButton', font=('Tahoma', 10))
style.configure('TLabel', font=('Tahoma', 10))

frame_enterprocess= ttk.Frame(window_enterprocess)
frame_enterprocess.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

label_enterprocess= ttk.Label(frame_enterprocess, text='Numero de procesos a capturar:')
label_enterprocess.grid(row=0, column= 0, padx=5, pady=5)
entry_enterprocess= ttk.Entry(frame_enterprocess)
entry_enterprocess.grid(row=0, column= 1, padx=5, pady=5)
label_quantum= ttk.Label(frame_enterprocess, text='Especifica el Quantum:')
label_quantum.grid(row=1, column= 0, padx=5, pady=5)
entry_quantum= ttk.Entry(frame_enterprocess)
entry_quantum.grid(row=1, column= 1, padx=5, pady=5)
button_enterprocess= ttk.Button(frame_enterprocess, text= 'Enviar', command= lambda: enterProcess(0))
button_enterprocess.grid(row=2, column=0, columnspan=2, pady=10)

entry_enterprocess.bind('<Return>', enterProcess)

window_enterprocess.mainloop()

#-------------------------------------------------------------------------------------------------------------

window_FCFS = tk.Tk()
window_FCFS.title("Procesamiento FCFS")
window_FCFS.geometry("1250x500")
#Titulos
title_readyprocess = tk.Label(window_FCFS, text="Procesos Listos", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_runningprocess = tk.Label(window_FCFS, text="Proceso en Ejecución", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_finishedprocess = tk.Label(window_FCFS, text="Procesos Terminados", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_blockedprocess = tk.Label(window_FCFS, text="Procesos Bloqueados", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_BCP = tk.Label(window_FCFS, text="Bloque de Control de Procesos", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
label_newprocess = tk.Label(window_FCFS, bg="grey", fg="white", font=("Tahoma", 12))

#Texto
text_readyprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_runningprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_finishedprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_blockedprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_BCP = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
scroll_finishedprocess = tk.Scrollbar(window_FCFS, command=text_finishedprocess.yview)
text_finishedprocess.config(yscrollcommand=scroll_finishedprocess.set)


# Cuadrícula
title_readyprocess.grid(row=0, column=0, padx=5, pady=5, sticky='w')
text_readyprocess.grid(row=1, column=0, rowspan=2, padx=5, pady=5, sticky='nsew')
title_runningprocess.grid(row=0, column=1, padx=5, pady=5, sticky='w')
text_runningprocess.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
title_finishedprocess.grid(row=0, column=2, padx=5, pady=5, sticky='w')
text_finishedprocess.grid(row=1, column=2, rowspan=2, padx=5, pady=5, sticky='nsew')
scroll_finishedprocess.grid(row=1, column=3, sticky='ns')
title_blockedprocess.grid(row=3, column=0, padx=5, pady=5, sticky='w')
text_blockedprocess.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
label_newprocess.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
title_BCP.grid(row=3, column=1, padx=5, pady=5, sticky='w')
text_BCP.grid(row=4, column=1,columnspan=2, padx=5, pady=5, sticky='nsew')

window_FCFS.grid_columnconfigure(2, weight=1)
window_FCFS.grid_rowconfigure(1, weight=1)

window_FCFS.bind("<Key>", events)

update()
window_FCFS.mainloop()
