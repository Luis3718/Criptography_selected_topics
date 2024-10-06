"""
  Discrete logarithm problem and DHKE
  Instituto Polit�cnico Nacional
  ESCOM
  Alvarado Romero Luis Manuel   
  Materia: Ciptografia
  Grupo: 7CM1
"""
import secrets
import random
import math
from sympy import primerange
from sympy import isprime
from sympy import mod_inverse
from sympy import factorint
from math import isqrt
from collections import Counter


# Funcion para tomar un numero primo random
def generar_primo_dos_digitos():
  primos = list(primerange(11, 100))  # Genera una lista de todos los primos de 2 dígitos
  return random.choice(primos)  

# Definimmos la funcion basada en el algoritmo extendido de euclides para calcular el inverso multiplicativo
def Xgcd(a,n):
  u,v=a,n
  x1=1 
  x2=0
  while u!=1:
    q=math.floor(v/u)
    r=v-q*u
    x=x2-q*x1
    v=u
    u=r
    x2=x1
    x1=x
  res = x1%n
  return(res)

# Funcion que calcula los residuos cuadraticos de Zp
def Quadratic_Recsidues(Prime):
  Elementos=[]
  Residue=[]
  QR=[]
  Square_roots={}
  #print(f"El numero primo es: {Prime}")
  for i in range(1,Prime):
    Elementos.append(i)
  print(f"Zp={Elementos}")

  # Calcula los residuos cuadraticos y los agrega a un diccionario de sus raices
  for i in Elementos:
    y_squared=(i*i)%Prime
    if y_squared in Square_roots:
      Square_roots[y_squared].append(i)
    else:
      Square_roots[y_squared]=[i]
    Residue.append(y_squared)
    
  # Contar las ocurrencias de cada residuo cuadratico
  contador = Counter(Residue)
  for i in contador:
    if contador[i]>1:
      QR.append(i)
  print(f"Los QR son: {QR}")
  print(f"Las raices son: {Square_roots}")
  return Square_roots

# Funcion para validar a las variables a y b
def Validar(a,b,Prime):
  res=(4*((a)**3) + 27*((b)**2))%Prime
  if res>0 and a<Prime and b<Prime:
    return True
  else:
    return False

# Funcion para calcular los resultados de la curva eliptica
def Eliptic_curves_function(a,b,Prime):
  Elementos=[]
  Resultados=[]
  if Validar(a,b,Prime):
    for i in range(Prime):
      Elementos.append(i)
    for i in Elementos:
      res=((i)**3+a*(i)+b)%Prime
      Resultados.append(res)
    #print(f"\nResultado de X^3 + {a}*X + {b}: {Resultados}")
  else:
    print("Ingrese variables a y b validas")
  return Resultados

# Funcion que calcula todos los puntos de una curba eliptica
def Encontrar_puntos(a,b,Prime):
  Square_roots={}
  Resultados=[]
  Puntos=[]
  Square_roots=Quadratic_Recsidues(Prime)
  Resultados=Eliptic_curves_function(a,b,Prime)
  cont=0
  for i in Resultados:
    if i==0: # caso para raiz 0
      Puntos.append(cont)
      Puntos.append(i)
      Puntos.append(1)
    for j in Square_roots:
      if i==j: # caso de buscar en residuos cuadraticos
        for k in Square_roots[j]:
          Puntos.append(cont)
          Puntos.append(k)
          Puntos.append(1)
    cont+=1

# Funcion que nos permite ingresar coordenadas de un punto a un arreglo
def Ingresar_punto():
  Punto=[]
  print("Ingresa las coordenadas del punto: ")
  x=int(input("Ingresa la coordenda X:"))
  y=int(input("Ingresa la coordenda Y:"))
  z=int(input("Ingresa la coordenda Z:"))
  Punto.append(x)
  Punto.append(y)  
  Punto.append(z)
  print(f"Punto: {Punto}") 
  return Punto 

# Funcion que evalua si un punto esta dentro de la curva eliptica
def Verificar_punto(a,b,Prime,Punto,Puntos):
  longitud_punto=len(Punto)
  for i in range(0,len(Puntos),3):
    if Puntos[i:i+longitud_punto] == Punto:
      return True

