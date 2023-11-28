from datetime import datetime
import time
from netmiko import ConnectHandler, NetmikoTimeoutException



def backup_switches(ip_addresses):
    for ip_address in ip_addresses:
    # Define the device information
        switch = {
    'device_type': 'hp_comware',
    'host': ip_address,
    'username': 'admin',
    'password': '!n\/esT@',
    }
    # Establish SSH connection
        try:
            ssh_connection = ConnectHandler(**switch)
        
            output = ssh_connection.send_command("_cmdline-mode on", expect_string='\n')
            print("Output: ", output)        
            output = ssh_connection.send_command("y", expect_string='\n')
            print("Output: ", output)        
            output = ssh_connection.send_command("512900", expect_string='\n')
            print("Output: ", output)        
        
            output = ssh_connection.send_command("disp curr", expect_string='\n', read_timeout=20)
            print("Output: ", output)        
        
            print(output)        
            all_text = output
            while True:
            # input_text = input("command: ")
                input_text = "-"
                output = ssh_connection.send_command(input_text,expect_string='\n', read_timeout=20)
                print(output)
                all_text += " \n " + output
                if input_text == "break" or "return" in output:
                    break

            
            write_to_text(ip_address,all_text) 
            
            print(output)  # Print the command output
            ssh_connection.disconnect()  # Disconnect from the device

    
        except Exception as e:
            print(f"Error: {str(e)}")





def send_show_command(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        prompt = ssh.find_prompt()
        ssh.send_command("terminal length 100")
        ssh.write_channel(f"{command}\n")
        output = ""
        while True:
            try:
                page = ssh.read_until_pattern(f"More|{prompt}")
                output += page
                if "More" in page:
                    ssh.write_channel(" ")
                elif prompt in output:
                    break
            except NetmikoTimeoutException:
                break
    return output




def write_to_text(ip_address, all_text):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"with_netmiko/hp_{ip_address}_{current_time}.txt"
    with open(file_name, "w") as file:
        file.writelines(all_text)
        
        
        
# ip_addresses = ["192.168.1.4"]

# _cmdline-mode on
# y
# 512900
# sys
# ?

ip_addresses = ["172.16.52.1"]
backup_switches(ip_addresses)