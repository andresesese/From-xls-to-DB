import sqlite3

def stampa_contenuto_database(nome_file_db):
    # Connessione al database
    connessione = sqlite3.connect(nome_file_db)
    cursore = connessione.cursor()

    # Ottenere i nomi di tutte le tabelle nel database
    cursore.execute("SELECT name FROM sqlite_master WHERE type='table';")
    nomi_tabelle = cursore.fetchall()

    # Stampa il contenuto di ciascuna tabella
    for tabella in nomi_tabelle:
        nome_tabella = tabella[0]
        print(f"\nContenuto della tabella '{nome_tabella}':")

        # Ottenere i nomi dei campi della tabella
        cursore.execute(f"PRAGMA table_info({nome_tabella});")
        nomi_campi = cursore.fetchall()
        nomi_campi = [campo[1] for campo in nomi_campi]
        print("Nomi dei campi:", nomi_campi)

        # Stampare il contenuto della tabella
        cursore.execute(f"SELECT * FROM {nome_tabella};")
        risultati = cursore.fetchall()
        for riga in risultati:
            print(riga)

    # Chiusura della connessione
    connessione.close()

# Nome del file del database SQLite
nome_file_db = "alunni.db"

# Chiamata alla funzione per stampare il contenuto di tutte le tabelle nel database
stampa_contenuto_database(nome_file_db)
