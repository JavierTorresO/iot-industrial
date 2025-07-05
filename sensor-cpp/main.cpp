#define _WIN32_WINNT 0x0601  // Habilita funciones modernas como inet_pton (Windows 7+)

#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <cstdlib>
#include <ctime>
#include "utils.h"

#pragma comment(lib, "ws2_32.lib")

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 9001
#define CLAVE_XOR 0x5A

PaqueteSensor generarLectura(int16_t id) {
    PaqueteSensor p;
    p.id = id;
    p.timestamp = std::time(nullptr);
    p.temperatura = 20 + rand() % 10 + (rand() % 100) / 100.0f;
    p.presion = 1000 + rand() % 50;
    p.humedad = 40 + rand() % 60;
    return p;
}

int main(int argc, char* argv[]) {
    // Parámetros por defecto: envío indefinido cada 5 segundos
    int num_paquetes = 0;          // 0 = infinito
    int intervalo_segundos = 5;    // Intervalo de 5 segundos

    // Leer argumentos opcionales: ./sensor.exe <num_paquetes> <intervalo_segundos>
    if (argc >= 2) num_paquetes = std::atoi(argv[1]);
    if (argc >= 3) intervalo_segundos = std::atoi(argv[2]);

    // Inicializar Winsock
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
        std::cerr << "Error al inicializar Winsock.\n";
        return 1;
    }

    // Crear socket TCP
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Error al crear socket.\n";
        WSACleanup();
        return 1;
    }

    // Configurar dirección del servidor
    sockaddr_in serv_addr{};
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr);

    // Conectar al servidor
    if (connect(sock, (sockaddr*)&serv_addr, sizeof(serv_addr)) == SOCKET_ERROR) {
        std::cerr << "Error al conectar con servidor.\n";
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    std::cout << "Conectado al servidor intermedio\n";

    srand(time(0));

    int contador = 0;
    while (num_paquetes == 0 || contador < num_paquetes) {
        PaqueteSensor p = generarLectura(1);
        auto binario = serializarPaquete(p);
        auto cifrado = cifrarXOR(binario, CLAVE_XOR);

        int bytesEnviados = send(sock, reinterpret_cast<const char*>(cifrado.data()), cifrado.size(), 0);
        if (bytesEnviados == SOCKET_ERROR) {
            std::cerr << "Error al enviar datos.\n";
            break;
        }
        std::cout << "Lectura enviada: T=" << p.temperatura << "°C, P=" << p.presion << " hPa, H=" << p.humedad << "%\n";

        std::this_thread::sleep_for(std::chrono::seconds(intervalo_segundos));
        contador++;
    }

    closesocket(sock);
    WSACleanup();

    return 0;
}


// Como probar: 1ero tener corriendo el archivo pruebas/server_test.py con "python server_test.py", 2do correr este archivo con "g++ main.cpp utils.cpp -lws2_32 -o sensor.exe" -> dara resultados en esta terminal estilo "Lectura enviada + datos" y en terminal del servidor dira "Recibidos X bytes"