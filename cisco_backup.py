from netmiko import ConnectHandler


ip_addresses = ["172.16.73.1","172.16.70.1","172.16.70.222","172.16.70.14","172.16.77.1","172.16.77.12","172.16.47.1","172.16.78.1","172.16.92.1","172.16.91.1","172.16.97.1","172.16.93.1","172.16.93.210","172.16.99.1","172.16.99.100","172.16.80.1","172.16.32.1","172.16.55.1","172.16.90.1","172.16.90.70","172.16.90.150","172.16.90.217","172.16.90.67","172.16.90.36","172.16.90.69","172.16.31.1","172.16.60.1","172.16.60.135","172.16.60.30","172.16.60.160","172.16.72.1","172.16.75.1","172.16.73.1","172.16.46.1"]

count = 0

def start_cisco_backup_procedure(ip_address):
    switch = {
    'device_type': 'cisco_ios_telnet',
    'host': ip_address,
    'username': 'admin',
    'password': '!n\/esT@',
    'secret': '!n\/esT@'  # If enable password is required
    }
    # Establish SSH connection
    try:
        ssh_connection = ConnectHandler(**switch)
        ssh_connection.enable()  # Enter privileged exec mode if required
        output = ssh_connection.send_command('show run')  # Execute a command (e.g., show version)
        with open(f"swith_{ip_address}.txt", 'w') as file:
            file.write(output)
            
        # print(output)  # Print the command output
        ssh_connection.disconnect()  # Disconnect from the device

    
    except Exception as e:
        print(f"Error: {str(e)}")


for ip_address in ip_addresses:
    count+=1
    print(f"==============={count}/{len(ip_addresses)} ================")
    print(f"=============== {ip_address} =================")
    
    start_cisco_backup_procedure(ip_address)
