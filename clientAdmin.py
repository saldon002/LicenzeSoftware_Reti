import socket
import sys
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 7000  # Porta del serverG per la gestione delle licenze


# Funzione per inviare una richiesta di invalidazione della licenza
def invia_richiesta(codice_licenza):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_HOST, SERVER_PORT))  # Connessione al serverG

            # Creiamo il messaggio in formato JSON con il comando "INVALIDA" e il codice della licenza
            richiesta = {
                "comando": "INVALIDA",  # Il comando ora è "INVALIDA"
                "licenza": codice_licenza,
            }

            # Convertiamo la richiesta in formato JSON e la inviamo al server
            sock.sendall(json.dumps(richiesta).encode())

            # Ricezione della risposta dal server
            risposta = sock.recv(1024).decode()

            if risposta == "OK: Licenza invalidata":
                print(f"Licenza {codice_licenza} invalidata con successo.")
            else:
                print(f"Errore nell'invalidare la licenza {codice_licenza}: {risposta}")
    except Exception as e:
        print(f"Errore durante la comunicazione con il server: {e}")


# Funzione principale
def main():
    if len(sys.argv) < 2:
        print(
            "Parametri in input insufficienti.\nEseguire seguendo la sintassi: python clientAdmin.py <CODICE_LICENZA>")
        sys.exit(1)

    codice_licenza = sys.argv[1].upper()  # Codice della licenza

    invia_richiesta(codice_licenza)  # Invia la richiesta per invalidare la licenza


if __name__ == "__main__":
    main()
