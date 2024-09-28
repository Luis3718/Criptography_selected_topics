"""
  Group operations on eliptic curves
  Instituto Polit�cnico Nacional
  ESCOM
  Alvarado Romero Luis Manuel   
  Materia: Ciptografia
  Grupo: 7CM1
"""
from sympy import primerange
import random
import math
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
  print(f"El numero primo es: {Prime}")
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
  if res>0 & a<Prime & b<Prime:
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
    print(f"\nResultado de X^3 + {a}*X + {b}: {Resultados}")
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
  for i in Square_roots:
    cont=0
    for j in Resultados:
      if j==0:
        Puntos.append(cont)
        Puntos.append(j)
        Puntos.append(1)
      if j==i:
        print(f"x:{cont} y1,y2:{Square_roots[j]}")
        for k in Square_roots[j]:
          Puntos.append(cont)
          Puntos.append(k)
          Puntos.append(1)
      cont+=1
  # Utilizamos estos digitos como referencia al punto al infinito
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
  z=int(input("Ingresa la coordenda Z:"))
  Punto.append(x)
  Punto.append(y)  
  Punto.append(z)
  print(f"Punto: {Punto}") 
  return Punto 

# Funcion que evalua si un punto esta dentro de la curva eliptica
def Verificar_punto(a,b,Prime,Punto):
  Puntos=Encontrar_puntos(a,b,Prime)
  longitud_punto=len(Punto)
  for i in range(0,len(Puntos),3):
    if Puntos[i:i+longitud_punto] == Punto:
      return True

def opcion_1():
  res=input("¿Tienes un numero pirmo? ")
  if res=='Si' or res=='si':
    Primo=int(input("Ingresa el numero primo: "))
  else:
    Primo=generar_primo_dos_digitos()
  print(f"El numero primo es {Primo}")
  res=input("¿Tienes las variables a y b? ")
  if res=='Si' or res=='si':
    a=int(input("Ingresa la variable a: "))
    b=int(input("Ingresa la variable b: "))
  else: 
    a=random.randint(1, Primo)
    b=random.randint(1, Primo)
  Punto=Ingresar_punto()
  if Verificar_punto(a,b,Primo,Punto)==True:
    print("El punto se encuentra en la curva")
  else: 
    print("El punto no se encunetra en la curva")

def opcion_2():
  res=input("¿Tienes un numero pirmo? ")
  if res=='Si' or res=='si':
    Primo=int(input("Ingresa el numero primo: "))
  else:
    Primo=generar_primo_dos_digitos()
  print(f"El numero primo es {Primo}")
  res=input("¿Tienes las variables a y b? ")
  if res=='Si' or res=='si':
    a=int(input("Ingresa la variable a: "))
    b=int(input("Ingresa la variable b: "))
  else: 
    a=random.randint(1, Primo)
    b=random.randint(1, Primo)
  Punto=Ingresar_punto()
  if Verificar_punto(a,b,Primo,Punto)==True:
    PuntoN=[]
    cont=0
    for i in Punto:
      if cont==1:
        i=-i
        i=i%Primo
      PuntoN.append(i)
      cont+=1
    print(f"-P= {PuntoN}")
    return PuntoN
  else:
    print("punto no valido")

def opcion_3():
  res=input("¿Tienes un numero pirmo? ")
  if res=='Si' or res=='si':
    Primo=int(input("Ingresa el numero primo: "))
  else:
    Primo=generar_primo_dos_digitos()
  print(f"El numero primo es {Primo}")
  res=input("¿Tienes las variables a y b? ")
  if res=='Si' or res=='si':
    a=int(input("Ingresa la variable a: "))
    b=int(input("Ingresa la variable b: "))
  else: 
    a=random.randint(1, Primo)
    b=random.randint(1, Primo)
  PuntoP=Ingresar_punto()
  PuntoQ=Ingresar_punto()
  if Verificar_punto(a,b,Primo,PuntoP)==True and Verificar_punto(a,b,Primo,PuntoQ)==True:
    Res=[]
    x1=PuntoP[0]
    x2=PuntoQ[0]
    y1=PuntoP[1]
    y2=PuntoQ[1]
    print(f"Valores de x: {x1,x2}")
    print(f"Valores de y: {y1,y2}")
    num=x2-x1
    print(num)
    if x1==x2:
      y1=-y1
      print(f"y1= {y1}")
      y1=y1%Primo
      Res.append(x1)
      Res.append(y1)
      Res.append(1)
      print(f"P+Q= {Res}")
      return Res
    elif num==0:
      # Ponemos el inverso en 0 ya que si no da error
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

def opcion_4():
  res=input("¿Tienes un numero pirmo? ")
  if res=='Si' or res=='si':
    Primo=int(input("Ingresa el numero primo: "))
  else:
    Primo=generar_primo_dos_digitos()
  print(f"El numero primo es {Primo}")
  res=input("¿Tienes las variables a y b? ")
  if res=='Si' or res=='si':
    a=int(input("Ingresa la variable a: "))
    b=int(input("Ingresa la variable b: "))
  else: 
    a=random.randint(1, Primo)
    b=random.randint(1, Primo)
  PuntoP=Ingresar_punto()
  if Verificar_punto(a,b,Primo,PuntoP)==True :
    Res=[]
    x1=PuntoP[0]
    y1=PuntoP[1]
    print(f"Valores de x: {x1}")
    print(f"Valores de y: {y1}")
    num=2*y1
    if num==0:
      # Ponemos esto en 0 ya que si no da error
      inv=0
    else: 
      inv=Xgcd(num,Primo)
    s= ((3*(x1**2)+a)*(inv))%Primo
    print(f"S= {s}")
    x3=((s**2)-x1)%Primo
    y3=(s*(x1-x3)-y1)%Primo
    Res.append(x3)
    Res.append(y3)
    Res.append(1)
    print(f"2P= {Res}")
    return Res

def salir():
    print("Saliendo del programa...")
    exit()

def main():
    
  opciones = {
    '1': opcion_1,
    '2': opcion_2,
    '3': opcion_3,
    '4': opcion_4,
    '5': salir
}

  while True:
    print("\n Menú:")
    print("1. Verificar un punto en la curva")
    print("2. Calcular -P de un Punto")
    print("3. Suma de 2 puntos P y Q")
    print("4. Suma de 2 puntos P")
    print("5. Salir\n")
    seleccion = input("Selecciona una opción: ")

    if seleccion in opciones:
      opciones[seleccion]()
    else:
      print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
