import numpy as np
from typing import Dict, List, Optional

class Grafo:
    def __init__(self, grafoDict: Optional[Dict] = None, orientato: bool = True):
        self.grafoDict = grafoDict or {}
        self.orientato = orientato
        if not orientato:
            self.conversioneNonOrientato()

    def conversioneNonOrientato(self) -> None:
        for a in list(self.grafoDict.keys()):
            for (b, dist) in self.grafoDict[a].items():
                self.grafoDict.setdefault(b, {})[a] = dist

    def connessione(self, A: str, B: str, distanza: float = 1) -> None:
        self.grafoDict.setdefault(A, {})[B] = distanza
        if not self.orientato:
            self.grafoDict.setdefault(B, {})[A] = distanza

    def get(self, a: str, b: Optional[str] = None) -> Dict:
        collegamenti = self.grafoDict.setdefault(a, {})
        return collegamenti if b is None else collegamenti.get(b)

    def nodi(self) -> List[str]:
        s1 = set(self.grafoDict.keys())
        s2 = set(k2 for v in self.grafoDict.values() for k2 in v.keys())
        return list(s1.union(s2))

    def rimuovi_nodo(self, nodo: str) -> None:
        for n in self.grafoDict:
            if nodo in self.grafoDict[n]:
                self.grafoDict[n].pop(nodo)
        if nodo in self.grafoDict:
            self.grafoDict.pop(nodo)

class Nodo:
    def __init__(self, nome: str, genitore: Optional['Nodo'] = None):
        self.nome = nome
        self.genitore = genitore
        self.g = 0.0  # Costo percorso da start
        self.h = 0.0  # Euristica
        self.f = 0.0  # Costo totale

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Nodo):
            return False
        return self.nome == other.nome

    def __lt__(self, other: 'Nodo') -> bool:
        return self.f < other.f

    def __repr__(self) -> str:
        return f"({self.nome}, f={self.f:.2f})"

class Zona:
    def __init__(self, name: str):
        self.name = name
        self.fattoriInquinanti = self._crea_inquinamento()
        self.inquinamento = self._assegna_inquinamento()

    def _crea_inquinamento(self) -> int:
        return np.random.randint(1, 101)  # Range 1-100

    def _assegna_inquinamento(self) -> str:
        if self.fattoriInquinanti <= 20:
            return 'moltoBasso'
        elif self.fattoriInquinanti <= 40:
            return 'basso'
        elif self.fattoriInquinanti <= 60:
            return 'moderato'
        elif self.fattoriInquinanti <= 80:
            return 'alto'
        else:
            return 'moltoAlto'

def calcolo_costo_reale(inquinamento_partenza: int, inquinamento_arrivo: int) -> float:
    return abs(inquinamento_partenza - inquinamento_arrivo) / 100.0

def calcolo_euristica(inquinamento_partenza: int, inquinamento_arrivo: int) -> float:
    return abs(inquinamento_partenza - inquinamento_arrivo) / 100.0

def vettore_euristiche(zona_target: Zona, zone: List[Zona]) -> Dict[str, float]:
    return {z.name: calcolo_euristica(zona_target.fattoriInquinanti, z.fattoriInquinanti) 
            for z in zone}

def ricerca_astar(grafo: Grafo, euristiche: Dict[str, float], 
                 partenza: Zona, arrivo: Zona) -> Optional[List[str]]:
    open_list = []
    closed_list = []
    
    nodo_start = Nodo(partenza.name)
    nodo_target = Nodo(arrivo.name)
    open_list.append(nodo_start)

    while open_list:
        open_list.sort()
        nodo_corrente = open_list.pop(0)
        closed_list.append(nodo_corrente)

        if nodo_corrente == nodo_target:
            path = []
            while nodo_corrente != nodo_start:
                path.append(nodo_corrente.nome)
                nodo_corrente = nodo_corrente.genitore
            path.append(nodo_start.nome)
            return path[::-1]
        
        vicini = grafo.get(nodo_corrente.nome) or {}
        for nome_vicino, costo in vicini.items():
            vicino = Nodo(nome_vicino, nodo_corrente)
            if vicino in closed_list:
                continue
                
            vicino.g = nodo_corrente.g + costo
            vicino.h = euristiche.get(vicino.nome, 0)
            vicino.f = vicino.g + vicino.h

            if not any(vicino == nodo and vicino.f >= nodo.f for nodo in open_list):
                open_list.append(vicino)
    
    return None

# Inizializzazione zone
lista_zone = [
    Zona("1.1"), Zona("1.2"), Zona("1.3"),
    Zona("2.1"), Zona("2.2"),
    Zona("3.1"), Zona("3.2"),
    Zona("4.1"), Zona("4.2"), Zona("4.3")
]

def genera_grafo() -> Grafo:
    grafo = Grafo(orientato=False)
    
    # Creiamo prima tutte le connessioni
    connessioni = [
        ("1.1", "1.2"), ("1.1", "1.3"), ("1.2", "1.3"),
        ("1.3", "2.2"), ("2.1", "2.2"), 
        ("2.2", "3.1"), ("2.2", "3.2"), ("3.1", "3.2"),
        ("3.1", "4.1"), ("4.1", "4.2"), ("4.2", "4.3")
    ]
    
    # Aggiungiamo solo connessioni tra zone non molto inquinate
    zone_non_molto_inquinate = [z for z in lista_zone if z.inquinamento != "moltoAlto"]
    nomi_zone_valide = {z.name for z in zone_non_molto_inquinate}
    
    for a, b in connessioni:
        if a in nomi_zone_valide and b in nomi_zone_valide:
            zona_a = next(z for z in lista_zone if z.name == a)
            zona_b = next(z for z in lista_zone if z.name == b)
            costo = calcolo_costo_reale(zona_a.fattoriInquinanti, zona_b.fattoriInquinanti)
            grafo.connessione(a, b, costo)
    
    return grafo

def trova_percorso(partenza: str, arrivo: str) -> None:
    zona_partenza = next((z for z in lista_zone if z.name == partenza), None)
    zona_arrivo = next((z for z in lista_zone if z.name == arrivo), None)

    if not zona_partenza or not zona_arrivo:
        print("Errore: una o più zone non valide")
        return
    
    if zona_partenza.inquinamento == "moltoAlto":
        print(f"Errore: la zona di partenza {partenza} ha inquinamento molto alto")
        return
        
    if zona_arrivo.inquinamento == "moltoAlto":
        print(f"Errore: la zona di arrivo {arrivo} ha inquinamento molto alto")
        return

    grafo = genera_grafo()
    euristiche = vettore_euristiche(zona_arrivo, lista_zone)
    percorso = ricerca_astar(grafo, euristiche, zona_partenza, zona_arrivo)
    
    if percorso:
        print("Percorso ottimale trovato:")
        print(" → ".join(percorso))
    else:
        print("Nessun percorso disponibile tra le zone specificate")