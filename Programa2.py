import queue
import random
import tkinter as tk 
from tkinter import ttk


class Process:
    def __init__(self, operator, op1, op2, TME, ide, TT):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.TME = TME
        self.ide = ide
        self.TT  = 0
        self.TR = TME
        self.interrupted = False
        self.has_error =  False
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
    global qp
    global qt
    global cont_global
    global actual_batch
    global fin_process
    global batch_count
    global dp
    global TT
    global TR
    global j 
    global timer_id
    
    if TR > 0:
        
        exprocess =("ID:\t" + str(process_obj.ide) + "\n" +
        "Operacion:\t" + str(process_obj.operator) + "\n" +
        "TME:\t" + str(process_obj.TME)+ "\n" +
        "Tiempo transcurrido:\t" + str(TT) + "\n" +
        "Tiempo restante:\t"+ str(TR) + "\n" +
        "\n\n~~~~~~~~~~~~Contador global: " + str(cont_global))
        
        TT += 1
        TR -= 1
        cont_global += 1    
        text_procej.delete(1.0, tk.END)
        text_procej.insert(tk.END, exprocess)  
        
        label_leftbatch.config(text="Lotes restantes: "+ str(batch_count - 1))
        
        printLoteAct()
        
        after()
        
    else:
        printProcter()
        nextprocess()

def printProcter():
    global fin_process
    global dp
    global process
    
    if len(fin_process) < process:
        fin_process.append(process_obj)
    n=0
    finprocess=" ID\tOperacion        Resultado\n"
    for p in fin_process:
        if n % dp == 0 and n != 0:
            finprocess= finprocess + "\n................................. lote "+ str(n//dp) + "\n"
        if p.has_error:
            finprocess= (finprocess + " " + str(p.ide)+ "\t   " + str(p.op1) + str(p.operator) + str(p.op2) + "\t            " + "Error\n")
        else:
            finprocess= (finprocess + " " + str(p.ide)+ "\t   " + str(p.op1) + str(p.operator) + str(p.op2) +"\t            " + str(round(p.operation(), 3)) + "\n")
        n += 1
        if n == process:
            finprocess= finprocess +"\n................................. lote " + str(int(batch)) + "\n"
    text_procter.delete(1.0, tk.END)
    text_procter.insert(tk.END, finprocess)
    
def nextprocess():
    global qp
    global process_obj
    global first_process
    global cont_global
    global TR
    global TT
    global j
    
    j += 1
    
    if not qp.empty():
        process_obj = qp.get()
        if not process_obj.interrupted: 
            TR = process_obj.TME
            TT = 1
        else:
            TR = process_obj.TR
            TT = process_obj.TT
        update()
    else:
        if (TR <= 0 or process_obj.has_error) and qt.empty() and qp.empty():
            text_procej.delete(1.0, tk.END)
            text_procej.insert(tk.END, "\n\n\n            Procesos completados.\n            contador global: " + str(cont_global))
            text_loctact.delete(1.0, tk.END)
            label_leftbatch.config(text="Lotes restantes: 0")
            TR = 0
        else:
            Fbatch()    

def error(): 
    global process_obj
    global flag

    #no funcione con la pausa
    if not flag:
        return
    else:
        process_obj.has_error = True
        printProcter()
        nextprocess()


def Fbatch():
    global qt
    global qp
    global process_obj
    global batch_count
    global j
    
    if qp.empty() and qt.empty():
        text_loctact.delete(1.0, tk.END)
    else:
        actual_batch.clear()
        j=0
        #llenar qp otra vez con qt
        while not qp.full() and not qt.empty():
            process_obj=qt.get()
            qp.put(process_obj)
            actual_batch.append(process_obj)
        batch_count -= 1
        nextprocess()
        
def printLoteAct():
    global actual_batch
    global j
    
    allProcess = "ID\t     TME\t              TT"
    for ab in actual_batch[j:]:
        allProcess = allProcess + "\n" + str(ab.ide) + "\t      " + str(ab.TME) + "\t              " + str(ab.TT)
    text_loctact.delete(1.0, tk.END)
    text_loctact.insert(tk.END, allProcess)  
    
    
def after():
    global flag, timer_id
    if flag:
        if timer_id:
            root.after_cancel(timer_id)        
        timer_id = root.after(1000, update)
        
def interruption():
    global qp
    global process_obj
    global TR
    global TT
    global j
    
    #no funcione con la pausa
    if not flag:
        return
    else: 
        process_obj.TT = TT
        process_obj.TR = TR
        
        process_obj.interrupted = True
        
        qp.put(process_obj)  
        
        actual_batch.append(actual_batch.pop(j-1))
        
        if not qp.empty():
            process_obj = qp.get()
            TR = process_obj.TR  
            TT = process_obj.TT
            update()


    
def interrupciones(event):
    global flag
    
    if event.char == ("p" or "P"):
        flag = False
    if event.char == ("c" or "C"):
        flag = True
        after()
    if event.char == ("i" or "I"):
        interruption()
    if event.char == ("e" or "E"):
        error()    

timer_id = None
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
if (process%dp!=0):
    batch = process//dp + 1
else:
    batch = process/dp

print("Numero de lotes: ", batch)

qt = queue.Queue(process)
qp = queue.Queue(dp)
cont_global = 1

actual_batch=[]
fin_process = []
batch_count = batch
j = 1
flag = True


i = 1
while i<=process:
    operators = ["+", "-", "*", "/", "%"]
    operator = random.choice(operators)
    op1 = random.randint(1,100)
    op2 = random.randint(1,100)
    TME = random.randint(3,14)
    ide = i
    TT = TME
    process_obj= Process(operator, op1, op2, TME, ide, TT)
    qt.put(process_obj)
    i+=1

while not qp.full() and not qt.empty():
    process_obj=qt.get()
    qp.put(process_obj)
    actual_batch.append(process_obj)

TR = process_obj.TME
TT = 1
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
title_lotact = tk.Label(root, text="Lote Actual", bg="grey", fg="white", font=("Calibri", 14, "bold"))
title_procej = tk.Label(root, text="Proceso en Ejecución", bg="grey", fg="white", font=("Calibri", 14, "bold"))
title_procter = tk.Label(root, text="Procesos Terminados", bg="grey", fg="white", font=("Calibri", 14, "bold"))


# Texto
text_loctact = tk.Text(root, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Calibri", 12))
text_procej = tk.Text(root, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Calibri", 12))
text_procter = tk.Text(root, bg="grey", fg="white", wrap=tk.WORD, height=10, width=30, font=("Calibri", 12))
scroll_procter = tk.Scrollbar(root, command=text_procter.yview)
text_procter.config(yscrollcommand=scroll_procter.set)
label_leftbatch = tk.Label(root, bg="black", fg="white", padx="15", pady="10", anchor='w')

# Cuadrícula
title_lotact.grid(row=0, column=0, padx=5, pady=5, sticky='w')
text_loctact.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

title_procej.grid(row=0, column=1, padx=5, pady=5, sticky='w')
text_procej.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

title_procter.grid(row=0, column=2, padx=5, pady=5, sticky='w')
text_procter.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
scroll_procter.grid(row=1, column=3, sticky='ns')

label_leftbatch.grid(row=3, column=0, columnspan=3, pady=3, sticky='nsew')


root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)

root.bind("<Key>", interrupciones)

process_obj = qp.get()
root.after(1000, update)
root.mainloop()

