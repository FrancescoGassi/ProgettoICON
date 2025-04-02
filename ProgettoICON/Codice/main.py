from typing import Optional
import os.path
import time
from typing import List, Tuple, Dict
from PIL import Image
import BaseConoscenza as KB
import Classificatore as clas
import Grafo as graph
import os

def clear_screen() -> None:
    """Pulisce lo schermo del terminale"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Inizializzazione immagine mappa
script_dir = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(script_dir, 'FAO37_sottozone.png'))

def display_header() -> None:
    print("\n" + "="*130)
    print(" "*25 + "███████╗ █████╗ ███████╗███████╗███████╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗ ")
    print(" "*25 + "██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██║██╔════╝██║  ██║██║████╗  ██║██╔════╝ ")
    print(" "*25 + "███████╗███████║█████╗  █████╗  █████╗  ██║███████╗███████║██║██╔██╗ ██║██║  ███╗")
    print(" "*25 + "╚════██║██╔══██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚════██║██╔══██║██║██║╚██╗██║██║   ██║")
    print(" "*25 + "███████║██║  ██║██║     ███████╗██║     ██║███████║██║  ██║██║██║ ╚████║╚██████╔╝")
    print(" "*25 + "╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ")
    print("="*130)
    print(" "*34 + "Creato da: Francesco Gassi & Alessandro Carli")
    print("="*130)

def display_menu() -> None:
    menu_options = [
        ("1", "Classificazione", "Classifica le zone di pesca"),
        ("2", "Valutazione Classificatore", "Valuta le prestazioni del classificatore"),
        ("3", "Mostra Zone FAO", "Visualizza la mappa delle zone FAO"),
        ("4", "Zone molto basso inquinamento", "Elenco zone con inquinamento minimo"),
        ("5", "Zone basso inquinamento", "Elenco zone con inquinamento basso"),
        ("6", "Zone moderato inquinamento", "Elenco zone con inquinamento moderato"),
        ("7", "Zone alto inquinamento", "Elenco zone con inquinamento alto"),
        ("8", "Zone molto alto inquinamento", "Elenco zone con inquinamento massimo"),
        ("9", "Lista inquinamenti", "Visualizza tutti i livelli di inquinamento"),
        ("10", "Trova percorso", "Calcola il percorso tra due zone"),
        ("11", "Verifica passaggio", "Controlla se è possibile passare tra due zone"),
        ("12", "Verifica inquinamento", "Controlla il livello di inquinamento"),
        ("0", "Esci", "Chiudi l'applicazione")
    ]
    
    print("\n" + "-"*90)
    print("{:<5} {:<35} {:<30}".format("NUM", "OPZIONE", "DESCRIZIONE"))
    print("-"*90)
    for num, opt, desc in menu_options:
        print("{:<5} {:<35} {:<30}".format(num, opt, desc))
    print("-"*90 + "\n")

def mostra_mappa() -> None:
    print("\nAPERTURA MAPPA FAO...")
    im.show()
    print("\nLa mappa rimarrà aperta. Chiudila manualmente quando hai finito.")
    input("Premi Invio per tornare al menu principale...")

def mostra_zone_per_inquinamento(livello: str) -> None:
    livelli = {
        "moltoBasso": ("MOLTO BASSO", "0-20%"),
        "basso": ("BASSO", "21-40%"),
        "moderato": ("MODERATO", "41-60%"),
        "alto": ("ALTO", "61-80%"),
        "moltoAlto": ("MOLTO ALTO", "81-100%")
    }
    
    if livello not in livelli:
        print("Livello di inquinamento non valido")
        return

    zone = KB.trova_zone_per_inquinamento(livello)
    livello_label, intervallo = livelli[livello]
    
    print("\n" + "-"*50)
    print(f"ZONE CON INQUINAMENTO {livello_label} ({intervallo})")
    print("-"*50)
    
    if zone:
        for z in zone:
            print(f"• {z}")
    else:
        print("Nessuna zona trovata con questo livello di inquinamento")
    
    print(f"\nTotale: {len(zone)} zone")

def gestisci_trova_percorso() -> None:
    print("\n" + "-"*40)
    print("CALCOLO PERCORSO OTTIMALE")
    print("-"*40)
    partenza = input("Zona di partenza (es. 1.1): ").strip()
    arrivo = input("Zona di destinazione (es. 1.2): ").strip()
    graph.trova_percorso(partenza, arrivo)

def gestisci_verifica_passaggio() -> None:
    """Versione migliorata con controllo input"""
    print("\n" + "="*50)
    print("VERIFICA PASSAGGIO TRA ZONE")
    print("="*50)
    
    while True:
        partenza = input("\nZona partenza (es. 1.1) o 'indietro': ").strip()
        if partenza.lower() == 'indietro':
            return
            
        arrivo = input("Zona arrivo (es. 1.2): ").strip()
        
        if not partenza or not arrivo:
            print("Inserire entrambe le zone")
            continue
            
        KB.domanda_passaggio(partenza, arrivo)
        break

def gestisci_verifica_inquinamento() -> None:
    print("\n" + "-"*40)
    print("VERIFICA INQUINAMENTO ZONA")
    print("-"*40)
    zona = input("Zona da verificare (es. 1.1): ").strip()
    livello = input("Livello da verificare (moltoBasso/basso/moderato/alto/moltoAlto): ").strip()
    KB.domanda_inquinamento_zona(zona, livello)

def menu(scelta: str) -> Optional[int]:
    scelta = scelta.lower().strip()
    
    opzioni = {
        "1": clas.classificatore,
        "2": clas.valutazione,
        "3": mostra_mappa,
        "4": lambda: mostra_zone_per_inquinamento("moltoBasso"),
        "5": lambda: mostra_zone_per_inquinamento("basso"),
        "6": lambda: mostra_zone_per_inquinamento("moderato"),
        "7": lambda: mostra_zone_per_inquinamento("alto"),
        "8": lambda: mostra_zone_per_inquinamento("moltoAlto"),
        "9": lambda: print("\nLivelli di inquinamento:\n- " + "\n- ".join(KB.get_lista_inquinamenti())),
        "10": gestisci_trova_percorso,
        "11": gestisci_verifica_passaggio,
        "12": gestisci_verifica_inquinamento,
        "0": lambda: 0
    }
    
    # Gestione alias per i comandi
    alias = {
        "classificazione": "1",
        "valutazione": "2",
        "mappa": "3",
        "molto basso": "4",
        "basso": "5",
        "moderato": "6",
        "alto": "7",
        "molto alto": "8",
        "lista": "9",
        "percorso": "10",
        "passaggio": "11",
        "inquinamento": "12",
        "esci": "0",
        "exit": "0"
    }
    
    scelta = alias.get(scelta, scelta)
    
    if scelta in opzioni:
        return opzioni[scelta]()
    else:
        print("\nScelta non valida. Riprova.")
        return None

if __name__ == '__main__':
    display_header()  # Mostra l'header iniziale
    while True:
        try:
            display_menu()
            scelta = input("Inserisci il numero dell'opzione desiderata (0-12) ➔  ").strip()
            risultato = menu(scelta)
            if risultato == 0:
                break
            input("\nPremi Invio per continuare...")
            clear_screen()
            display_header()  # Aggiungi questa linea per mostrare di nuovo l'header
        except KeyboardInterrupt:
            print("\n\nInterruzione dell'utente. Chiusura in corso...")
            break
        except Exception as e:
            print(f"\nSi è verificato un errore: {str(e)}")
            input("Premi Invio per continuare...")
            clear_screen()
            display_header()  # Aggiungi anche qui
    
    print("\n" + "="*34)
    print("GRAZIE PER AVER USATO SAFEFISHING!")
    print("="*34 + "\n")
    im.close()