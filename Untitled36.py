#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import cos, sin, pi

# Números y colores en una ruleta europea
numeros_ruleta = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
colores_ruleta = ['green'] + ['black' if i % 2 == 0 else 'red' for i in range(1, 37)]

# Función para girar la ruleta
def girar_ruleta():
    return random.choice(numeros_ruleta)

# Función para mostrar la ruleta girando
def mostrar_ruleta(resultado):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    def init():
        ax.clear()
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        for i, num in enumerate(numeros_ruleta):
            angulo = 2 * pi * i / 37
            x = 1.2 * cos(angulo)
            y = 1.2 * sin(angulo)
            ax.text(x, y, str(num), horizontalalignment='center', verticalalignment='center',
                    fontsize=10, color='white' if colores_ruleta[i] == 'black' else 'black', 
                    bbox=dict(facecolor=colores_ruleta[i], edgecolor='none', boxstyle='round,pad=0.3'))
        plt.title('Ruleta de Casino')
        plt.axis('off')

    def update(frame):
        ax.clear()
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        current_angle = 2 * pi * frame / 37
        for i, num in enumerate(numeros_ruleta):
            angulo = 2 * pi * i / 37
            x = 1.2 * cos(angulo + current_angle)
            y = 1.2 * sin(angulo + current_angle)
            ax.text(x, y, str(num), horizontalalignment='center', verticalalignment='center',
                    fontsize=10, color='white' if colores_ruleta[i] == 'black' else 'black', 
                    bbox=dict(facecolor=colores_ruleta[i], edgecolor='none', boxstyle='round,pad=0.3'))
        
        angulo_res = 2 * pi * resultado / 37
        x_res = 1.4 * cos(angulo_res + current_angle)
        y_res = 1.4 * sin(angulo_res + current_angle)
        ax.arrow(0, 0, x_res, y_res, head_width=0.1, head_length=0.1, fc='yellow', ec='yellow')

    ani = animation.FuncAnimation(fig, update, frames=range(37), init_func=init, blit=False, repeat=False)
    plt.show()

# Función para apostar
def apostar(numero, cantidad):
    resultado = girar_ruleta()
    mostrar_ruleta(resultado)
    print(f"La ruleta giró y cayó en el número {resultado} ({colores_ruleta[numeros_ruleta.index(resultado)]}).")
    
    if numero == resultado:
        ganancia = cantidad * 35  # Ganancia de 35 a 1 si aciertas el número
        print(f"¡Felicidades! Ganaste {ganancia} unidades.")
        return ganancia
    else:
        print(f"Lo siento, perdiste {cantidad} unidades.")
        return -cantidad

# Función principal del juego
def jugar_ruleta():
    saldo = 1000  # Saldo inicial del jugador
    while True:
        print(f"\nTu saldo actual es: {saldo} unidades.")
        if saldo <= 0:
            print("Te has quedado sin saldo. ¡Gracias por jugar!")
            break
        
        try:
            numero_apuesta = int(input("Ingresa el número al que deseas apostar (0-36): "))
            cantidad_apuesta = int(input("Ingresa la cantidad que deseas apostar: "))
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número válido.")
            continue
        
        if numero_apuesta < 0 or numero_apuesta > 36:
            print("Número inválido. Por favor, ingresa un número entre 0 y 36.")
            continue
        if cantidad_apuesta > saldo:
            print("No tienes suficiente saldo para esa apuesta. Inténtalo de nuevo.")
            continue
        
        saldo += apostar(numero_apuesta, cantidad_apuesta)
        
        continuar = input("¿Deseas seguir jugando? (s/n): ").lower()
        if continuar != 's':
            print("Gracias por jugar. ¡Hasta la próxima!")
            break

# Iniciar el juego
jugar_ruleta()


# In[ ]:




