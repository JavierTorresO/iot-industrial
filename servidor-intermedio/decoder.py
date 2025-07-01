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
    # desempaquetar los primeros 22 bytes
    id_sensor, ts, temp, pres, hum = struct.unpack('!hdfff', data[:22])
    # convertir timestamp a ISO string
    fecha = datetime.datetime.fromtimestamp(ts).isoformat()
    return {
        'id':      id_sensor,
        'timestamp': fecha,
        'temperatura': temp,
        'presion':     pres,
        'humedad':     hum
    }