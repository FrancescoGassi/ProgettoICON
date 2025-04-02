from typing import Dict, List, Set, Optional
from Grafo import lista_zone

def crea_lista_zone_confinanti() -> Dict[str, bool]:
    """Crea un dizionario delle zone confinanti con chiavi univoche"""
    confini = {
        ("1.1", "1.2"): True,
        ("1.1", "1.3"): True,
        ("1.3", "1.2"): True,
        ("1.3", "2.2"): True,
        ("2.1", "2.2"): True,
        ("2.2", "3.1"): True,
        ("2.2", "3.2"): True,
        ("3.1", "3.2"): True,
        ("3.1", "4.1"): True,
        ("4.1", "4.2"): True,
        ("4.2", "4.3"): True
    }
    return {f"{a}{b}": val for (a, b), val in confini.items()}

lista_confini_zone = crea_lista_zone_confinanti()

def crea_lista_inquinamenti_zone() -> Dict[str, bool]:
    return {f"{zona.name}_{zona.inquinamento}": True for zona in lista_zone}

lista_inquinamenti_zone = crea_lista_inquinamenti_zone()

def crea_lista_livelli_inquinamento() -> List[str]:
    return ['moltoBasso', 'basso', 'moderato', 'alto', 'moltoAlto']

lista_inquinamenti = crea_lista_livelli_inquinamento()

def zona_esiste(zona: str) -> bool:
    return any(z.name == zona for z in lista_zone)

def trova_inquinamento_zona(zona_inquinamento: str) -> bool:
    return zona_inquinamento in lista_inquinamenti_zone

def filtra_zone_per_inquinamento(livello: str) -> List[str]:
    if livello not in lista_inquinamenti:
        return []
    return [z.name for z in lista_zone if z.inquinamento == livello]

def controlla_livello_inquinamento(inquinamento: str) -> bool:
    return inquinamento in lista_inquinamenti

def zona_non_molto_inquinata(zona: str) -> bool:
    return f"{zona}_moltoAlto" not in lista_inquinamenti_zone

def mostra_dettagli_inquinamento(zona: str, inquinamento: str, risultato: bool) -> None:
    zona_obj = next((z for z in lista_zone if z.name == zona), None)
    if not zona_obj:
        print("Zona non trovata")
        return
        
    print(f"\nDettagli completi inquinamento zona {zona}:")
    print(f"- Livello attuale: {zona_obj.inquinamento}")
    print(f"- Livello verificato: {inquinamento}")
    print(f"- Corrispondenza: {'✅' if risultato else '❌'}")
    print("\nLivelli possibili: moltoBasso, basso, moderato, alto, moltoAlto")
    
    while True:
        comando = input("\nDigita 'esci' per terminare: ").lower().strip()
        if comando == "esci":
            return
        else:
            print("Comando non riconosciuto")

def mostra_dettagli_inquinamento_zona(zona: str) -> None:
    if not zona_esiste(zona):
        print("Zona non valida")
        return
        
    print(f"\nLivelli di inquinamento per {zona}:")
    for livello in ['moltoBasso', 'basso', 'moderato', 'alto', 'moltoAlto']:
        stato = "✅" if trova_inquinamento_zona(f"{zona}_{livello}") else "❌"
        print(f"- {livello}: {stato}")

def mostra_dettagli_passaggio(partenza: str, arrivo: str, 
                            confinanti: bool, zona1_sicura: bool, zona2_sicura: bool) -> None:
    print(f"\nDettagli passaggio da {partenza} a {arrivo}:")
    print(f"1. Confinanti: {'✅' if confinanti else '❌'}")
    print(f"2. {partenza} non molto inquinata: {'✅' if zona1_sicura else '❌'}")
    print(f"3. {arrivo} non molto inquinata: {'✅' if zona2_sicura else '❌'}")
    
    while True:
        comando = input("Digita 'how 1/2/3' per dettagli o 'esci' per terminare: ").lower()
        if comando == "esci":
            return
        elif comando == "how 1":
            print(f"Confine tra {partenza} e {arrivo} esiste: {confinanti}")
        elif comando == "how 2":
            mostra_dettagli_inquinamento_zona(partenza)
        elif comando == "how 3":
            mostra_dettagli_inquinamento_zona(arrivo)
        else:
            print("Comando non riconosciuto")

def domanda_inquinamento_zona(zona: str, livello: str) -> None:
    """Versione definitiva con miglioramenti"""
    # Validazione input
    if not zona_esiste(zona):
        print(f"NO - Zona {zona} non valida")
        return
        
    livelli_validi = ['moltoBasso', 'basso', 'moderato', 'alto', 'moltoAlto']
    if livello not in livelli_validi:
        print(f"NO - Livello deve essere uno di: {', '.join(livelli_validi)}")
        return
    
    zona_obj = next(z for z in lista_zone if z.name == zona)
    risultato = zona_obj.inquinamento == livello
    
    # Output dettagliato
    print("\n" + "="*50)
    print(f"VERIFICA INQUINAMENTO: {zona}")
    print("="*50)
    print(f"● Livello attuale: {zona_obj.inquinamento}")
    print(f"● Livello verificato: {livello}")
    print("-"*50)
    print(f"RISULTATO: {'✅ YES' if risultato else '❌ NO'}")
    
    # Interazione how
    while True:
        cmd = input("\nDigita 'how' per spiegazione o 'esci': ").lower().strip()
        if cmd == "esci":
            break
        elif cmd == "how":
            print("\nSPIEGAZIONE:")
            print(f"La zona {zona} ha inquinamento {zona_obj.inquinamento}")
            print(f"Stai verificando se è {livello}")
            print("\nLivelli possibili:", ', '.join(livelli_validi))
        else:
            print("Comando non valido")

