import random
import tkinter as tk
from tkinter import scrolledtext

# Importar objeto de maquina de Turing creado
from DTM import dtm
# Importar automata celular que simula trafico en una red de nodos
from CellularAutomata import TrafficCellularAutomata
# Importar generador de ruta optima en el mapa de fusagasugá
from MapGenerator import OptimalRouteGeneratorMap


# Funcion para generar un string aleatorio de 0s y 1s con longitud aleatoria (máximo 12 caracteres)
def generar_string():
    longitud = random.randint(2, 12)
    return ''.join(random.choice(['0', '1']) for _ in range(longitud))

def show_transitions_in_window(transitions):
    # Crear la ventana de tkinter
    window = tk.Tk()
    window.title("Transiciones del DTM")

    # Crear un widget scrolledtext para mostrar el texto con barra de desplazamiento
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
    text_area.pack(pady=10, padx=10)

    # Iterar sobre las transiciones y escribirlas en el widget scrolledtext
    for state, transition_dict in transitions.items():
        text_area.insert(tk.END, f"Estado: {state}\n")
        for symbol, (next_state, write_symbol, move_direction) in transition_dict.items():
            text_area.insert(tk.END, f"  Con símbolo '{symbol}':\n")
            text_area.insert(tk.END, f"    Ir al estado: {next_state}\n")
            text_area.insert(tk.END, f"    Escribir en la cinta: {write_symbol}\n")
            text_area.insert(tk.END, f"    Dirección de movimiento: {move_direction}\n")
        text_area.insert(tk.END, "\n")  # Salto de línea entre estados

    # Configurar el text_area como de solo lectura
    text_area.configure(state='disabled')

    # Iniciar el bucle de eventos de tkinter
    window.mainloop()

# Generar un string de entrada aleatorio y probarlo paso a paso
input_str = generar_string()
print(f"Input string generado: {input_str}")

# ----- Procesar el string de entrada y determinar el resultado
#print(dtm.read_input(input_str))

cellularAutomata = TrafficCellularAutomata()
mapGenerator = OptimalRouteGeneratorMap()


# Numero de 1 y 0 que contiene el string
num_ceros = 0
num_unos = 0

for i in input_str:
    if i == '0':
        num_ceros += 1
    elif i == '1':
        num_unos += 1

pariedad_unos = num_unos % 2
pariedad_ceros = num_ceros % 2

# ------- Ejecución del Código
if __name__ == "__main__":
    if pariedad_unos == 0:
        print('String Aceptado')
        show_transitions_in_window(dtm.transitions)
        cellularAutomata.simulate(input_str)
        mapGenerator.generate_optimal_route(input_str)
    elif pariedad_ceros == 0:
        print('String Aceptado')
        show_transitions_in_window(dtm.transitions)
        cellularAutomata.simulate(input_str)
        mapGenerator.generate_optimal_route(input_str)
    else:
        print('String Rechazado')
