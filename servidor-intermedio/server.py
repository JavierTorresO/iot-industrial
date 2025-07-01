import socket
import json
from decoder import decode_packet

# Configuracion local
LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 9001

# Configuracion del Servidor Final
FINAL_HOST = 'localhost'
FINAL_PORT = 9002

def forward_to_final(payload: dict):
    """Envia el JSON para el resultado final"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((FINAL_HOST, FINAL_PORT))
        data = json.dumps(payload).encode('utf-8')
        s.sendall(data)

def run_middle_server():
    """Loop principal que acepta conexiones del sensor, decodifica y reenvia."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((LISTEN_HOST, LISTEN_PORT))
        server.listen()
        print(f"(Intermedio) Escuchando en {LISTEN_HOST}:{LISTEN_PORT}…")
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"(Intermedio) Conexion de {addr}")
                raw = conn.recv(1024)
                if not raw:
                    continue
                try:
                    packet = decode_packet(raw)
                    print(f"(Intermedio) Decodificado: {packet}")
                    forward_to_final(packet)
                    print("(Intermedio) Reenviado al servidor final")
                except Exception as e:
                    print(f"(Intermedio) Error: {e}")

if __name__ == '__main__':
    run_middle_server()