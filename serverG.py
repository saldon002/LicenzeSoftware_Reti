import socket
import threading
import json

# Configurazioni
SERVERG_PORT = 7000
SERVERL_HOST = "localhost"
SERVERL_PORT = 5000  # Porta del serverL per la gestione delle licenze
THREAD_POOL_SIZE = 10


# Funzione per inoltrare la richiesta al serverL
def inoltra_richiesta_serverL(messaggio):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVERL_HOST, SERVERL_PORT))
            s.sendall(messaggio.encode())
            risposta = s.recv(1024).decode()
        return risposta
    except Exception as e:
        return f"ERRORE: {str(e)}"


# Funzione per gestire la connessione del client
def handle_connection(client_sock):
    try:
        # Riceve i dati dal client (in formato JSON)
        data = client_sock.recv(1024).decode()
        if not data:
            return

        # Convertiamo i dati ricevuti in un dizionario
        richiesta = json.loads(data)

        # Determiniamo il tipo di servizio richiesto (Verifica o Invalidazione)
        if richiesta['comando'] == "VERIFICA":
            print("Servizio richiesto: verifica di validità della licenza")
        elif richiesta['comando'] == "INVALIDA":
            print("Servizio richiesto: invalidazione della licenza")
        else:
            client_sock.sendall("ERRORE: Comando non riconosciuto".encode())
            return

        # Inoltra la richiesta al serverL
        risposta_serverL = inoltra_richiesta_serverL(data)

        # Invia la risposta ricevuta dal serverL al client
        client_sock.sendall(risposta_serverL.encode())

    except Exception as e:
        print(f"Errore nella gestione della connessione: {e}")
    finally:
        client_sock.close()


# Funzione per avviare il server
def avvia_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('localhost', SERVERG_PORT))
    server_sock.listen(THREAD_POOL_SIZE)

    print(f"ServerG in ascolto sulla porta {SERVERG_PORT}")

    # Accetta le connessioni in parallelo utilizzando un pool di thread
    while True:
        client_sock, client_address = server_sock.accept()
        print(f"Connessione ricevuta da {client_address}")

        # Gestisce la connessione del client in un thread separato
        threading.Thread(target=handle_connection, args=(client_sock,)).start()


if __name__ == "__main__":
    avvia_server()