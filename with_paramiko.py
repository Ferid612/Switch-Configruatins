from datetime import datetime
import paramiko
import time

from input import get_key

# Function to execute commands on the switch


def connect_to_switch(ip_address, username="admin", password="!n\/esT@"):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, password=password, timeout=5)
    print(f"Connected to {ip_address}")
        # Create a shell
    remote_shell = ssh_client.invoke_shell()
    return ssh_client, remote_shell




def send_command_to_switch(remote_shell, command = None, sleep_time = 1 ):
    if command is None:
        command = input("command: ")
        
    remote_shell.send(command + "\n")
    time.sleep(sleep_time)
    output = remote_shell.recv(65535).decode('utf-8')
    print(output)
    return output



def collect_current_conf_data(ip_address):
    try:
        # Connect to the switch
        ssh_client, remote_shell = connect_to_switch(ip_address)
        login_to_switch(remote_shell)


        command = "display current-configuration"
        output = send_command_to_switch(remote_shell, command = command)
        all_text = output
        while True:
            output = send_command_to_switch(remote_shell, command = " ", sleep_time=0)
            all_text += "\n" + output + "\n"        
            if ">" in output:
                break    
            
        write_to_text(ip_address, all_text)


    except paramiko.AuthenticationException:
        print(f"Authentication failed for {ip_address}")
    except paramiko.SSHException as ssh_err:
        print(f"SSH connection failed for {ip_address}: {ssh_err}")
    finally:
        ssh_client.close()



def write_to_text(ip_address, all_text):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"with_paramiko/hp_{ip_address}_{current_time}.txt"
    with open(file_name, "w") as file:
        file.writelines(all_text)




def login_to_switch(remote_shell):
    send_command_to_switch(remote_shell,command = "_cmdline-mode on")
    send_command_to_switch(remote_shell,command = "y",sleep_time=0)
    output = send_command_to_switch(remote_shell,command = "512900",sleep_time=0)
        
        
    if "Error: Invalid password." in output:
        send_command_to_switch(remote_shell,command = "_cmdline-mode on")
        send_command_to_switch(remote_shell,command = "y", sleep_time=0)
        send_command_to_switch(remote_shell,command = "Jinhua1920unauthorized",sleep_time=0)
        
        
        
def start_self_input_precedure(remote_shell, ip_address):
    while True:
        command = input("command: ")
        if command == "write_to_txt":
            write_to_text(all_text=all_text, ip_address=ip_address)


        output = send_command_to_switch(remote_shell, command = command)
        all_text = ""
        while True:
            output = send_command_to_switch(remote_shell, command = " ")
            all_text += "\n" + output + "\n"        
            if ">" in output:
                break    
        
        print(all_text)

        
        
def start_backup_process():
    ip_addresses = ["172.16.81.1", "172.16.52.1"]
    for ip_address in ip_addresses:
        # collect_current_conf_data(ip_address)
        pass
    
    print("\n Hey, backup process is finished. \n Do you want to continue playing? Y\\N: ", end=" ")
    # key = input()
    key = get_key()
    print()
    if key in "Yy":
        ip_address = input("IP: ")
        ssh_client, remote_shell = connect_to_switch(ip_address)
        start_self_input_precedure(remote_shell, ip_address)          
    else:
        print("Good bye")
    
start_backup_process()
    
    
    