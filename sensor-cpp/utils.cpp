//Implementación de funciones auxiliares

#include "utils.h"
#include <cstring>

std::vector<uint8_t> serializarPaquete(const PaqueteSensor& p) {
    std::vector<uint8_t> buffer(sizeof(PaqueteSensor));
    std::memcpy(buffer.data(), &p, sizeof(PaqueteSensor));
    return buffer;
}

std::vector<uint8_t> cifrarXOR(const std::vector<uint8_t>& data, uint8_t clave) {
    std::vector<uint8_t> resultado = data;
    for (auto& byte : resultado) {
        byte ^= clave; // XOR con clave simple
    }
    return resultado;
}