def valida_formato_zona(zona: str) -> bool:
    """Controlla se il formato è 'numero.numero'"""
    if not isinstance(zona, str):
        return False
    parts = zona.split('.')
    return len(parts) == 2 and all(p.isdigit() for p in parts)

def domanda_passaggio(zona_partenza: str, zona_arrivo: str) -> None:
    # Validazione input
    if not valida_formato_zona(zona_partenza) or not valida_formato_zona(zona_arrivo):
        print("❌ Formato zona non valido. Usa 'numero.numero' (es. '1.1')")
        input("\nPremi Invio per continuare...")
        return

    if zona_partenza == zona_arrivo:
        print("❌ Inserire due zone diverse")
        input("\nPremi Invio per continuare...")
        return

    if not zona_esiste(zona_partenza):
        print(f"❌ Zona {zona_partenza} non esistente. Zone valide: {', '.join(z.name for z in lista_zone)}")
        input("\nPremi Invio per continuare...")
        return

    if not zona_esiste(zona_arrivo):
        print(f"❌ Zona {zona_arrivo} non esistente. Zone valide: {', '.join(z.name for z in lista_zone)}")
        input("\nPremi Invio per continuare...")
        return

    # Ottieni i dati delle zone
    partenza = next(z for z in lista_zone if z.name == zona_partenza)
    arrivo = next(z for z in lista_zone if z.name == zona_arrivo)

    # Verifica confini e inquinamento
    confinanti = f"{zona_partenza}{zona_arrivo}" in lista_confini_zone or f"{zona_arrivo}{zona_partenza}" in lista_confini_zone
    zona1_sicura = partenza.inquinamento != "moltoAlto"
    zona2_sicura = arrivo.inquinamento != "moltoAlto"
    risultato = confinanti and zona1_sicura and zona2_sicura

    # Output risultato principale
    print("\n" + "═" * 50)
    print(f"VERIFICA PASSAGGIO: {zona_partenza} → {zona_arrivo}")
    print("═" * 50)
    print(f"● Zone confinanti: {'✅' if confinanti else '❌'} (collegate direttamente)")
    print(f"● Inquinamento {zona_partenza}: {partenza.inquinamento} {'✅' if zona1_sicura else '❌'}")
    print(f"● Inquinamento {zona_arrivo}: {arrivo.inquinamento} {'✅' if zona2_sicura else '❌'}")
    print("═" * 50)
    print(f"RISULTATO: {'✅ YES' if risultato else '❌ NO'}")

    # Interazione how migliorata
    print("\nDigita 'how' per maggiori dettagli o INVIO per continuare...")
    cmd = input().lower().strip()
    
    if cmd == "how":
        print("\n" + "═" * 50)
        print("SPIEGAZIONE DETTAGLIATA")
        print("═" * 50)
        
        # 1. Spiegazione connessione
        print("\nCONNESSIONE TRA LE ZONE:")
        print(f"- Confinanti: {'Sì' if confinanti else 'No'}")
        if confinanti:
            print("  Le zone sono collegate direttamente nella mappa FAO")
        else:
            print("  Non esiste un collegamento diretto tra queste zone")
        
        # 2. Spiegazione inquinamento
        print("\nLIVELLI DI INQUINAMENTO:")
        print(f"- {zona_partenza}: {partenza.inquinamento}")
        print(f"- {zona_arrivo}: {arrivo.inquinamento}")
        print("\nNota: Il passaggio è bloccato se una zona ha inquinamento 'moltoAlto'")

        # 3. Connessioni disponibili
        print("\n" + "═" * 50)
        print("CONNESSIONI DISPONIBILI PER QUESTE ZONE:")
        connections = set()
        for conn in lista_confini_zone.keys():
            if zona_partenza in conn or zona_arrivo in conn:
                # Estrae le zone dal formato "1.11.2"
                parts = [conn[i:i+3] for i in range(0, len(conn), 3)]
                connections.update(parts)
        
        if connections:
            print("- " + "\n- ".join(sorted(connections)))
        else:
            print("Nessuna connessione disponibile")

        input("\nPremi Invio per tornare al menu...")
            
# Funzioni di utilità per l'interfaccia
def trova_zone_per_inquinamento(livello: str) -> List[str]:
    return filtra_zone_per_inquinamento(livello)

def get_lista_inquinamenti() -> List[str]:
    return lista_inquinamenti.copy()