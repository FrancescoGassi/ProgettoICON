import pandas as pd
import os.path
from sklearn import tree
from sklearn.model_selection import cross_val_score
from typing import Dict, Tuple, Optional

# Configurazioni
PESCI_VALIDI: Dict[str, int] = {
    'acciuga': 1,
    'merluzzo': 2,
    'sgombro': 3,
    'pesce_spada': 4,
    'palamita': 5,
    'rana_pescatrice': 6,
    'sardina': 7,
    'lampuga': 8,
    'alaccia': 9,
    'cernia': 11,
    'triglia': 12,
    'tonno': 13
}

ZONE_VALIDE: Dict[str, int] = {
    '1.1': 1,
    '1.2': 2,
    '1.3': 3,
    '2.1': 4,
    '2.2': 5,
    '3.1': 6,
    '3.2': 7,
    '4.1': 8,
    '4.2': 9,
    '4.3': 10
}

# Modello globale per evitare ri-addestramento
_modello: Optional[tree.DecisionTreeClassifier] = None
_dati: Optional[pd.DataFrame] = None

def _carica_dati() -> pd.DataFrame:
    """Carica il dataset delle probabilità di pesca"""
    global _dati
    if _dati is not None:
        return _dati
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'probpesca.csv')
    
    try:
        _dati = pd.read_csv(file_path)
        return _dati
    except FileNotFoundError:
        raise FileNotFoundError("File probpesca.csv non trovato")
    except Exception as e:
        raise Exception(f"Errore nel caricamento del file: {str(e)}")

def _addestra_modello() -> tree.DecisionTreeClassifier:
    """Addestra e restituisce il modello di classificazione"""
    global _modello
    if _modello is not None:
        return _modello
        
    dati = _carica_dati()
    X = dati.drop(columns=['prob'])
    y = dati['prob']
    
    _modello = tree.DecisionTreeClassifier(random_state=42)
    _modello.fit(X.values, y.values)
    return _modello

def _chiedi_pesce() -> str:
    """Chiede all'utente di inserire un tipo di pesce valido"""
    while True:
        pesce = input("Inserisci il pesce che vorresti pescare (es: tonno): ").lower()
        if pesce in PESCI_VALIDI:
            return pesce
        print(f"Pesce non valido. Scegli tra: {', '.join(PESCI_VALIDI.keys())}\n")

def _chiedi_zona() -> str:
    """Chiede all'utente di inserire una zona FAO valida"""
    while True:
        zona = input("Inserisci la zona FAO dove vuoi pescare (es: 1.1): ").strip()
        if zona in ZONE_VALIDE:
            return zona
        print(f"Zona non valida. Scegli tra: {', '.join(ZONE_VALIDE.keys())}")

def prevedi_probabilita(zona: int, pesce: int) -> int:
    """Esegue la previsione usando il modello addestrato"""
    modello = _addestra_modello()
    return modello.predict([[zona, pesce]])[0]

def valuta_modello() -> Tuple[float, float]:
    """Esegue la valutazione del modello con cross-validation"""
    dati = _carica_dati()
    X = dati.drop(columns=['prob'])
    y = dati['prob']
    
    modello = tree.DecisionTreeClassifier(random_state=42)
    scores = cross_val_score(modello, X.values, y.values, scoring='r2', cv=5)
    return scores.mean(), scores.std()

def classificatore() -> None:
    print("\n" + "-"*40)
    print("CLASSIFICAZIONE ZONE DI PESCA")
    print("-"*40)
    try:
        nome_pesce = _chiedi_pesce()
        nome_zona = _chiedi_zona()
        
        parametro_pesce = PESCI_VALIDI[nome_pesce]
        parametro_zona = ZONE_VALIDE[nome_zona]
        
        probabilita = prevedi_probabilita(parametro_zona, parametro_pesce)
        print(f"\nProbabilità di pescare {nome_pesce} in zona {nome_zona}: {probabilita}%")
    except Exception as e:
        print(f"\nErrore durante la classificazione: {str(e)}")

def valutazione() -> None:
    print("\n" + "-"*40)
    print("VALUTAZIONE CLASSIFICATORE")
    print("-"*40)
    try:
        media, dev_std = valuta_modello()
        print("\nRisultati valutazione:")
        print(f"- Accuratezza media (R²): {media:.2f}")
        print(f"- Deviazione standard: {dev_std:.2f}")
    except Exception as e:
        print(f"\nErrore durante la valutazione: {str(e)}")