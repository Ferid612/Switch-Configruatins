import time
from netmiko import ConnectHandler
from services import write_to_text, current_time



def connect_to_switch(ip_address, username = "admin", password = "!n\/esT@"):

    # device_type = 'hp_comware_telnet' if model == "hp" else "cisco_ios_telnet"
    device_type = 'hp_comware_telnet'
    switch = {
        'device_type': device_type,
        'host': ip_address,
        'username': username,
        'password': password,
        'secret': password  
    }
    
    try:
        connection = ConnectHandler(**switch)
        print(f"Connected to {ip_address}")
    except:
        switch['device_type'] = "cisco_ios_telnet"
        connection = ConnectHandler(**switch)
        connection.enable()  # Enter privileged exec mode if required
        
        print(f"Connected to {ip_address}")
        
        
    return connection



def login_to_switch(connection):
    send_command_to_switch(connection, command = "_cmdline-mode on",sleep_time=0)
    send_command_to_switch(connection, command = "y",sleep_time=0)
    output = send_command_to_switch(connection, command = "512900",sleep_time=0)
        
        
    if "Error: Invalid password." in output:
        send_command_to_switch(connection, command = "_cmdline-mode on",sleep_time=0)
        send_command_to_switch(connection, command = "y", sleep_time=0)
        send_command_to_switch(connection, command = "Jinhua1920unauthorized",sleep_time=0)
        




def send_command_to_switch(connection, command = None, sleep_time = 1 ):
    if command is None:
        command = input("command: ")
        
    output = connection.send_command(command, expect_string='\n')
    time.sleep(sleep_time)
    print(output)
    return output
        
        

def start_hp_backup_procedure(ip_address, password = '!n\/esT@'):
    connection = connect_to_switch(ip_address, password = password)

    login_to_switch(connection) 

    output = send_command_to_switch(connection, "disp curr")

    all_text = output
    while True:
        # command = input("command: ")
        command = " - "
        output = send_command_to_switch(connection, command = command, sleep_time=0)
        all_text += " \n " + output
        print(output)
        if "% Unrecognized command found" in output or command == "break":
            break

    
    
    write_to_text(ip_address,all_text) 
    print(all_text)  # Print the command output
    connection.disconnect()  # Disconnect from the device



def start_cisco_backup_procedure(ip_address, password = '!n\/esT@'):
 
    try:

        connection = connect_to_switch(ip_address, password = password)
        output = connection.send_command('show run')  # Execute a command (e.g., show version)
        write_to_text(ip_address,all_text = output, model = "cisco") 
        
            
        # print(output)  # Print the command output
        connection.disconnect()  # Disconnect from the device
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    
def backup_switches(ip_addresses, model = "hp"):
    error_ips = []
    count = 0
    start_backup_procedure = start_hp_backup_procedure if model == "hp" else start_cisco_backup_procedure
    for ip_address in ip_addresses:
        count += 1 
        print(f"============== {count}/ {len(ip_addresses)} ==============")
        print(f"=========== {ip_address} ==============")
        try:   
            start_backup_procedure(ip_address)
        except Exception as e:
            try:
                try_again_count = 1
                start_backup_procedure(ip_address, password="AssKlim{}+#$")
            except Exception as e:
                print(f"Error: {str(e)}")

                try:
                    try_again_count+=1
                    start_backup_procedure(ip_address, password="Switch")
                except Exception as e:
                    print(f"Error: {str(e)}")
                    try_again_count+=1
                    pass

            if try_again_count == 3:
                error_ips.append(ip_address)
                print(f"Error: {str(e)}")

    if error_ips:
        file_name = f"error_reports/error_hp_switches_{current_time}.txt"
        with open(file_name, "w") as file:
            file.writelines(", ".join(error_ips))
        






# cisco_ip_addresses = ["172.16.73.1","172.16.70.1","172.16.70.222","172.16.70.14","172.16.77.1","172.16.77.12","172.16.47.1","172.16.78.1","172.16.92.1","172.16.91.1","172.16.97.1","172.16.93.1","172.16.93.210","172.16.99.1","172.16.99.100","172.16.80.1","172.16.32.1","172.16.55.1","172.16.90.1","172.16.90.70","172.16.90.150","172.16.90.217","172.16.90.67","172.16.90.36","172.16.90.69","172.16.31.1","172.16.60.1","172.16.60.135","172.16.60.30","172.16.60.160","172.16.72.1","172.16.75.1","172.16.73.1","172.16.46.1"]
# hp_ip_addresses = ["172.16.81.1","172.16.82.1","172.16.44.1","172.16.42.1","172.16.41.1","172.16.43.1","172.16.40.1","172.16.70.116","172.16.70.180","172.16.70.240","172.16.30.1","172.16.30.76","172.16.30.100","172.16.90.223","172.16.96.1","172.16.95.1","172.16.54.1","172.16.94.1","172.16.53.1","172.16.53.202","172.16.71.1","172.16.50.1","172.16.52.1","172.16.51.1","172.16.74.1","10.3.22.6 "]

   
hp_ip_addresses = ["172.16.81.1"]
cisco_ip_addresses = ["172.16.73.1"]

# backup_switches(hp_ip_addresses, model="hp")
backup_switches(cisco_ip_addresses, model="cisco")