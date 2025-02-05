# serverL.py - Server per la gestione delle licenze software
import socket
import threading
import json
import os
from datetime import datetime, timedelta

LICENZE_FILE = "licenze.json"
LOCK = threading.Lock()

# Carica il file JSON con le licenze
if not os.path.exists(LICENZE_FILE):
    with open(LICENZE_FILE, "w") as f:
        json.dump({}, f)

def carica_licenze():
    try:
        with LOCK, open(LICENZE_FILE, "r") as f:
            licenze = json.load(f)
            if not isinstance(licenze, dict):  # Controllo se è un dizionario valido
                return {}
            return licenze
    except (json.JSONDecodeError, FileNotFoundError):
        return {}  # Se il file è vuoto, corrotto o inesistente, restituisce un dizionario vuoto

def salva_licenze(licenze):
    with LOCK, open(LICENZE_FILE, "w") as f:
        json.dump(licenze, f, indent=4)

def registra_licenza(software_id, data_acquisto, validita_mesi):
    licenze = carica_licenze()
    if software_id in licenze:
        return "ERRORE: Licenza già registrata"
    licenze[software_id] = {"data_acquisto": data_acquisto, "validita_mesi": validita_mesi, "valida": True}
    salva_licenze(licenze)
    return "OK: Licenza registrata"


def verifica_licenza(software_id):
    licenze = carica_licenze()
    if software_id not in licenze:
        return "ERRORE: Licenza non trovata"

    licenza = licenze[software_id]

    if not licenza["valida"]:
        return "ERRORE: Licenza invalidata"

    # Converto la data di attivazione in formato datetime
    data_attivazione = datetime.strptime(licenza["data_acquisto"], "%Y-%m-%d")

    # Aggiungo i mesi di validità alla data di attivazione
    mesi_validita = licenza["validita_mesi"]
    data_scadenza = data_attivazione + timedelta(days=mesi_validita * 30)  # Ogni mese ha 30 giorni

    # Ottengo la data odierna
    oggi = datetime.today()

    if oggi > data_scadenza:
        return "ERRORE: Licenza scaduta"

    return "OK: Licenza valida"

def invalida_licenza(software_id):
    licenze = carica_licenze()
    if software_id not in licenze:
        return "ERRORE: Licenza non trovata"

    licenze[software_id]["valida"] = False
    salva_licenze(licenze)
    return "OK: Licenza invalidata"


def gestisci_client(conn, addr):
    print(f"Connessione da {addr}")
    while True:
        try:
            dati = conn.recv(1024).decode()
            if not dati:
                break

            richiesta = json.loads(dati)  # Parsing del JSON
            comando = richiesta.get("comando")

            print(f"Ricevuto comando: {comando}, dati: {richiesta}")  # DEBUG

            if comando == "REGISTRA":
                software_id = richiesta.get("licenza")
                data_attivazione = richiesta.get("data_acquisto")
                validita_mesi = richiesta.get("validita_mesi")

                if None in (software_id, data_attivazione, validita_mesi):
                    risposta = "ERRORE: Parametri mancanti per la registrazione"
                else:
                    risposta = registra_licenza(software_id, data_attivazione, validita_mesi)

            elif comando == "VERIFICA":
                software_id = richiesta.get("licenza")

                if software_id is None:
                    risposta = "ERRORE: Parametri mancanti per la verifica"
                else:
                    risposta = verifica_licenza(software_id)

            elif comando == "INVALIDA":
                software_id = richiesta.get("licenza")

                if software_id is None:
                    risposta = "ERRORE: Parametri mancanti per invalidazione"
                else:
                    risposta = invalida_licenza(software_id)

            else:
                risposta = "ERRORE: Comando sconosciuto"

            conn.sendall(risposta.encode())
        except Exception as e:
            print(f"Errore: {e}")
            break
    conn.close()


def avvia_server():
    HOST = "localhost"
    PORT = 5000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"ServerL in ascolto su {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=gestisci_client, args=(conn, addr)).start()

if __name__ == "__main__":
    avvia_server()
