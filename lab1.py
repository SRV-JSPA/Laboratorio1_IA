import csv
from collections import deque
import heapq

class Node:
    def __init__(self, nombre, heuristica):
        self.nombre = nombre
        self.heuristica = heuristica
        self.vecinos = []  

    def agregar_vecino(self, vecino, costo):
        self.vecinos.append((vecino, costo))

    def __lt__(self, otro):
        return self.heuristica < otro.heuristica

class Queue:
    def __init__(self, lifo=False):
        self.es_lifo = lifo
        self.cola = deque()

    def empty(self):
        return not self.cola

    def pop(self):
        return self.cola.pop() if self.es_lifo else self.cola.popleft()

    def add(self, elemento):
        self.cola.append(elemento)

class PriorityQueue:
    def __init__(self):
        self.cola = []

    def empty(self):
        return not self.cola

    def pop(self):
        return heapq.heappop(self.cola)[1]

    def add(self, prioridad, elemento):
        heapq.heappush(self.cola, (prioridad, elemento))


def obtener_vecinos(nodo):
    vecinos = []
    with open("funcion_de_costo.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar encabezado
        for origen, destino, costo in reader:
            if origen == nodo:
                vecinos.append((destino, int(costo)))
    return vecinos

def obtener_heuristica(nodo):
    with open("heuristica.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for actividad, heuristica in reader:
            if actividad == nodo:
                return int(heuristica)
    return float('inf')  

def busqueda_BFS(inicio, objetivo):
    cola = deque([(inicio, [inicio])])
    
    while cola:
        nodo_actual, ruta = cola.popleft()
        if nodo_actual == objetivo:
            return ruta
        for vecino, _ in obtener_vecinos(nodo_actual):
            if vecino not in ruta:
                cola.append((vecino, ruta + [vecino]))

def busqueda_DFS(inicio, objetivo):
    pila = [(inicio, [inicio])]

    while pila:
        nodo_actual, ruta = pila.pop()
        if nodo_actual == objetivo:
            return ruta
        for vecino, _ in obtener_vecinos(nodo_actual):
            if vecino not in ruta:
                pila.append((vecino, ruta + [vecino]))

def busqueda_UCS(inicio, objetivo):
    cola = []
    heapq.heappush(cola, (0, inicio, [inicio]))

    while cola:
        costo_actual, nodo_actual, ruta = heapq.heappop(cola)
        if nodo_actual == objetivo:
            return ruta, costo_actual
        for vecino, costo in obtener_vecinos(nodo_actual):
            if vecino not in ruta:
                heapq.heappush(cola, (costo_actual + costo, vecino, ruta + [vecino]))

def busqueda_Greedy(inicio, objetivo):
    cola = []
    heapq.heappush(cola, (obtener_heuristica(inicio), inicio, [inicio]))

    while cola:
        _, nodo_actual, ruta = heapq.heappop(cola)
        if nodo_actual == objetivo:
            return ruta
        for vecino, _ in obtener_vecinos(nodo_actual):
            if vecino not in ruta:
                heapq.heappush(cola, (obtener_heuristica(vecino), vecino, ruta + [vecino]))

def busqueda_Astar(inicio, objetivo):
    cola = []
    heapq.heappush(cola, (obtener_heuristica(inicio), 0, inicio, [inicio]))

    while cola:
        _, costo_acumulado, nodo_actual, ruta = heapq.heappop(cola)
        if nodo_actual == objetivo:
            return ruta, costo_acumulado
        for vecino, costo in obtener_vecinos(nodo_actual):
            if vecino not in ruta:
                g_n = costo_acumulado + costo
                h_n = obtener_heuristica(vecino)
                heapq.heappush(cola, (g_n + h_n, g_n, vecino, ruta + [vecino]))


inicio, objetivo = "Warm-up activities", "Stretching"

print("BFS:", busqueda_BFS(inicio, objetivo))
print("DFS:", busqueda_DFS(inicio, objetivo))
print("UCS:", busqueda_UCS(inicio, objetivo))
print("Greedy:", busqueda_Greedy(inicio, objetivo))
print("A*:", busqueda_Astar(inicio, objetivo))

