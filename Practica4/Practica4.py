"""
  Group operations on eliptic curves
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
      primer=pow(i,3)
      segundo=a*i
      res=(primer+segundo+b)%Prime
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
  
  # Punto al infinito
  Puntos.append(0)
  Puntos.append(1)
  Puntos.append(0)
  
  print("\nPuntos de la curva: ")
  for i in range(0,len(Puntos),3):
    print(f"({Puntos[i]},{Puntos[i+1]},{Puntos[i+2]})")
  
  return Puntos

# Funcion que nos permite ingresar coordenadas de un punto a un arreglo
def Ingresar_punto():
  Punto=[]
  print("Ingresa las coordenadas del punto: ")
  x=int(input("Ingresa la coordenda X:"))
  y=int(input("Ingresa la coordenda Y:"))
  z=1
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
  #if Verificar_punto(a,b,Primo,PuntoP,Puntos)==True and Verificar_punto(a,b,Primo,PuntoQ,Puntos)==True:
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
  #if Verificar_punto(a,b,Primo,PuntoP,Puntos)==True :
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

# Funcion que nos permite realizar DHKE con curvas elipticas
def ECDH(Primo,a,b,Ka,Generador,Puntos):
  Resultados=[]
  for i in range(Ka):
    # Caso 1G
    if i==0: 
      PuntoP=Generador
      Resultados.append(PuntoP)
    # Caso 2G
    elif i==1:
      PuntoP=Doblado_punto(a,b,Primo,Generador,Puntos)
      Resultados.append(PuntoP)
    # Caso NG
    else:
      PuntoP=Suma_punto(a,b,Primo,PuntoP,Generador,Puntos)
      Resultados.append(PuntoP)
    print(PuntoP)
  return Resultados[Ka-1]

def opcion_1():
  Primo=int(input("Ingresa el numero primo: "))
  a=int(input("Ingresa la variable a: "))
  b=int(input("Ingresa la variable b: "))
  Puntos=Encontrar_puntos(a,b,Primo)
  Cardinalidad=int((len(Puntos)/3))
  print(f"|E(a,b)|= {Cardinalidad}")
  print("Ingresa tu punto generador: ")
  Generador=Ingresar_punto()
  while True:
    ka=int(input("Ingresa tu Ka: "))
    if ka>=2 and ka<=Cardinalidad-1:
      break
    else:
      print("Ingresa un Ka valido")
  A=ECDH(Primo,a,b,ka,Generador,Puntos)
  print(f"El valor de {ka}*{Generador} = {A}")

def opcion_2():
  Primo=int(input("Ingresa el numero primo: "))
  a=int(input("Ingresa la variable a: "))
  b=int(input("Ingresa la variable b: "))
  Puntos=Encontrar_puntos(a,b,Primo)
  Cardinalidad=int((len(Puntos)/3))
  print(f"|E(a,b)|= {Cardinalidad}")
  print("Ingresa tu punto generador: ")
  Generador=Ingresar_punto()
  while True:
    ka=int(input("Ingresa tu Ka: "))
    if ka>=2 and ka<=Cardinalidad-1:
      break
    else:
      print("Ingresa un Ka valido")
  A=ECDH(Primo,a,b,ka,Generador,Puntos)
  print(f"El valor de ka*{Generador} = {A}")
  B=Ingresar_punto()
  Secreto_compartido=ECDH(Primo,a,b,ka,B,Puntos)
  print(f"El secreto compartido de ka*{B} = {Secreto_compartido}")

def salir():
    print("Saliendo del programa...")
    exit()

def main():
    
  opciones = {
    '1': opcion_1,
    '2': opcion_2,
    '3': salir
}

  while True:
    print("\n Menú:")
    print("1. DHKE with elliptic curves")
    print("2. Simulacion DHKE with elliptic curves")
    print("3. Salir\n")
    seleccion = input("Selecciona una opción: ")

    if seleccion in opciones:
      opciones[seleccion]()
    else:
      print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
