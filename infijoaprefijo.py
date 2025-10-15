# Conversión infijo -> prefijo mostrando subexpresiones entre paréntesis
# Soporta números multi-dígito y nombres de variables alfanuméricos

prioridad = {
    '+' : 1,
    '-' : 1,
    '*' : 2,
    '/' : 2,
    '^' : 3
}
# asociatividad (True = derecha, False = izquierda)
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
            # número (enteros o decimales)
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        if c.isalpha() or c == '_':
            # variable / identificador (alfanumérico y guiones bajos)
            j = i
            while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        # operador o paréntesis
        tokens.append(c)
        i += 1
    return tokens

def infix_to_postfix(tokens):
    out = []
    ops = []
    for t in tokens:
        if t.isalnum() or (t.replace('.','',1).isdigit()):  # operandos: números o identificadores
            out.append(t)
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            if not ops:
                raise ValueError("Paréntesis desbalanceados")
            ops.pop()  # quitar '('
        else:  # operador
            while (ops and ops[-1] != '(' and
                   ((t in derecha and prioridad.get(t,0) < prioridad.get(ops[-1],0)) or
                    (t not in derecha and prioridad.get(t,0) <= prioridad.get(ops[-1],0)))):
                out.append(ops.pop())
            ops.append(t)
    while ops:
        if ops[-1] in ('(',')'):
            raise ValueError("Paréntesis desbalanceados")
        out.append(ops.pop())
    return out

def postfix_to_prefixed_with_parens(postfix):
    stack = []
    for tok in postfix:
        if tok.isalnum() or (tok.replace('.','',1).isdigit()):
            stack.append(tok)
        else:  # operador
            if len(stack) < 2:
                raise ValueError("Expresión inválida")
            b = stack.pop()
            a = stack.pop()
            # formamos subexpresión prefija con paréntesis
            stack.append(f"({tok} {a} {b})")
    if len(stack) != 1:
        raise ValueError("Expresión inválida")
    res = stack[0]
    # quitar paréntesis exteriores si abarcan toda la expresión
    if res.startswith('(') and res.endswith(')'):
        # verificar que quitar los extremos deja paréntesis balanceados
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
            return inner  # sin paréntesis exteriores
    return res

def infija_a_prefija_con_parentesis(expr):
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    pref = postfix_to_prefixed_with_parens(postfix)
    return pref

# Ejemplos
expresion = input("Ingrese una expresión infija: ")
try:
    prefija = infija_a_prefija_con_parentesis(expresion)
    print("Infijo: ", expresion)
    print("Prefijo:", prefija)
except Exception as e:
    print("Error:", e)


import subprocess

# Declaramos el contenido del script bash como texto
cmd = f'sbcl --script evaluate.lisp "({prefija})"'
subprocess.run(cmd, shell=True)