import queue
import random
import tkinter as tk 
from tkinter import ttk


class Process:
    def __init__(self, operator, op1, op2, TME, ide, TLlegada=0, estado=0):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.TME = TME
        self.ide = ide
        self.TT  = 0
        self.TR = TME
        self.TTB = 7
        self.TLlegada = TLlegada
        self.TFin = 0
        self.TEspera = 0
        self.TRetorno = 0
        self.TRespuesta = 0
        self.estado = estado
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
        

def sendP():
    global process
    process = int(process_entry.get())
    window.destroy()
    
def update():
    global flag2
    global process_count
    
    ReadyProcess()
    if process_count < 0:
        if len(actual_ready) == 0 and len(blocked) == dp + process_count:
            if not process_exe.has_error:
                Null()
            after()
        elif process_exe.TR > 0:   
            Execution()
            after()
        else:
            flag2 = True
            FinishedProcess()
    else: 
        if len(actual_ready) == 0 and len(blocked) == dp:
            if not process_exe.has_error:
                Null()
            after()
        elif process_exe.TR > 0:   
            Execution()
            after()
        else:
            flag2 = True
            FinishedProcess()
        
        
def FinishedProcess():
    global fin_process
    global process
    global process_count
    global dp
    global flag
    
    
    process_exe.TFin = cont_global
    process_exe.TRetorno = process_exe.TFin - process_exe.TLlegada
    process_exe.TEspera = process_exe.TRetorno - process_exe.TT
    
    
    if len(fin_process) < process:
        fin_process.append(process_exe)
        
    finprocess=" ID\tOperacion        Resultado\n"
    for p in fin_process:
        if p.has_error:
            finprocess= (finprocess + " " + str(p.ide)+ "\t   " + str(p.op1) + str(p.operator) + str(p.op2) + "\t            " + "Error\n")
        else:
            finprocess= (finprocess + " " + str(p.ide)+ "\t   " + str(p.op1) + str(p.operator) + str(p.op2) +"\t            " + str(round(p.operation(), 3)) + "\n")
    process_count -= 1
    text_procter.delete(1.0, tk.END)
    text_procter.insert(tk.END, finprocess)
    if len(actual_ready) > 0 and not process_exe.has_error:
        update()
    elif process_exe.has_error:
        if not len(actual_ready) > 0:
            text_procej.delete(1.0, tk.END)
            text_procej.insert(tk.END, "\n\n\n            a)Procesos completados.\n            contador global: " + str(cont_global))
            BCP()
        else:
            ReadyProcess()
    else:
        if len(blocked) > 0:
            update()
        else:
            text_procej.delete(1.0, tk.END)
            text_procej.insert(tk.END, "\n\n\n            b)Procesos completados.\n            contador global: " + str(cont_global))
            BCP()
    
def ReadyProcess():
    global dp
    global process_exe
    global flag2
    global flag_ffull
    
    if flag2:
        
        if flag_ffull:
            while len(actual_ready) < dp: #llena la lista por primera vez
                if not qt.empty():
                    process_obj=qt.get()
                    process_obj.TLlegada = cont_global
                    actual_ready.append(process_obj)
                else:
                    break
            flag_ffull = False
        elif len(actual_ready) < dp and not flag_ffull:
            if not qt.empty():
                process_obj=qt.get()
                process_obj.TLlegada = cont_global
                actual_ready.append(process_obj)
        if len(actual_ready) > 0:
            process_exe = actual_ready.pop(0)
            
        allProcess = "ID\t     TME\t              TT"
        for ar in actual_ready:
            allProcess = allProcess + "\n" + str(ar.ide) + "\t      " + str(ar.TME) + "\t              " + str(ar.TT)
        
        
        flag2 = False
        text_loctact.delete(1.0, tk.END)
        text_loctact.insert(tk.END, allProcess) 
    
    
