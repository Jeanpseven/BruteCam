# BruteCam
faz ataques de força bruta em câmeras de segurança,usando usuario e senhas padrão

________________________________________
# Wannasee3 - Script de Configuração Automática de CFTV e Rede Wi-Fi 
(fusão do DEDnetSec(https://github.com/Jeanpseven/DEDnetSEC) e BruteCam(https://github.com/Jeanpseven/BruteCam)

O Wannasee3 é um script Python que automatiza o processo de configuração de câmeras de segurança (CFTV) para permitir o acesso externo através da Internet. Além disso, o script também realiza a conexão automática a redes Wi-Fi disponíveis, utilizando um algoritmo para calcular senhas de redes Wi-Fi com base no BSSID.

## Funcionalidades

- Descoberta automática de redes Wi-Fi disponíveis e conexão utilizando senhas calculadas.
- Verificação de credenciais de acesso às câmeras de segurança através de um arquivo de lista de credenciais.
- Configuração automática de encaminhamento de portas no roteador para tornar as câmeras de segurança acessíveis pela Internet.
- Obtenção automática das informações de configuração de rede, como endereço IP do roteador, nome de usuário e senha.
- Salva IPs para você entrar depois com ponto de referência de localização e salva também usuario e senha para o login da camera

## Requisitos

- Python 3.x
- Bibliotecas Python necessárias: pywifi, scapy, paramiko, nmap

## Utilização

1. Certifique-se de ter o arquivo `camlist.txt` atualizado com as informações de credenciais das câmeras de segurança.
2. Abra um terminal e navegue até o diretório `BruteCam`.
3. Execute o seguinte comando para executar o script:

   python wannasee3.py
