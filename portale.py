# portale.py - Server intermedio per la gestione delle licenze software
import socket
import threading
import json

# Configurazioni
HOST = "localhost"
PORT = 6000
SERVER_L_HOST = "localhost"
SERVER_L_PORT = 5000

# Funzione per inoltrare le richieste ai server
def inoltra_richiesta(server_host, server_port, messaggio):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_host, server_port))
            s.sendall(messaggio.encode())
            risposta = s.recv(1024).decode()
        return risposta
    except Exception as e:
        return f"ERRORE: {str(e)}"

# Funzione per gestire la connessione con il client
def gestisci_client(conn, addr):
    print(f"Connessione ricevuta da {addr}")
    while True:
        try:
            dati = conn.recv(1024).decode()  # Riceve la richiesta dal client
            if not dati:
                break

            # Decodifica della richiesta JSON
            richiesta = json.loads(dati)

            comando = richiesta.get("comando")
            if comando == "REGISTRA":
                # Estrai i parametri dalla richiesta JSON
                codice_licenza = richiesta["licenza"]
                data_acquisto = richiesta["data_acquisto"]
                validita_mesi = richiesta["validita_mesi"]

                # Crea un messaggio per il serverL
                dati_serverL = json.dumps({
                    "comando": "REGISTRA",
                    "licenza": codice_licenza,
                    "data_acquisto": data_acquisto,
                    "validita_mesi": validita_mesi
                })

                # Invia la richiesta al serverL
                risposta = inoltra_richiesta(SERVER_L_HOST, SERVER_L_PORT, dati_serverL)

            else:
                risposta = "ERRORE: Comando non riconosciuto"

            # Invia la risposta al client
            conn.sendall(risposta.encode())

        except Exception as e:
            print(f"Errore: {e}")
            break

    conn.close()

# Funzione per avviare il server
def avvia_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Portale in ascolto su {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=gestisci_client, args=(conn, addr)).start()

if __name__ == "__main__":
    avvia_server()