# Funcion que realiza la suma de puntos
def Suma_punto(a,b,Primo,PuntoP,PuntoQ,Puntos):
  if Verificar_punto(a,b,Primo,PuntoP,Puntos)==True and Verificar_punto(a,b,Primo,PuntoQ,Puntos)==True:
    Res=[]
    x1=PuntoP[0]
    x2=PuntoQ[0]
    y1=PuntoP[1]
    y2=PuntoQ[1]
    print(f"Valores de x: {x1,x2}")
    print(f"Valores de y: {y1,y2}")
    if x1==x2:
      y1=-y1
      print(f"y1= {y1}")
      y1=y1%Primo
      Res.append(x1)
      Res.append(y1)
      Res.append(1)
      print(f"P+Q= {Res}")
      return Res
    num=(x2-x1)%Primo
    print(num)
    if num==0:
      # Esto es un caso que debo de checar
      inv=0
    else: 
      inv=Xgcd(num,Primo)
      s= ((y2-y1)*(inv))%Primo
      print(f"S= {s}")
      x3=((s**2)-x1-x2)%Primo
      y3=(s*(x1-x3)-y1)%Primo
      Res.append(x3)
      Res.append(y3)
      Res.append(1)
      print(f"P+Q= {Res}")
      return Res

# Funcion que realiza el doblado de punto 
def Doblado_punto(a,b,Primo,PuntoP,Puntos):
  if Verificar_punto(a,b,Primo,PuntoP,Puntos)==True :
    Res=[]
    x1=PuntoP[0]
    y1=PuntoP[1]
    print(f"Valores de x: {x1}")
    print(f"Valores de y: {y1}")
    num=2*y1
    if num==0:
      # Esto es un caso que debo de checar
      inv=0
    else: 
      inv=Xgcd(num,Primo)
    s= ((3*(x1**2)+a)*(inv))%Primo
    print(f"S= {s}")
    x3=((s**2)-x1-x1)%Primo
    y3=(s*(x1-x3)-y1)%Primo
    Res.append(+x3)
    Res.append(y3)
    Res.append(1)
    print(f"2P= {Res}")
    return Res

# Funcion para resolver el problema del logaritmo discreto
def baby_step_giant_step(g, h, p):
    # Paso 1: Calcular m = ⌈√p⌉
    m = isqrt(p) + 1
    # Paso 2: Baby-step (calcular g^j mod p para j = 0, 1, ..., m-1)
    baby_steps = {}
    for j in range(m):
        value = pow(g, j, p)
        baby_steps[value] = j
    # Paso 3: Giant-step (calcular h * (g^(-m))^i mod p para i = 0, 1, ..., m-1)
    g_m_inv = mod_inverse(pow(g, m, p), p)  # Calcula g^(-m) mod p
    current = h
    for i in range(m):
        if current in baby_steps:
            # Si se encuentra una coincidencia, devuelve el valor x = i * m + j
            return i * m + baby_steps[current]
        current = (current * g_m_inv) % p  # Actualiza el valor de h * (g^(-m))^i mod p

    return None  # Si no se encuentra ninguna solución

# Funcion para buscar k en un punto en los resultados generados
def Buscar_k(Punto,Puntos):
  cont=1
  for i in Puntos:
    print(i)
    if i==Punto:
      return cont
    cont+=1

# Función que genera un número primo de 1024 bits
def generar_primo_grande(bits):
    while True:
        numero = secrets.randbits(bits)
        if isprime(numero):
            return numero

