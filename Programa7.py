import random
import tkinter as tk
from tkinter import ttk #no reemplaza los widgets tk

class Process:
    def __init__(self, ide):
        self.operator = random.choice(["+", "-", "*", "/", "%"])
        self.op1 = random.randint(1,100)
        self.op2 = random.randint(1,100)
        self.TME = random.randint(5,16)
        self.ide = ide
        self.quantum = 0
        self.TT  = 0
        self.TR = self.TME
        self.TRB = 7
        self.TLlegada = 0
        self.TFin = 0
        self.TEspera = 0
        self.TRetorno = 0
        self.TRespuesta = 0
        self.marco = 5
        self.peso = random.randint(6, 26)
        self.paginas = self.div_pag()
        self.fragmento = self.frag()
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
    def div_pag(self):
        if self.peso%self.marco == 0: #hace la division de las paginas
            return self.peso/self.marco
        else:
            return (self.peso//self.marco) + 1
    def frag(self):
        return self.peso%self.marco #devuelve el sobrante
            
    
def events(event):
    global paused, memoria
    if event.char == ("p"):#----------------------------------------------
        paused = True
        title_runningprocess.config(text="Proceso en Pausa")
    if event.char == ("c"):#----------------------------------------------
        paused = False
        text_BCP.delete(1.0, tk.END)
        title_runningprocess.config(text="Proceso en Ejecución")
        text_BCP.grid(row=4, column=1,columnspan=2, padx=5, pady=5, sticky='nsew')
        text_memory.grid(row=1, column=3,rowspan=4, padx=5, pady=5, sticky='nsew')
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
            memoria += process_exe.paginas
            for label in labels:
                if label["ide"] == process_exe.ide:
                    label["label_cell"].config(text="")
                    label["label_process"].config(text="")
                    label["estado"] = 0
            finished.append(running.pop())
    if event.char == ("n"):#----------------------------------------------
        if paused:
            return
        else:
            process_creation()
            #pone los procesos en listos
            if len(total) != 0:
                while total[0].paginas <= memoria:
                    process = total.pop(0)
                    ready.append(process)
                    memoria -= process.paginas
                    process.TLlegada = global_counter
                    
                    rellenado = 0
                    i = 0
                    while process.paginas > rellenado:
                        if labels[i]["estado"] == 0:
                            rellenado += 1
                            if process.paginas == rellenado:
                                if process.fragmento == 1:
                                    labels[i]["label_cell"].config(text="██",foreground='blue')
                                    labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                    labels[i]["estado"] = 1
                                    labels[i]["ide"] = process.ide
                                elif process.fragmento == 2:
                                    labels[i]["label_cell"].config(text="██ ██ ",foreground='blue')
                                    labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                    labels[i]["estado"] = 1
                                    labels[i]["ide"] = process.ide
                                elif process.fragmento == 3:
                                    labels[i]["label_cell"].config(text="██ ██ ██ ",foreground='blue')
                                    labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                    labels[i]["estado"] = 1
                                    labels[i]["ide"] = process.ide
                                elif process.fragmento == 4:
                                    labels[i]["label_cell"].config(text="██ ██ ██ ██",foreground='blue')
                                    labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                    labels[i]["estado"] = 1
                                    labels[i]["ide"] = process.ide
                                elif process.fragmento == 0:
                                    labels[i]["label_cell"].config(text="██ ██ ██ ██ ██",foreground='blue')
                                    labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                    labels[i]["estado"] = 1
                                    labels[i]["ide"] = process.ide
                            else:
                                labels[i]["label_cell"].config(text="██ ██ ██ ██ ██",foreground='blue')
                                labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                labels[i]["estado"] = 1
                                labels[i]["ide"] = process.ide
                        else:
                            i += 1
                    if len(total) == 0:
                        break
            #actualizar listos
            printReady = "ID\tTME\tTT\tPeso"
            for i in ready:
                printReady += "\n"+str(i.ide)+"\t"+str(i.TME)+"\t"+str(i.TT)+"\t"+str(i.peso)
                for label in labels:
                    if label["ide"] == i.ide:
                        label["label_cell"].config(foreground="blue")
                        label["label_process"].config(foreground="blue")
            text_readyprocess.delete(1.0, tk.END)
            text_readyprocess.insert(tk.END, printReady)
            
            process_counter = len(total) #actualiza de inmediato
            label_newprocess.config(text="Procesos restantes: "+ str(process_counter)+"\tQ:"+str(quantum))
    if event.char == ("b"):#----------------------------------------------
        paused = True
        title_runningprocess.config(text="Proceso en Pausa")
        BCP()

def BCP():
    text_BCP.grid(row=4, column=1,columnspan=3, padx=5, pady=5, sticky='nsew')
    text_memory.grid(row=1, column=3,rowspan=3, padx=5, pady=5, sticky='nsew')
    
    all_processes = total + ready + blocked + running + finished + retenedor
    all_processes.sort(key=lambda p: p.ide)
    
    bcp = ("  ID  Operacion\t\tRes\tTLl\tTF\tTS\tTRet\tTE\tTRes\tTME\tEstado \n"+
            "--------------------------------------------------------------------------------------------------------------------------------\n")

    for p in all_processes:
        resultado = round(p.operation(), 3) if not p.has_error else "Error"
        # Procesos nuevos
        if p in total:
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
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\tN/A\t{p.TLlegada}\tN/A\t{p.TT-1}\tN/A\t{p.TEspera}\t{p.TRespuesta}\t{p.TME}\tEjecutando\tTR = {p.TR+1}\n"    
        elif p in retenedor:
            p.TEspera = p.TRespuesta if p.TT == 0 else global_counter - p.TLlegada - p.TT
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\tN/A\t{p.TLlegada}\tN/A\t{p.TT-1}\tN/A\t{p.TEspera}\t{p.TRespuesta}\t{p.TME}\tEjecutando\tTR = {p.TR+1}\n"
        # Procesos terminados    
        elif p in finished:
            bcp += f"  {p.ide}    {p.op1} {p.operator} {p.op2}\t\t{resultado}\t{p.TLlegada}\t{p.TFin}\t{p.TT}\t{p.TRetorno}\t{p.TEspera}\t{p.TRespuesta}\t{p.TME}\tTerminado\n"
    
    text_BCP.delete(1.0, tk.END)
    text_BCP.insert(tk.END, bcp)
    
def enterProcess(event):
    global process, pro, quantum
    process = int(entry_enterprocess.get())    
    quantum = int(entry_quantum.get())
    while pro <= process:
        process_creation()
    window_enterprocess.destroy()

def process_creation():
    global pro
    
    ide = pro
    process_obj= Process(ide)
    total.append(process_obj)
    pro+=1

def update():
    global ready, running, finished, blocked, global_counter, process, paused, process_exe, memoria, labels, belong, pro, retenedor
    
    #PAUSA
    if paused:
        window_FCFS.after(1000, update)
        return
    
    #retenedor ejecucion
    if len(running) > 0:
        if len(retenedor) > 0:
            retenedor.pop()
            
    if len(retenedor) > 0:
        if retenedor[0].TR == 0:
            memoria += retenedor[0].paginas
            for label in labels:
                if label["ide"] == retenedor[0].ide:
                    label["label_cell"].config(text="")
                    label["label_process"].config(text="")
                    label["estado"] = 0
            finished.append(retenedor.pop())
        elif retenedor[0].quantum == quantum:
            retenedor[0].quantum = 0
            for label in labels:
                if label["ide"] == retenedor[0].ide:
                    label["label_cell"].config(foreground='blue')
                    label["label_process"].config(foreground='blue')
            ready.append(retenedor.pop())
    
    #LISTOS
    if len(running) == 0:
        if len(total) != 0:
            while total[0].paginas <= memoria:
                process = total.pop(0)
                ready.append(process)
                memoria -= process.paginas
                process.TLlegada = global_counter
                
                rellenado = 0
                i = 0
                while process.paginas > rellenado:
                    if labels[i]["estado"] == 0:
                        rellenado += 1
                        if process.paginas == rellenado:
                            if process.fragmento == 1:
                                labels[i]["label_cell"].config(text="██",foreground='blue')
                                labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                labels[i]["estado"] = 1
                                labels[i]["ide"] = process.ide
                            elif process.fragmento == 2:
                                labels[i]["label_cell"].config(text="██ ██ ",foreground='blue')
                                labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                labels[i]["estado"] = 1
                                labels[i]["ide"] = process.ide
                            elif process.fragmento == 3:
                                labels[i]["label_cell"].config(text="██ ██ ██ ",foreground='blue')
                                labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                labels[i]["estado"] = 1
                                labels[i]["ide"] = process.ide
                            elif process.fragmento == 4:
                                labels[i]["label_cell"].config(text="██ ██ ██ ██",foreground='blue')
                                labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                labels[i]["estado"] = 1
                                labels[i]["ide"] = process.ide
                            elif process.fragmento == 0:
                                labels[i]["label_cell"].config(text="██ ██ ██ ██ ██",foreground='blue')
                                labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                                labels[i]["estado"] = 1
                                labels[i]["ide"] = process.ide
                        else:
                            labels[i]["label_cell"].config(text="██ ██ ██ ██ ██",foreground='blue')
                            labels[i]["label_process"].config(text= process.ide ,foreground='blue')
                            labels[i]["estado"] = 1
                            labels[i]["ide"] = process.ide
                    else:
                        i += 1
                if len(total) == 0:
                    break
        #sacar un proceso a ejecucion
        if len(ready) > 0:
            process_exe = ready.pop(0)
            running.append(process_exe)
        printReady = "ID\tTME\tTT\tPeso"
        for i in ready:
            printReady += "\n"+str(i.ide)+"\t"+str(i.TME)+"\t"+str(i.TT)+"\t"+str(i.peso)
            for label in labels:
                if label["ide"] == i.ide:
                    label["label_cell"].config(foreground="blue")
                    label["label_process"].config(foreground="blue")
        
        text_readyprocess.delete(1.0, tk.END)
        text_readyprocess.insert(tk.END, printReady)  
    
    #TERMINADOS
        #limpiar la memoria
        printFinished = "ID\tOperacion\t     Resultado"
        
        for i in finished:
            if i.has_error:
                printFinished += "\n"+str(i.ide)+"\t"+str(i.op1)+ str(i.operator)+str(i.op2)+"\t      Error"
            else:
                printFinished += "\n"+str(i.ide)+"\t"+str(i.op1)+ str(i.operator)+str(i.op2)+"\t      "+ str(round(i.operation(), 3))
        
        text_finishedprocess.delete(1.0, tk.END)
        text_finishedprocess.insert(tk.END, printFinished)
        #mensaje de terminado
        if len(total) == 0 and len(running) == 0 and len(blocked) == 0:
            end = "\n\n\n\n            Procesos terminados.\n            Contador global: " + str(global_counter)
            text_runningprocess.delete(1.0, tk.END)
            text_runningprocess.insert(tk.END, end)
            BCP()
            paused = True
    #BLOQUEADOS      
    if len(blocked) > 0:
        block = ""
        for i in blocked[:]: #una copia para que no haya problemas en la impresion 
            for label in labels:
                if label["ide"] == i.ide:
                    label["label_cell"].config(foreground="purple")
                    label["label_process"].config(foreground="purple")
            if i.TRB == 0:
                i.TRB = 7
                i.quantum = 0
                if len(running) == 0:   #si no hay proceso en ejecucion
                    running.append(i)
                else:                   #si hay, se pone en listos
                    ready.append(i)
                    for label in labels:
                        if label["ide"] == i.ide:
                            label["label_cell"].config(foreground="blue")
                            label["label_process"].config(foreground="blue")
                blocked.remove(i)
            else:
                block += "ID: " + str(i.ide) + "\nTRB: " + str(i.TRB) + "\n"
                i.TRB -= 1
                
        text_blockedprocess.delete(1.0, tk.END)
        text_blockedprocess.insert(tk.END, block)
        
        #actualizar listos cuando salga un bloqueado
        printReady = "ID\tTME\tTT\tPeso"
        for i in ready:
            printReady += "\n"+str(i.ide)+"\t"+str(i.TME)+"\t"+str(i.TT)+"\t"+str(i.peso)
        text_readyprocess.delete(1.0, tk.END)
        text_readyprocess.insert(tk.END, printReady)
    
    
            
    #EJECUCION
    if len(running) > 0: #si hay un proceso en ejecucion 
        for i in running:
            
            printExe = ""
            if i.first_execution:
                i.TRespuesta = global_counter - i.TLlegada
                i.first_execution = False
            printExe = ("ID:\t" + str(i.ide) + "\n" +
            "Operacion:\t" + str(i.operator) + "\n" +
            "TME:\t" + str(i.TME)+ "\n" +
            "Quan:\t" + str(i.quantum)+ "\n"
            "TT:\t" + str(i.TT) + "\n" +
            "TR:\t"+ str(i.TR) + "\n" +
            "Peso:\t"+ str(i.peso) + "\n" +
            "\n\n~~~~~~~~Contador global: " + str(global_counter))
            
            for label in labels:
                if label["ide"] == i.ide:
                    label["label_cell"].config(foreground='red')
                    label["label_process"].config(foreground='red')

            
            if i.TR == 1:
                i.TFin = global_counter
                i.TRetorno = i.TFin - i.TLlegada
                i.TpEspera = i.TRetorno - i.TT
                
                retenedor.append(running.pop())
                
            elif i.quantum == quantum - 1:          #para que no haga pop a una lista vacia
                retenedor.append(running.pop())
                
                
            i.TT += 1
            i.TR -= 1
            i.quantum += 1
            global_counter += 1
            
            text_runningprocess.delete(1.0, tk.END)
            text_runningprocess.insert(tk.END, printExe)
            
    if len(running) == 0 and len(ready) == 0 and len(blocked)>0:# ejecucion proceso nulo
        printNull = ("ID:\tNull\n" +"Operacion:\t\n" +"TME:\t\n" +"TT:\t\n" +"TR:\t\n" +
        "\n\n~~~~~~~~Contador global: " + str(global_counter))
        global_counter += 1
        text_runningprocess.delete(1.0, tk.END)
        text_runningprocess.insert(tk.END, printNull)
            
    #procesos nuevos
    process_counter = len(total)
    label_newprocess.config(text="Procesos restantes: "+ str(process_counter)+"\tQ:"+str(quantum))
    
    if len(total) != 0:
        label_nextready.config(text="<"+str(total[0].ide)+">"+"  Peso del proximo proceso: "+ str(total[0].peso))
    else:
        label_nextready.config(text="Peso del proximo proceso: N/A")
    
    
    print("retenedor: "+str(len(retenedor)))
    if len(retenedor) > 0:
            print(retenedor[0].ide)
    print("ejecutado: "+str(len(running)))
    if len(running) > 0:
            print(running[0].ide)
    print("\n\n")
    window_FCFS.after(1000, update)
#-------------------------------------------------------------------------------------------------------------

total = []
ready = []
memoria = 44
running = []
finished = []
blocked = []
global_counter = 0
exe = False
process_exe = None #necesario para el evento de error
process = None
paused = False
quantum = None
pro = 1
labels = []
retenedor = []


#-------------------------------------------------------------------------------------------------------------
window_enterprocess = tk.Tk()
window_enterprocess.title("Paginación Simple")
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
window_FCFS.title("Paginación Simple")
window_FCFS.geometry("1300x600")
#Titulos
title_readyprocess = tk.Label(window_FCFS, text="Procesos Listos", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_runningprocess = tk.Label(window_FCFS, text="Proceso en Ejecución", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_finishedprocess = tk.Label(window_FCFS, text="Procesos Terminados", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_blockedprocess = tk.Label(window_FCFS, text="Procesos Bloqueados", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_BCP = tk.Label(window_FCFS, text="Bloque de Control de Procesos", bg="grey", fg="white", font=("Tahoma", 14, "bold"))
title_memory = tk.Label(window_FCFS, text="Tabla de Paginas", bg="grey", fg="white",font=("Tahoma", 14, "bold"))
label_newprocess = tk.Label(window_FCFS, bg="grey", fg="white", font=("Tahoma", 12))
label_nextready = tk.Label(window_FCFS, bg="grey", fg="white", font=("Tahoma", 12))


#Texto
text_readyprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_runningprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_finishedprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_blockedprocess = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_BCP = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))
text_memory = tk.Text(window_FCFS, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Tahoma", 12))

style = ttk.Style()
style.configure("Colored.TFrame", background="grey")
frame = ttk.Frame(text_memory, style='Colored.TFrame')
frame.pack(padx=5, pady=5, fill="both", expand=True)
rows = 24
cols = 2
celda = 1
for i in range(rows):
    for j in range(cols):
       label_num = ttk.Label(frame, relief="solid", text=str(celda), background='grey', foreground='white', font='Tahoma 10')
       label_num.grid(row=i, column=j*3,padx=2,sticky="nsew")
       label_cell = ttk.Label(frame, relief="solid",width=11,background='grey')
       label_cell.grid(row=i, column=(j*3)+1,padx=2,sticky="nsew")
       label_process = ttk.Label(frame, relief='solid', background='grey', font='Tahoma 10')
       label_process.grid(row=i, column=(j*3)+2,sticky='nsew')
       frame.grid_rowconfigure(i, weight=1)
       frame.grid_columnconfigure(j*3, weight=1)
       frame.grid_columnconfigure((j*3)+1, weight=10)
       frame.grid_columnconfigure((j*3)+2, weight=1)
       labels.append({"celda":celda,"estado":0,"label_cell":label_cell,"label_process":label_process,"ide":0}) 
       celda += 1

for i in range(44,48): #marcos que ocupa el sistema operativo
    labels[i]["label_cell"].config(text="██ ██ ██ ██ ██",foreground='black')
    labels[i]["estado"] = 1
    labels[i]["label_process"].config(text='S.O.',foreground='black')



# Cuadrícula
title_readyprocess.grid(row=0, column=0, padx=5, pady=5, sticky='w')
text_readyprocess.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
title_runningprocess.grid(row=0, column=1, padx=5, pady=5, sticky='w')
text_runningprocess.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
title_finishedprocess.grid(row=0, column=2, padx=5, pady=5, sticky='w')
text_finishedprocess.grid(row=1, column=2, rowspan=3, padx=5, pady=5, sticky='nsew')
title_memory.grid(row=0, column=3, padx=5, pady= 5, sticky='w')
text_memory.grid(row=1, column=3,rowspan=4, padx=5, pady=5, sticky='nsew')
title_blockedprocess.grid(row=3, column=0, padx=5, pady=5, sticky='w')
text_blockedprocess.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
label_newprocess.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
label_nextready.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
title_BCP.grid(row=3, column=1, padx=5, pady=5, sticky='w')
text_BCP.grid(row=4, column=1,columnspan=2, padx=5, pady=5, sticky='nsew')

window_FCFS.grid_columnconfigure(3, weight=1)
window_FCFS.grid_rowconfigure(1, weight=1)
window_FCFS.grid_rowconfigure(3, weight=1)
    
window_FCFS.bind("<Key>", events)

update()
window_FCFS.mainloop()