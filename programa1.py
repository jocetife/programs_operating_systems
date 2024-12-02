import time

Lista_Procesos = []
Lista_Lotes = []
Procesos_Terminados = []
global_counter = 0
cont = 1

# Pregunta al usuario
num_procesos = int(input('Ingrese la cantidad de números de procesos que desea ejecutar: '))
print("\n")

# Captura Datos
while cont <= num_procesos:
    print("- Proceso: ", cont)
    
    Name = str(input("Nombre: "))
    while True:
        ID = (input("ID: "))
        # Verifica si el ID ya existe en la lista de procesos
        if any(ID == x[1] for x in Lista_Procesos):
            print("ID inválido. Por favor, ingrese otro ID.")
        else:
            break           
    
    print("Operación: ")
    while True: 
        while True:
            try:
                num1 = int(input("Primer numero: "))
                break
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número entero.")
        operation = str(input("Operación a realizar: "))
        while True:
            try:
                num2 = int(input("Segundo numero: "))
                break
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número entero.") 
        
        resultado = None
        
        # SUMA
        if operation == "+":
            resultado = num1 + num2
        
        # RESTA
        elif operation == "-":
            resultado = num1 - num2
    
        # MULTIPLICACIÓN
        elif operation == "*":
            resultado = num1 * num2
        
        # MÓDULO
        elif operation == "%":
            while num2 == 0:
                print("Número inválido, division entre 0")
                num2 = int(input("Segundo número: "))
            resultado = num1 % num2
                
        # DIVISIÓN
        elif operation == "/":
            while num2 == 0:
                print("Número inválido, division entre 0")
                num2 = int(input("Segundo número: "))
            resultado = num1 / num2
        
        else: 
            print("Operando inválido, vuelva a intentarlo")
            continue
        break
    
    Operation = str(num1) + " " + operation + " " + str(num2)
    
    while True:
        try:
            TME = int(input("Tiempo máximo estimado: "))
            print("\n")
    
            # Valida que el TME sea mayor a 0
            while TME <= 0:
                print("Número inválido, el número tiene que ser mayor a 0")
                TME = int(input("Tiempo máximo estimado: "))
            break
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")
    
    # Ingresa datos a las listas     
    Proceso = [Name, ID, Operation, TME, resultado]
    Lista_Procesos.append(Proceso)
    cont += 1 
    
# Separación por lotes y procesos
dp=5
for i in range(0, len(Lista_Procesos), dp):
    lote = Lista_Procesos[i:i + dp]
    Lista_Lotes.append(lote)
    
pos = 0

while pos < len(Lista_Lotes):
    
    while True:
        # Filtra los procesos pendientes en el lote actual
        lote_actual = [x for x in Lista_Lotes[pos] if x not in Procesos_Terminados]
        
        # Si el lote actual está vacío, pasar al siguiente lote
        if not lote_actual:
            pos += 1
            break
        
        #Lote Actual
        print("-----------------------------------------------------")
        print("\nNo. de lotes pendientes: ", len(Lista_Lotes) - (pos + 1))
        print("\n~ LOTE ACTUAL ~\n")
        for x in lote_actual:
            print("Nombre:", x[0])
            print("Tiempo Máximo Estimado: ", x[3])
            print("\n")
        
        # Ejecución
        print("-----------------------------------------------------")
        pos2 = 0
        while pos2 < len(Lista_Lotes[pos]): 
            proceso = Lista_Lotes[pos][pos2]
            if proceso in Procesos_Terminados:
                pos2 += 1
                continue
            
            print("\n~ EJECUCIÓN ~\n")
            
            tiempo_restante = proceso[3]
            tiempo_transcurrido = 0
            
            while tiempo_restante >= 0:
                print("Nombre: ", proceso[0])
                print("ID: ", proceso[1])
                print("Operación: ", proceso[2])
                print("Tiempo Transcurrido: ", tiempo_transcurrido)
                print("Tiempo Restante: ", tiempo_restante)
                print("\n-- CONTADOR: ", global_counter)
                print("\n")
                time.sleep(1)
                
                global_counter += 1
                tiempo_transcurrido += 1
                tiempo_restante -= 1
            
            print("-----------------------------------------------------")
            
            #Procesos terminados
            Procesos_Terminados.append(proceso)
            
            print("\n~ PROCESOS TERMINADOS ~\n")
               
            for proceso in Procesos_Terminados:
                print("ID: ", proceso[1])
                print("Operación: ", proceso[2])
                print("Resultado: ", proceso[4], "\n")
                
                if (Procesos_Terminados.index(proceso) + 1) % dp == 0:
                    print("~~~~~~~~~~~~~")
            
            print("-----------------------------------------------------")
            
            # Actualiza y muestra el lote actual
            lote_actual = [x for x in Lista_Lotes[pos] if x not in Procesos_Terminados]
            if lote_actual:
                print("\nNo. de lotes pendientes: ", len(Lista_Lotes) - (pos + 1))
                print("\n~ LOTE ACTUAL ~\n")
                for x in lote_actual:
                    print("Nombre:", x[0])
                    print("Tiempo Máximo Estimado: ", x[3])
                    print("\n")
            print("-----------------------------------------------------")
            