# Función que encuentra un generador para el grupo multiplicativo Z_p*
def encontrar_generador(p):
    # Factorizamos p-1
    factores = factorint(p - 1)
    # Probamos diferentes valores de g
    for g in range(2, p):
        es_generador = True
        # Para cada factor q de p-1, comprobamos que g^((p-1)/q) != 1 (mod p)
        for q in factores:
            if pow(g, (p-1)//q, p) == 1:
                es_generador = False
                break 
        # Si es un generador válido, lo devolvemos
        if es_generador:
            return g

# Exponenciación modular rápida (binaria)
def exponenciacion_modular(base, exponente, modulo):
  resultado = 1
  base = base % modulo  
  while exponente > 0:
    # Si el exponente es impar, multiplicamos el resultado actual por la base
    if exponente % 2 == 1:
        resultado = (resultado * base) % modulo
    # El exponente se divide entre 2 (lo desplazamos a la derecha)
    exponente = exponente // 2
    # La base se eleva al cuadrado (mod n)
    base = (base * base) % modulo 
  return resultado

# Funcion de Diffie Hellman para generar A
def DH_GeneraraA(Primo,Generador,X):
  res=exponenciacion_modular(Generador,X,Primo)
  print(f"{Generador}^X mod {Primo}={res}")
  return res

# Funcion de Diffie Hellman para generar el secreto compartido
def DH_EncontrarSecretoCompartido(B,X,Primo):
  res=exponenciacion_modular(B,X,Primo)
  print(f"{B}^X mod {Primo}={res}")
  return res

def opcion_1():
  Primo=int(input("Ingresa el numero primo: "))
  generador=int(input("Ingresa el numero generador: "))
  beta=int(input("Ingresa el beta: "))
  if generador>Primo and generador<=0 and beta>Primo and beta<=0:
    print("Valores no validos")
    return 0
  else: 
    x=baby_step_giant_step(generador,beta,Primo)
    print(f"El valor de x es: {x}")
    print(f"{generador}^{x} mod {Primo} = {beta}")
    res=exponenciacion_modular(generador,x,Primo)
    print(f"Comrpobacion: {res}")

def opcion_2():
  Puntos=[]
  Generador=[]
  Resultados=[]
  Primo=int(input("Ingresa el numero primo: "))
  a=int(input("Ingresa la variable a: "))
  b=int(input("Ingresa la variable b: "))
  Puntos=Encontrar_puntos(a,b,Primo)
  Cardinalidad=int((len(Puntos)/3))
  print(Cardinalidad)
  print("Ingresa tu punto generador: ")
  Generador=Ingresar_punto()
  print("Ingresa tu punto beta: ")
  beta=Ingresar_punto()
  for i in range(0,Cardinalidad-1,1):
    print(f"\nCalculando {i+1}G \n")
    if i==0:
      PuntoP=Generador
      Resultados.append(PuntoP)
    elif i==1:
      PuntoP=Doblado_punto(a,b,Primo,Generador,Puntos)
      Resultados.append(PuntoP)
    else:
      PuntoP=Suma_punto(a,b,Primo,PuntoP,Generador,Puntos)
      Resultados.append(PuntoP)
    print(PuntoP)
  Punto_infinito=[0,1,0]
  Resultados.append(Punto_infinito)
  k=Buscar_k(beta,Resultados)
  print(f"K={k}")


def opcion_3():
  res=input("¿Tienes un numero pirmo? ")
  if res=='Si' or res=='si':
    Primo=int(input("Ingresa el numero primo: "))
  else:
    Primo=generar_primo_grande(50)
    print(f"El primo es: {Primo}")
  res2=input("¿Tienes un numero generador? ")
  if res2=='Si' or res2=='si':
    Generador=int(input("Ingresa el numero generador: "))
  else:
    Generador=encontrar_generador(Primo)
    print(f"El generador es: {Generador}")
  res3=input("¿Tienes un exponente secreto? ")
  if res3=='Si' or res3=='si':
    Exponente=int(input("Ingresa el exponente secreto: "))
  else:
    Exponente=random.randint(2, Primo)
    print(f"El exponente es: {Exponente}")
  A=DH_GeneraraA(Primo,Generador,Exponente)
  B=int(input("Ingresa el valor de B: "))
  Secreto=DH_EncontrarSecretoCompartido(B,Exponente,Primo)

def salir():
    print("Saliendo del programa...")
    exit()

def main():
    
  opciones = {
    '1': opcion_1,
    '2': opcion_2,
    '3': opcion_3,
    '4': salir
}

  while True:
    print("\n Menú:")
    print("1. Discrete logarithm problem")
    print("2. Discrete logarithm problem on Eliptic curves")
    print("3. DH Key exchange")
    print("4. Salir\n")
    seleccion = input("Selecciona una opción: ")

    if seleccion in opciones:
      opciones[seleccion]()
    else:
      print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
