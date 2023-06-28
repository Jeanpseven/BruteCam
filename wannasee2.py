import nmap

# Function to check credentials for a specific manufacturer
def check_credentials(manufacturer, user, password):
    # Add your code here to test the credentials for the given manufacturer
    # Return True if the credentials are valid, False otherwise
    return False

# Read the camlist.txt file
credentials = {}
with open('Jeanpseven/BruteCam/camlist.txt', 'r') as file:
    for line in file:
        # Split the line into manufacturer, user, and password
        manufacturer, user, password = line.strip().split(',')
        credentials[manufacturer] = {"user": user, "password": password}

# Get the host from the user
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
    else:
        print("Credentials are invalid.")
else:
    print("No credentials available for the detected manufacturer.")
