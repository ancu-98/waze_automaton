from automata.tm.dtm import DTM

# DTM que
'''
Turing Machine
- Q → Conjunto de todos los estados no vacío
- Σ → (Sigma) Conjunto de símbolos de entrada no vacío
- τ → (Tau) Es un conjunto no vacío de símbolos de la cinta
- δ → (Delta) Es la función de transición
- q0 → Es el estado inicial
- b → Es el símbolo en blanco
- F → Conjunto de Estados Finales
'''

# ----- Definir la máquina de Turing con 12 estados
dtm = DTM(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'ACCEPT', 'REJECT'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    transitions={
        # Estado inicial q0, aquí comenzamos la verificación del string
       'q0': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
        # Estados q1 a q10, seguimos evaluando la paridad de 0s y 1s
       'q1': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q2': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q3': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q4': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q5': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q6': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q7': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q8': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q9': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       'q10': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('REJECT', '.', 'R')
        },
       # Estado q11 verifica y decide si acepta o rechaza según la paridad del string
        'q11': {
            '0': ('ACCEPT', '0', 'R'),  # Paridad de 0s y 1s
            '1': ('ACCEPT', '1', 'R'),
            '.': ('REJECT', '.', 'R')  # Si no es par
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'ACCEPT', 'REJECT'}
)