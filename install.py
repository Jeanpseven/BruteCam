import subprocess

# Instala as dependências do arquivo requirements.txt
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

print("Instalação concluída.")