def Execution():
    global cont_global
    global process_count
    global dp
    
    if process_exe.first_execution:
        process_exe.TRespuesta = cont_global - process_exe.TLlegada
        process_exe.first_execution = False
    
    exprocess =("ID:\t" + str(process_exe.ide) + "\n" +
    "Operacion:\t" + str(process_exe.operator) + "\n" +
    "TME:\t" + str(process_exe.TME)+ "\n" +
    "Tiempo transcurrido:\t" + str(process_exe.TT) + "\n" +
    "Tiempo restante:\t"+ str(process_exe.TR) + "\n" +
    "\n\n~~~~~~~~~~~~Contador global: " + str(cont_global))
            
    process_exe.TT += 1
    process_exe.TR -= 1
    cont_global += 1 
        
    BlockedProcess()
        
    text_procej.delete(1.0, tk.END)
    text_procej.insert(tk.END, exprocess)
              
    if process_count < 0:    
        label_leftbatch.config(text="Procesos restantes: 0")
    else:
        label_leftbatch.config(text="Procesos restantes: "+ str(process_count))
    
def Null():
    global cont_global
    global process_count
    global dp 
    
    exprocess =("ID:\tNull\n" +
    "Operacion:\t\n" +
    "TME:\t\n" +
    "Tiempo transcurrido:\t\n" +
    "Tiempo restante:\t\n" +
    "\n\n~~~~~~~~~~~~Contador global: " + str(cont_global))
            
    cont_global += 1    
    BlockedProcess()
        
    text_procej.delete(1.0, tk.END)
    text_procej.insert(tk.END, exprocess)
                  
    if process_count < 0:    
        label_leftbatch.config(text="Procesos restantes: 0")
    else:
        label_leftbatch.config(text="Procesos restantes: "+ str(process_count))
         
    
def error(): 
    global flag
    global flag2

    if not flag:
        return
    else:
        process_exe.has_error = True
        process_exe.TR = 0
        flag2 = True
        FinishedProcess()
        

def after():
    global flag
    
    if flag:
        root.after(1000, update)
        
    
def interrupciones(event):
    global flag
    global flag_null
    global process_exe
    global process
    global i
    global process_count
    global bcp_window
    
    if event.char == ("p" or "P"):
        flag = False
    if event.char == ("c" or "C"):
        flag = True
        after()
        if bcp_window:
            bcp_window.destroy()
            bcp_window = None
    if event.char == ("i" or "I"):
        if len(blocked) == dp:
            return
        elif process_count < 0:
            if len(actual_ready) == 0 and len(blocked) == dp + process_count:
                return
        process_exe.interrupted = True
        blocked.append(process_exe)
        if len(actual_ready) > 0:
            process_exe = actual_ready.pop(0)
        if process_count < 0:
            if len(actual_ready) == 0 and len(blocked) == dp + process_count:
                process_exe = blocked[0]
                flag_null = True
        else:
            if len(actual_ready) == 0 and len(blocked) == dp:
                process_exe = blocked[0]
                flag_null = True
    if event.char == ("e" or "E"): 
        if len(blocked) == dp:
            return
        elif process_count < 0:
            if len(actual_ready) == 0 and len(blocked) == dp + process_count:
                return
        error()
    if event.char == ("n" or "N"):
        process+=1
        operators = ["+", "-", "*", "/", "%"]
        operator = random.choice(operators)
        op1 = random.randint(1,100)
        op2 = random.randint(1,100)
        TME = random.randint(5,25)
        ide = i
        TT = TME
        process_obj= Process(operator, op1, op2, TME, ide)
        qt.put(process_obj)
        i+=1
        process_count+=1
        
        if process_count < 0:    
            label_leftbatch.config(text="Procesos restantes: 0")
        else:
            label_leftbatch.config(text="Procesos restantes: "+ str(process_count))
        
        total = len(actual_ready) + len(blocked)
        
        if total < dp - 1:
            process_obj=qt.get()
            process_obj.TLlegada = cont_global
            actual_ready.append(process_obj)
            allProcess = "ID\t     TME\t              TT"
            for ar in actual_ready:
                allProcess = allProcess + "\n" + str(ar.ide) + "\t      " + str(ar.TME) + "\t              " + str(ar.TT)
            
            text_loctact.delete(1.0, tk.END)
            text_loctact.insert(tk.END, allProcess) 
    
    if event.char == ("b" or "B"):
        flag = False
        BCP()            
        
        
