import nmap
import paramiko
import socket
import subprocess

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

# Function to check credentials for a specific manufacturer
def check_credentials(manufacturer, user, password):
    with open('Jeanpseven/BruteCam/camlist.txt', 'r') as file:
        for line in file:
            m, u, p = line.strip().split(',')
            if m == manufacturer and u == user and p == password:
                return True
    return False

# Read the camlist.txt file
credentials = {}
with open('Jeanpseven/BruteCam/camlist.txt', 'r') as file:
    for line in file:
        # Split the line into manufacturer, user, and password
        manufacturer, user, password = line.strip().split(',')
        credentials[manufacturer] = {"user": user, "password": password}

# Get the host from the user
ascii()
target_host = input("Enter the host (IP address or domain name) of the camera: ")

# Scan the host and get the manufacturer information
nm = nmap.PortScanner()
nm.scan(target_host, arguments="-O")

# Get the manufacturer from the scan results
manufacturer = nm[target_host]['osmatch'][0]['osclass'][0]['vendor']

# Check if credentials are available for the detected manufacturer
if manufacturer in credentials:
    user = credentials[manufacturer]["user"]
    password = credentials[manufacturer]["password"]
    if check_credentials(manufacturer, user, password):
        print("Credentials are valid.")
        print(f"Manufacturer: {manufacturer}")
        print(f"User: {user}")
        print(f"Password: {password}")

        # Get internal IP address
        internal_ip = socket.gethostbyname(socket.gethostname())
        print(f"Internal IP: {internal_ip}")

        # Get available port
        process = subprocess.Popen(['netstat', '-an', '-p', 'tcp'], stdout=subprocess.PIPE)
        output, _ = process.communicate()

        ports = []
        for line in output.decode().split('\n'):
            parts = line.split()
            if len(parts) == 4 and parts[1] == internal_ip and parts[3] == 'LISTENING':
                _, port = parts[3].rsplit(':', 1)
                ports.append(int(port))

        internal_port = min(set(range(8080, 9090)) - set(ports))  # Change the range if needed
        print(f"Internal Port: {internal_port}")

        # Get router IP address
        router_ip = subprocess.check_output(['ip', 'route', 'show', 'default']).decode().split()
        router_ip = router_ip[2]

        # Get router username and password (assuming they are the same as the computer's username and password)
        router_username = subprocess.check_output(['whoami']).decode().strip()
        router_password = subprocess.check_output(['pass', 'show', 'router_password']).decode().strip()  # Replace with your password retrieval method

        # Get external interface port (assuming it is the same as the internal port)
        external_interface_port = internal_port

        # Establish SSH connection to the router
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(router_ip, username=router_username, password=router_password)

            # Configure port forwarding on the router
            command = f'ip nat inside source static tcp {internal_ip} {internal_port} interface {external_interface_port}'
            ssh.exec_command(command)

            # Save the router configuration
            ssh.exec_command('write memory')

            print("Port forwarding configured successfully.")
        except paramiko.AuthenticationException:
            print("Failed to connect to the router. Authentication failed.")
        except paramiko.SSHException:
            print("Failed to establish SSH connection to the router.")
        finally:
            ssh.close()
    else:
        print("Credentials are invalid.")
else:
    print("No credentials available for the detected manufacturer.")
