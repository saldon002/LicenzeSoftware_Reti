import socket
import sys
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 6000  # Porta del server per la gestione delle licenze


# Funzione per inviare una richiesta di licenza al server
def invia_richiesta(codice_licenza, data_acquisto, validita_mesi):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_HOST, SERVER_PORT))  # Connessione al portale

            # Creiamo il messaggio in formato JSON con il codice della licenza e i dettagli
            richiesta = {
                "comando": "REGISTRA", # Comando per registrare una nuova licenza
                "licenza": codice_licenza,
                "data_acquisto": data_acquisto,
                "validita_mesi": validita_mesi
            }
            # Convertiamo la richiesta in formato JSON e la inviamo al server
            sock.sendall(json.dumps(richiesta).encode())

            # Ricezione della risposta del portale che comunica con serverL
            risposta = sock.recv(1024).decode()

            # Mostriamo la risposta ricevuta
            print(f"Risposta dal server: {risposta}")
    except Exception as e:
        print(f"Errore durante la comunicazione con il server: {e}")


# Funzione principale
def main():
    if len(sys.argv) < 4:
        print("Parametri di input insufficienti.\nEseguire seguendo la sintassi: python clientReg.py <CODICE_LICENZA> <DATA_ACQUISTO> <VALIDITA_MESI>")
        sys.exit(1)

    codice_licenza = sys.argv[1].upper()  # Codice licenza in maiuscolo
    data_acquisto = sys.argv[2]  # Data di acquisto nel formato YYYY-MM-DD
    validita_mesi = int(sys.argv[3])  # Durata in mesi della licenza

    invia_richiesta(codice_licenza, data_acquisto, validita_mesi)


if __name__ == "__main__":
    main()
