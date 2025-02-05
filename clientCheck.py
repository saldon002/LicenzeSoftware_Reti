import socket
import sys
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 7000  # Porta del serverG per la gestione della validità delle licenze

# Funzione per inviare una richiesta di verifica della licenza
def invia_richiesta(codice_licenza):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_HOST, SERVER_PORT))  # Connessione al serverG

            # Creiamo il messaggio in formato JSON con il codice della licenza
            richiesta = {
                "comando": "VERIFICA",
                "licenza": codice_licenza
            }

            # Convertiamo la richiesta in formato JSON e la inviamo al serverG
            sock.sendall(json.dumps(richiesta).encode())

            # Ricezione della risposta dal serverG
            risposta = sock.recv(1024).decode()

            # Gestiamo la risposta per determinare la validità della licenza
            if risposta == "OK: Licenza valida":
                print(f"Licenza {codice_licenza} valida.")
            elif risposta == "ERRORE: Licenza non trovata":
                print(f"Licenza {codice_licenza} non trovata.")
            elif risposta == "ERRORE: Licenza scaduta":
                print(f"Licenza {codice_licenza} scaduta.")
            elif risposta == "ERRORE: Licenza invalidata":
                print(f"Licenza {codice_licenza} invalidata.")
            else:
                print(f"Risposta imprevista dal server: {risposta}")

    except Exception as e:
        print(f"Errore durante la comunicazione con il serverG: {e}")

# Funzione principale
def main():
    if len(sys.argv) < 2:
        print(
            "Parametri in input insufficienti.\nEseguire seguendo la sintassi: python clientCheck.py <CODICE_LICENZA>")
        sys.exit(1)

    for codice_licenza in sys.argv[1:]:
        codice_licenza = codice_licenza.upper()  # Convertiamo la licenza in maiuscolo
        invia_richiesta(codice_licenza)  # Invia una richiesta per ogni codice di licenza


if __name__ == "__main__":
    main()