def BlockedProcess():
    global flag_null
    
    if not flag:
        return
    else:
        block =""
        index = 0
        for b in blocked[:]:
            if not b.TTB > 0:
                b.interrupted = False
                b.TTB = 7
                if flag_null:
                    flag_null= False
                else:
                    actual_ready.append(b)
                blocked.remove(b)
                index +=1
            else:
                block += ("ID: " + str(b.ide) + "\nTTB: " + str(b.TTB) + "\n")
                b.TTB -= 1
    
        allProcess = "ID\t     TME\t              TT"
        for ar in actual_ready:
            allProcess = allProcess + "\n" + str(ar.ide) + "\t      " + str(ar.TME) + "\t              " + str(ar.TT)
        text_loctact.delete(1.0, tk.END)
        text_loctact.insert(tk.END, allProcess)
        
        text_bloqueado.delete(1.0, tk.END)
        text_bloqueado.insert(tk.END, block)
        
        
def BCP():
    global bcp_window
   
    if bcp_window is None: 
        bcp_window = tk.Toplevel(root)
        bcp_window.title("Bloque de Control de Procesos (BCP)")
       
        frame = tk.Frame(bcp_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
       
        bcp_text = tk.Text(frame, bg="grey", fg="white", wrap=tk.WORD, height=15, width=130, font=("Calibri", 12))
        bcp_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=bcp_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        bcp_text.config(yscrollcommand=scrollbar.set)
       
        all_processes = list(qt.queue) + actual_ready + blocked + ([process_exe] if process_exe else []) + fin_process
        all_processes.sort(key=lambda p: p.ide)
        
        bcp = "  ID       Operacion       Resultado       TLlegada       TFin       TServicio       TRetorno       TEspera       TRespuesta       TME          Estado \n"
        
        for p in all_processes:
            resultado = round(p.operation(), 3) if not p.has_error else "Error"
            
            # Procesos nuevos
            if p in list(qt.queue):
                bcp += f"  {p.ide}\t {p.op1} {p.operator} {p.op2}\t        N/A\t\t {p.TLlegada}\t   N/A\t    0\t          N/A\t\tN/A\t        N/A\t           {p.TME}\t        Nuevo\n"
            
            # Procesos en listo
            elif p in actual_ready:
                p.TEspera = cont_global - p.TLlegada - p.TT if p.TT > 0 else cont_global - p.TLlegada
                bcp += f"  {p.ide}\t {p.op1} {p.operator} {p.op2}\t        {'N/A' if p.TFin == 0 else resultado}\t\t {p.TLlegada}\t   {'N/A' if p.TFin == 0 else p.TFin}\t    {p.TT}\t          {p.TRetorno}\t\t{p.TEspera}\t        {p.TRespuesta}\t           {p.TME}\t        Listo\n"
                
            # Procesos bloqueados    
            elif p in blocked:
                p.TEspera = cont_global - p.TLlegada - p.TT if p.TT > 0 else cont_global - p.TLlegada
                bcp += f"  {p.ide}\t {p.op1} {p.operator} {p.op2}\t        {'N/A' if p.TFin == 0 else resultado}\t\t {p.TLlegada}\t   {'N/A' if p.TFin == 0 else p.TFin}\t    {p.TT}\t          {p.TRetorno}\t\t{p.TEspera}\t        {p.TRespuesta}\t           {p.TME}\t        Bloqueado        TTB = {p.TTB}\n"
                
            # Procesos en ejecucion    
            elif p == process_exe:
                process_exe.TEspera = p.TRespuesta if process_exe.TT == 0 else cont_global - process_exe.TLlegada - process_exe.TT
                bcp += f"  {p.ide}\t {p.op1} {p.operator} {p.op2}\t        {'N/A' if p.TFin == 0 else resultado}\t\t {p.TLlegada}\t   {'N/A' if p.TFin == 0 else p.TFin}\t    {p.TT}\t          {p.TRetorno}\t\t{p.TEspera}\t        {p.TRespuesta}\t           {p.TME}\t        Ejecutando       TR = {process_exe.TR}\n"
                
            # Procesos terminados    
            elif p in fin_process:
                bcp += f"  {p.ide}\t {p.op1} {p.operator} {p.op2}\t        {resultado}\t\t {p.TLlegada}\t   {p.TFin}\t    {p.TT}\t          {p.TRetorno}\t\t{p.TEspera}\t        {p.TRespuesta}\t           {p.TME}\t        Terminado\n"
          
        bcp_text.insert(tk.END, bcp)
        bcp_text.config(state=tk.DISABLED)
           
        bcp_window.mainloop()

window = tk.Tk()
window.title("Procesamiento por Lotes")
window.geometry("400x130")  # Tamaño de la ventana

# Estilo de la ventana
style = ttk.Style()
style.configure('TButton', font=('Calibri', 10), padding=10)
style.configure('TLabel', font=('Calibri', 10))

# Frame para entrada de datos
frame_input = ttk.Frame(window, padding=10)
frame_input.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

label_ingproc = ttk.Label(frame_input, text="Número de procesos a capturar: ")
process_entry = ttk.Entry(frame_input)
button1 = ttk.Button(frame_input, text="Enviar", command=sendP)

label_ingproc.grid(row=0, column=0, padx=5, pady=5, sticky='w')
process_entry.grid(row=0, column=1, padx=5, pady=5)
button1.grid(row=1, column=0, columnspan=2, pady=10)

window.mainloop()
#----------------------------------------------------------------
#division de procesos
print(process)

dp=5

qt = queue.Queue(process)
cont_global = 0

actual_ready=[]
fin_process = []
blocked = []
process_count = process-dp
process_exe = None
flag = True
flag2 = True
flag_ffull = True
flag_null = False
bcp_window = None

i = 1
while i<=process:
    operators = ["+", "-", "*", "/", "%"]
    operator = random.choice(operators)
    op1 = random.randint(1,100)
    op2 = random.randint(1,100)
    TME = random.randint(5,25)
    ide = i
    TT = TME
    process_obj= Process(operator, op1, op2, TME, ide)
    qt.put(process_obj)
    i+=1


#--------------------------------------------------------------
root=tk.Tk()
root.config(bg="white")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Títulos
title_lotact = tk.Label(root, text="Procesos Listos", bg="grey", fg="white", font=("Calibri", 14, "bold"))
title_procej = tk.Label(root, text="Proceso en Ejecución", bg="grey", fg="white", font=("Calibri", 14, "bold"))
title_procter = tk.Label(root, text="Procesos Terminados", bg="grey", fg="white", font=("Calibri", 14, "bold"))
title_bloqueado = tk.Label(root, text="Procesos Bloqueados", bg="grey", fg="white", font=("Calibri", 14, "bold"))


# Texto
text_loctact = tk.Text(root, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Calibri", 12))
text_procej = tk.Text(root, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Calibri", 12))
text_procter = tk.Text(root, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Calibri", 12))
text_bloqueado = tk.Text(root, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Calibri", 12))
scroll_procter = tk.Scrollbar(root, command=text_procter.yview)
text_procter.config(yscrollcommand=scroll_procter.set)
label_leftbatch = tk.Label(root, bg="grey", fg="white", padx="15", pady="10", anchor='w')

# Cuadrícula
title_lotact.grid(row=0, column=0, padx=5, pady=5, sticky='w')
text_loctact.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

title_procej.grid(row=0, column=1, padx=5, pady=5, sticky='w')
text_procej.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

title_procter.grid(row=0, column=2, padx=5, pady=5, sticky='w')
text_procter.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
scroll_procter.grid(row=1, column=3, sticky='ns')

title_bloqueado.grid(row=2, column=0, padx=5, pady=5, sticky='w')
text_bloqueado.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

label_leftbatch.grid(row=3, column=1, columnspan=2, pady=3, sticky='nsew')

root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)

root.bind("<Key>", interrupciones)

update()
root.mainloop()



