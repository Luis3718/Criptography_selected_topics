"""
  ECDSA
  Instituto Polit�cnico Nacional
  ESCOM
  Alvarado Romero Luis Manuel   
  Materia: Ciptografia
  Grupo: 7CM1
"""
import secrets
import random
import ast
import math
from sympy import primerange
from sympy import isprime
from Crypto.Util.number import inverse
from collections import Counter

Ruta = "Practica5/"

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
    print("Suma punto")
    print(f"Valores de x: {x1,x2}")
    print(f"Valores de y: {y1,y2}")
    if x1==x2:
      y1=-y1
      print(f"y1= {y1}")
      y1=y1%Primo
      Res.append(x1)
      Res.append(y1)
      Res.append(1)
      print(f"P+Q= {Res} \n")
      return Res
    num=(x2-x1)%Primo
    if num==0:
      inv=0
    else: 
      inv=inverse(num,Primo)
    s= ((y2-y1)*(inv))%Primo
    x3=((s**2)-x1-x2)%Primo
    y3=(s*(x1-x3)-y1)%Primo
    Res.append(x3)
    Res.append(y3)
    Res.append(1)
    print(f"P+Q= {Res} \n")
    return Res

# Funcion que realiza el doblado de punto 
def Doblado_punto(a,b,Primo,PuntoP,Puntos):
  #if Verificar_punto(a,b,Primo,PuntoP,Puntos)==True :
    Res=[]
    x1=PuntoP[0]
    y1=PuntoP[1]
    print("Doblado de punto")
    print(f"Valores de x: {x1}")
    print(f"Valores de y: {y1}")
    num=2*y1
    if num==0:
      # Esto es un caso que debo de checar
      inv=0
    else: 
      inv=inverse(num,Primo)
    s= ((3*(x1**2)+a)*(inv))%Primo
    x3=((s**2)-x1-x1)%Primo
    y3=(s*(x1-x3)-y1)%Primo
    Res.append(+x3)
    Res.append(y3)
    Res.append(1)
    print(f"2P= {Res}\n")
    return Res

# Funcion que nos permite realizar DHKE con curvas elipticas
def ECDH(Primo,a,b,Ka,Generador,Puntos):
  Resultados=[]
  Ka=Ka%Primo
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
  return Resultados[Ka-1]

# Funcion que permite ingresarlos parametros del protocolo ECDSA
def Public_Parameters_ECDSA():
  Primo=int(input("Ingresa el numero primo: "))
  a=int(input("Ingresa la variable a: "))
  b=int(input("Ingresa la variable b: "))
  Puntos=Encontrar_puntos(a,b,Primo)
  Cardinalidad=int((len(Puntos)/3))
  print(f"|E(a,b)|= {Cardinalidad}")
  print("Ingresa tu punto generador: ")
  Generador=Ingresar_punto()
  Orden=int(input("Ingrese el orden del generador (q): "))
  return Primo,a,b,Puntos,Generador,Orden

# Funcion que genera las llaves de ECDSA
def Generate_Keys_ECDSA(Primo,a,b,Puntos,Generador,Orden):
  d=random.randint(0, Orden)
  B=ECDH(Primo,a,b,d,Generador,Puntos)
  Public_key = (Primo, a, b, Orden, Generador, B)
  with open(Ruta+"Llave_publica.txt", 'w+') as archivo:
    archivo.write(str(Public_key))
  return d

# Funcion que firma el mensaje con ECDSA
def Signature_ECDSA(Primo,a,b,Orden,Generador,Puntos,Mensaje,Private_key):
  Ke=random.randint(0, Orden)
  print(f"La llave efimera es: {Ke}")
  R=ECDH(Primo,a,b,Ke,Generador,Puntos)
  print(f"R={R}")
  r=R[0]
  print(f"r={r}")
  InvKe=inverse(Ke,Orden)
  print(InvKe)
  mitad=(Private_key*r)
  s=((Mensaje+mitad)*InvKe)%Orden
  Signature=(r,s)
  with open(Ruta+"Firma.txt", 'w+') as archivo:
    archivo.write(str(Signature))
  return Signature

# Funcion que verifica una firma con ECDSA
def Verification_ECDSA(Mensaje,Nombre_archivo,Firma):
  # Leer el archivo y convertirlo a una tupla
  with open(Ruta+Nombre_archivo, "r") as file:
      llave_publica = file.read()
  with open(Ruta+Firma, "r") as file:
      firma = file.read()
  # Convertir el contenido a una tupla
  public_key = ast.literal_eval(llave_publica)
  firma = ast.literal_eval(firma)
  print("Llave pública leída:", public_key)
  print("Firma:", firma)
  print(f"Mensaje: {Mensaje}")
  # Extraer los elementos de la tupla llave publica y firma
  Primo=int(public_key[0])
  a=int(public_key[1])
  b=int(public_key[2])
  Puntos=Encontrar_puntos(a,b,Primo)
  q=int(public_key[3])
  print(f"q={q}")
  A=(public_key[4])
  print(f"A={A}")
  B=(public_key[5])
  print(f"B={B}")
  r=int(firma[0])
  print(f"r= {r}")
  s=int(firma[1])
  print(f"s= {s}")
  # Encontrar inversos multiplicativos
  if s==0:
    w=0
    print(f"W= {w}")
  else:
    w=inverse(s,q)
    print(f"W= {w}") 
  u1=(w*Mensaje)%q
  u2=(w*r)%q
  print(f"u1={u1} u2={u2}\n")
  # Casos de U1 y U2
  if u1==0 and u2==0:
    P=[0,0] 
    print(f"P={P}")
  elif u1>0 and u2<=0:
    Primer_parte=ECDH(Primo,a,b,u1,A,Puntos)
    P=Primer_parte
    print(f"P={P}")
  elif u1<=0 and u2>0:
    Segunda_parte=ECDH(Primo,a,b,u2,B,Puntos)
    P=Segunda_parte
    print(f"P={P}")
  else: 
    Primer_parte=ECDH(Primo,a,b,u1,A,Puntos)
    Segunda_parte=ECDH(Primo,a,b,u2,B,Puntos)
    P=Suma_punto(a,b,Primo,Primer_parte,Segunda_parte,Puntos)  
    print(f"P={P}")
  xp=P[0]
  print(f"Xp={xp}")
  print(f"r={r}")
  if xp==r:
    return True
  else:
    return False
  
def opcion_1():
  Primo,a,b,Puntos,Generador,Orden=Public_Parameters_ECDSA()  
  Private_key=Generate_Keys_ECDSA(Primo,a,b,Puntos,Generador,Orden)
  print(f"La llave privada es {Private_key}\n")
  Mensaje=int(input("Ingresa el mensaje: "))
  Firma=Signature_ECDSA(Primo,a,b,Orden,Generador,Puntos,Mensaje,Private_key)
  print(Firma)

def opcion_2():
  Mensaje=int(input("Ingresa el mensaje: "))
  Ver=Verification_ECDSA(Mensaje,"clave_publica.txt","Firma.txt") 
  if Ver==True:
    print("Firma valida")
  else: 
    print("Firma no valida")

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
    print("1. Generacion de llaves y firma ECDSA")
    print("2. Verificacion de firma ECDSA")
    print("3. Salir\n")
    seleccion = input("Selecciona una opción: ")

    if seleccion in opciones:
      opciones[seleccion]()
    else:
      print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
