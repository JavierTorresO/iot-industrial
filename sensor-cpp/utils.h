//Estructura del paquete y funciones auxiliares

#ifndef UTILS_H
#define UTILS_H

#include <cstdint>
#include <ctime>
#include <vector>

struct PaqueteSensor {
    int16_t id;
    int64_t timestamp;     // epoch time (segundos desde 1970)
    float temperatura;
    float presion;
    float humedad;
};

std::vector<uint8_t> serializarPaquete(const PaqueteSensor& p);
std::vector<uint8_t> cifrarXOR(const std::vector<uint8_t>& data, uint8_t clave);

#endif
