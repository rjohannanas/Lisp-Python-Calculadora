import subprocess
import sys
import os

# Prioridad y asociatividad
prioridad = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
derecha = {'^'}

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or (c == '.' and i+1 < len(expr) and expr[i+1].isdigit()):
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        if c.isalpha() or c == '_':
            j = i
            while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        tokens.append(c)
        i += 1
    return tokens

def infix_to_postfix(tokens):
    out, ops = [], []
    for t in tokens:
        if t.isalnum() or t.replace('.', '', 1).isdigit():
            out.append(t)
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            if not ops:
                raise ValueError("Paréntesis desbalanceados")
            ops.pop()
        else:
            while (ops and ops[-1] != '(' and
                   ((t in derecha and prioridad[t] < prioridad[ops[-1]]) or
                    (t not in derecha and prioridad[t] <= prioridad[ops[-1]]))):
                out.append(ops.pop())
            ops.append(t)
    while ops:
        if ops[-1] in ('(', ')'):
            raise ValueError("Paréntesis desbalanceados")
        out.append(ops.pop())
    return out

def postfix_to_prefixed_with_parens(postfix):
    stack = []
    for tok in postfix:
        if tok.isalnum() or tok.replace('.', '', 1).isdigit():
            stack.append(tok)
        else:
            if len(stack) < 2:
                raise ValueError("Expresión inválida")
            b = stack.pop()
            a = stack.pop()
            stack.append(f"({tok} {a} {b})")
    if len(stack) != 1:
        raise ValueError("Expresión inválida")
    res = stack[0]
    if res.startswith('(') and res.endswith(')'):
        inner = res[1:-1]
        bal = 0
        ok = True
        for ch in inner:
            if ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
            if bal < 0:
                ok = False
                break
        if ok and bal == 0:
            return inner
    return res

def infija_a_prefija_con_parentesis(expr):
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    return postfix_to_prefixed_with_parens(postfix)

def obtener_ruta_absoluta_archivo(nombre):
    if getattr(sys, 'frozen', False):
        ruta_base = sys._MEIPASS
    else:
        ruta_base = os.path.dirname(__file__)
    return os.path.join(ruta_base, nombre)

# Programa principal con bucle
if __name__ == "__main__":
    print("=== Conversor infijo → prefijo con ejecución en Lisp ===")
    print("Escribe 'exit' para salir.\n")

    while True:
        expresion = input("Ingrese una expresión infija: ").strip()
        if expresion.lower() == "exit":
            print("Saliendo del programa...")
            break

        try:
            prefija = infija_a_prefija_con_parentesis(expresion)
            print("Infijo: ", expresion)
            print("Prefijo:", prefija)

            ruta_lisp = obtener_ruta_absoluta_archivo("evaluate.lisp")
            cmd = f'sbcl --script "{ruta_lisp}" "({prefija})"'
            subprocess.run(cmd, shell=True)

        except Exception as e:
            print("Error:", e)

        print()  # Línea en blanco antes de la siguiente iteración