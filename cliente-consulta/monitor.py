import requests
import time

# URL
API_URL = "http://localhost:5000/api/datos"

# Segundos entre cada intervalo
SEGUNDOS = 5

# Rangos normales
RANGO_TEMP = (15, 30)    # °C
RANGO_PRES = (950, 1050) # hPa
RANGO_HUM  = (30, 90)    # %

def verificar_rangos(dato):
    alertas = []
    if not (RANGO_TEMP[0] <= dato['temperatura'] <= RANGO_TEMP[1]):
        alertas.append(f"Temperatura fuera de rango: {dato['temperatura']}°C")
    if not (RANGO_PRES[0] <= dato['presion'] <= RANGO_PRES[1]):
        alertas.append(f"Presion fuera de rango: {dato['presion']} hPa")
    if not (RANGO_HUM[0] <= dato['humedad'] <= RANGO_HUM[1]):
        alertas.append(f"Humedad fuera de rango: {dato['humedad']}%")
    return alertas

def main():
    print("Cliente de Consulta iniciado. Verificando cada", SEGUNDOS, "segundos...")
    while True:
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            datos = response.json()
            if not datos:
                print("No hay datos registrados aún.")
            else:
                ultimo = datos[-1]
                print(f"Última lectura: T={ultimo['temperatura']}°C, P={ultimo['presion']} hPa, H={ultimo['humedad']}%")
                alertas = verificar_rangos(ultimo)
                if alertas:
                    print("ADVERTENCIA")
                    for alerta in alertas:
                        print(" -", alerta)
        except Exception as e:
            print("Error consultando la API:", e)
        time.sleep(SEGUNDOS)

if __name__ == '__main__':
    main()
