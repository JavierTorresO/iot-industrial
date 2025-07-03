import struct
import datetime

def decode_packet(data: bytes):
    """
    Toma un buffer de bytes y extrae:
      - id (int16_t)
      - timestamp (double, segundos desde epoch)
      - temperatura (float)
      - presion (float)
      - humedad (float)
    Formato del struct: ! -> big endian
      h (int16), d (double), f (float), f y f
    Total = 2 + 8 + 4 + 4 + 4 = 22 bytes
    """
    if len(data) < 22:
        raise ValueError(f"Buffer muy pequeño: {len(data)} bytes (esperados ≥22)")
    
    try:  
        # desempaquetar los primeros 22 bytes
        id_sensor, ts, temp, pres, hum = struct.unpack('<hqfff', data[:22])
        print(f"[DEBUG] Timestamp recibido: {ts}")  # ← Añadido para depuración
        # convertir timestamp a ISO string
        fecha = datetime.datetime.utcfromtimestamp(ts).isoformat()
        return {
            'id':      id_sensor,
            'fecha_hora': fecha,
            'temperatura': temp,
            'presion':     pres,
            'humedad':     hum
        }
    except Exception as e:
        raise ValueError(f"Fallo al decodificar: {e}")