from Grafo import lista_zone, genera_grafo
from Classificatore import valuta_modello, _carica_dati
import pandas as pd

# Configurazione per massima leggibilità
pd.set_option('display.width', 120)
pd.set_option('display.colheader_justify', 'center')

# Stile tabella con bordi
def print_table(title, df, max_col_width=20):
    print(f"\n{'#' * 60}\n#{title:^58}#\n{'#' * 60}")
    df_str = df.to_string(
        index=False,
        justify='center',
        max_colwidth=max_col_width
    )
    print(df_str.replace('\n', '\n' + '-' * 60 + '\n'))

# --- Tabella 1: Inquinamento (compattata) ---
tab1 = pd.DataFrame([(z.name, z.inquinamento) for z in lista_zone], 
                    columns=["Zona", "Livello"])
tab1_grouped = tab1.groupby("Livello")["Zona"].agg(
    Zone=", ".join,
    Count="count"
).reset_index()
print_table("LIVELLI DI INQUINAMENTO PER ZONA", tab1_grouped)

# --- Tabella 2: Prestazioni Classificatore ---
media, dev = valuta_modello()
tab2 = pd.DataFrame({
    "Metrica": ["Accuratezza Media (R²)", "Deviazione Standard"],
    "Valore": [f"{media:.3f}", f"{dev:.3f}"]
})
print_table("PRESTAZIONI CLASSIFICATORE", tab2)

# --- Tabella 3: Connessioni (formato verticale) ---
grafo = genera_grafo()
connessioni = []
for zona in sorted(grafo.grafoDict.keys()):
    for vicino in grafo.grafoDict[zona]:
        connessioni.append([zona, "→", vicino])
tab3 = pd.DataFrame(connessioni, columns=["Da", "", "A"])
print_table("CONNESSIONI TRA ZONE", tab3)

# --- Tabella 4: Probabilità di Pesca (top 3 per specie) ---
df_pesca = _carica_dati()
specie = {1: "Acciuga", 2: "Merluzzo", 4: "Pesce Spada"}
tab4_data = []
for id_pesce, nome in specie.items():
    top = df_pesca[df_pesca["pesce"] == id_pesce].nlargest(3, "prob")
    for _, row in top.iterrows():
        tab4_data.append([nome, row["zona"], f"{row['prob']}%"])
tab4 = pd.DataFrame(tab4_data, columns=["Specie", "Zona", "Probabilità"])
print_table("MIGLIORI ZONE DI PESCA PER SPECIE", tab4)