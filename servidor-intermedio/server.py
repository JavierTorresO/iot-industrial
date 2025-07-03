import socket
import json
import requests
from decoder import decode_packet

# Configuracion local
LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 9001
CLAVE_XOR = 0x5A

# Configuracion del Servidor Final
FINAL_HOST = 'localhost'
FINAL_PORT = 5000
FINAL_API_URL = f'http://{FINAL_HOST}:{FINAL_PORT}/api/datos'

def xor_decrypt(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)

def forward_to_final(payload: dict):
    """Envia el JSON para el resultado final"""
    try:
        response = requests.post(FINAL_API_URL, json=payload)
        response.raise_for_status()
        print("(Intermedio) Reenviado al servidor final con éxito")
    except Exception as e:
        print(f"(Intermedio) Error enviando al servidor final: {e}")

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
                while True:
                    raw_enc = conn.recv(1024)    
                    if not raw_enc:
                        break
                    raw = xor_decrypt(raw_enc, CLAVE_XOR)
                    try:
                        packet = decode_packet(raw)
                        print(f"(Intermedio) Decodificado: {packet}")
                        forward_to_final(packet)
                        print("(Intermedio) Reenviado al servidor final")
                    except Exception as e:
                        print(f"(Intermedio) Error: {e}")

if __name__ == '__main__':
    run_middle_server()