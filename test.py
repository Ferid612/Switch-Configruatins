import time
from netmiko import ConnectHandler, NetmikoTimeoutException

# ip_addresses = ["192.168.1.4"]
ip_addresses = ["172.16.52.1"]

# _cmdline-mode on
# y
# 512900
# sys
# ?


for ip_address in ip_addresses:

    # Define the device information
    switch = {
    # 'device_type': 'cisco_ios_telnet',
    'device_type': 'hp_comware',
    'host': ip_address,
    'username': 'admin',
    'password': '!n\/esT@',
    # 'secret': '!n\/esT@'  # If enable password is required
    }
    # Establish SSH connection
    try:
        ssh_connection = ConnectHandler(**switch)
        
        output = ssh_connection.send_command("_cmdline-mode on", expect_string='y')
        print("Output: ", output)        
        output = ssh_connection.send_command("y", expect_string='y')
        print("Output: ", output)        
        output = ssh_connection.send_command("512900", expect_string='y')
        print("Output: ", output)        
        
        output = ssh_connection.send_command("disp cur conf", expect_string='', read_timeout=20)
        print("Output: ", output)        
        
        # output = ssh_connection.send_command("\n", expect_string='HP_Comware#', read_timeout=20)
        # output = ssh_connection.send_command()
        print(output)        
        while True:
            input_text = input("command: ")
            output = ssh_connection.send_command(input_text, expect_string="", read_timeout=20)
            print(output)
            if input_text == "break":
                break

        # output = ssh_connection.send_command('display arp')  # Execute a command (e.g., show version)
        # ssh_connection.enable()  # Enter privileged exec mode if required
        # output = ssh_connection.send_command('sys', read_timeout=20, cmd_verify=False)  # Execute a command (e.g., show version)
        with open(f"swith_{ip_address}", 'w') as file:
            file.write(output)
            
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
