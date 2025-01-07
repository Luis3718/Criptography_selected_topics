"""
  Points in an elliptic curve algorithm
  Instituto Polit�cnico Nacional
  ESCOM
  Alvarado Romero Luis Manuel   
  Materia: Ciptografia
  Grupo: 7CM1
"""
from sympy import primerange
import random
from collections import Counter

# Funcion para tomar un numero primo random
def generar_primo_dos_digitos():
  primos = list(primerange(11, 100))  # Genera una lista de todos los primos de 2 dígitos
  return random.choice(primos)  

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
  
def opcion_1():
  res=input("¿Tienes un numero pirmo? ")
  if res=='Si' or res=='si':
    Primo=int(input("Ingresa el numero primo: "))
    Quadratic_Recsidues(Primo)
  else: 
    Primo=generar_primo_dos_digitos()  
    Quadratic_Recsidues(Primo)

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
    Eliptic_curves_function(a,b,Primo)
  else: 
    a=random.randint(1, Primo)
    b=random.randint(1, Primo)
    Eliptic_curves_function(a,b,Primo)

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
    Encontrar_puntos(a,b,Primo)
  else: 
    a=random.randint(1, Primo)
    b=random.randint(1, Primo)
    Encontrar_puntos(a,b,Primo)

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
    print("1. Encontrar los residuos cuadraticos y las raices de un numero primo")
    print("2. Encontrar los resultados de una funcion de curva eliptica")
    print("3. Encontrar los puntos dentro de una funcion de curva eliptica")
    print("4. Salir\n")
    seleccion = input("Selecciona una opción: ")

    if seleccion in opciones:
      opciones[seleccion]()
    else:
      print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
