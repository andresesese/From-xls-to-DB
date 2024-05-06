import xlrd
import json
import sqlite3
import re
import os
import argparse

def process_xls_files(xls_files):
    # Inizializza una lista per contenere tutti i dati degli alunni
    all_students_data = []

    # Processa ogni file xls
    for xls_file in xls_files:
        data = xls_to_dict(xls_file)
        all_students_data.extend(data)

    # Carica il contenuto esistente del file JSON, se esiste
    json_content = []
    if os.path.exists("alunni.json"):
        with open("alunni.json", 'r') as json_file:
            json_content = json.load(json_file)

    # Aggiungi i nuovi dati agli esistenti
    json_content.extend(all_students_data)

    # Ordina i campi come richiesto
    ordered_fields = sorted(set().union(*(d.keys() for d in json_content)))
    ordered_fields = ["Pr_", "Alunno", "classe"] + sorted(field for field in ordered_fields if field not in ["Pr_", "Alunno", "Media", "Esito", "classe"]) + ["Media", "Esito"]

    # Scrivi tutti i dati degli studenti nel file JSON
    with open("alunni.json", 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

    # Cancella il database se esiste
    clear_database()

    # Crea un nuovo database SQLite
    conn = sqlite3.connect("alunni.db")
    cursor = conn.cursor()

    # Crea la tabella nel database SQLite
    create_table_query = f"CREATE TABLE IF NOT EXISTS data ({', '.join(ordered_fields)})"
    cursor.execute(create_table_query)

    # Inserisci dati nella tabella
    for student_data in json_content:
        values = [f"'{student_data.get(field, 'NULL')}'" for field in ordered_fields]
        insert_query = f"INSERT INTO data ({', '.join(ordered_fields)}) VALUES ({', '.join(values)})"
        cursor.execute(insert_query)

    # Commit e chiudi la connessione al database
    conn.commit()
    conn.close()

    print("Database SQLite creato e popolato con successo.")

def xls_to_dict(file_path):
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)

    # Estrai informazioni dalla seconda riga
    second_row_data = sheet.row_values(1)
    classe = os.path.splitext(os.path.basename(file_path))[0]  # Nome del file senza estensione

    # Estrai nomi delle colonne dalla quarta riga e sostituisci i caratteri non validi
    columns = sheet.row_values(3)
    columns = [re.sub(r'\W+', '_', col) for col in columns if col.strip()]

    # Crea lista di dizionari contenenti i dati
    data = []
    for row_index in range(4, min(27, sheet.nrows)):  # Ignora le righe dalla 24 in poi
        row_data = sheet.row_values(row_index)
        # Ignora le colonne "Z" e "AA"
        row_data = row_data[:25] + row_data[27:]
        # Ignora le colonne da "C" a "J"
        row_data = row_data[:2] + row_data[10:]
        # Leggi le prime due celle normalmente
        first_cells = row_data[:2]

        data.append({columns[i]: row_data[i] if i < len(row_data) else None for i in range(len(columns))})

    # Aggiungi il campo "classe" a ciascun record
    for record in data:
        record["classe"] = classe

    return data

def clear_database():
    if os.path.exists("alunni.db"):
        os.remove("alunni.db")
        print("Database SQLite eliminato.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process XLS files and create SQLite database.")
    parser.add_argument("files", nargs="+", help="List of XLS files to process")
    args = parser.parse_args()

    process_xls_files(args.files)
