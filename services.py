from datetime import datetime
import os


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")



def write_to_text(ip_address, all_text, model="hp"):
    file_name = f"{folder_name}/{model}_{ip_address}_{current_time}.txt"
    with open(file_name, "w") as file:
        file.writelines(all_text)

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
create_folder("with_netmiko")
folder_name = f"with_netmiko/{current_time}"
create_folder(folder_name)
                