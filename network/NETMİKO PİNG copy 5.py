from netmiko import ConnectHandler
import re
import ipaddress

# Switchə qoşulmaq üçün məlumatları daxil edin
switch_ip = input("Daxil olmaq istədiyiniz switchin IP ünvanını daxil edin: ")

def connect_switch(switch_ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'ip':   switch_ip,
        'username': 'admin',
        'password': '!n\\/esT@',
        'secret': '!n\\/esT@',
    }
    # Switchə qoşulun
    net_connect = ConnectHandler(**device)
    print("Switchə uğurla daxil oldunuz.")

    # Enable rejiminə keçin
    net_connect.enable()

    return net_connect


net_connect = connect_switch(switch_ip)

def send_ping(switch_ip, net_connect):
    ip_input = input("Ping etmək istədiyiniz IP ünvanını və ya şəbəkəni daxil edin (məsələn, 172.16.1.1 və ya 172.16.1.1/28): ")
    try:
        net = ipaddress.ip_network(ip_input)
        ips = net.hosts()
    except ValueError:
        ips = [ip_input]

    for ip in ips:
        if str(ip) != switch_ip:  # Switchin özünə ping göndərməmək üçün
            try:
                output = net_connect.send_command(f"ping {ip} repeat 5")
                matches = re.search(r"Success rate is (?P<success_rate>\d+) percent \((?P<success>\d+)/(?P<total>\d+)\), round-trip min/avg/max = (?P<min>\d+)/(?P<avg>\d+)/(?P<max>\d+)", output)

                if matches and int(matches.group('success')) > 0:
                    output = net_connect.send_command(f"ping {ip} repeat 300")
                    matches = re.search(r"Success rate is (?P<success_rate>\d+) percent \((?P<success>\d+)/(?P<total>\d+)\), round-trip min/avg/max = (?P<min>\d+)/(?P<avg>\d+)/(?P<max>\d+)", output)

                    if matches:
                        print(f"IP: {ip}")
                        print(f"Success rate: {matches.group('success_rate')}% ({matches.group('success')}/{matches.group('total')})")
                        print(f"Round-trip min/avg/max: {matches.group('min')}/{matches.group('avg')}/{matches.group('max')} ms")
                        if int(matches.group('success')) < 30:
                            print("Bu IP ünvanı ilə qırılma var. Bu məsələni təcili araşdırın.")
                    else:
                        print(f"IP: {ip}")
                        print("Ping nəticələrini təhlil etmək mümkün olmadı.")
                else:
                    print(f"IP: {ip}")
                    print("Bu IP ünvanı ilə əlaqə yaratmaq mümkün olmadı.")
            except Exception as e:
                print(f"IP: {ip}")
                print("Bu IP ünvanına ping göndərmək mümkün olmadı.")




import textwrap

def format_output(title, content):
    width = max(50, len(title) + 4)
    print(f"{'*' * width}")
    print(f"* {title.center(width - 4)} *")
    print(f"{'*' * width}")
    for line in textwrap.wrap(content, width - 4):
        print(f"* {line.ljust(width - 4)} *")
    print(f"{'*' * width}\n")

def ping_to_neighbors(net_connect):
    output = net_connect.send_command("show interface status")
    interfaces = re.findall(r"(\S+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(.+)", output)
    neighbors = []

    for intf, desc in interfaces:
        output = net_connect.send_command(f"show cdp neighbors {intf} detail")
        ip_address = re.search(r"IP address: (.+)", output)
        if ip_address:
            neighbors.append((intf, desc, ip_address.group(1)))

    for intf, desc, ip in neighbors:
        print(f"Interface: {intf}")
        print(f"Description: {desc}")
        print(f"IP: {ip}")

    ping_test = input("Bu siyahıdakı İP-lərə ping testi edimmi? (Et/Etme): ")
    if ping_test.lower() == 'et':
        for intf, desc, ip in neighbors:
            try:
                output = net_connect.send_command(f"ping {ip} repeat 1000")
                matches = re.search(r"Success rate is (?P<success_rate>\d+) percent \((?P<success>\d+)/(?P<total>\d+)\), round-trip min/avg/max = (?P<min>\d+)/(?P<avg>\d+)/(?P<max>\d+)", output)
                if matches:
                    result = f"IP: {ip}\nSuccess rate: {matches.group('success_rate')}% ({matches.group('success')}/{matches.group('total')})\nRound-trip min/avg/max: {matches.group('min')}/{matches.group('avg')}/{matches.group('max')} ms"
                    if int(matches.group('success')) < 1000:
                        result += "\nBu IP ünvanı ilə qırılma var. Bu məsələni təcili araşdırın."
                else:
                    result = f"IP: {ip}\nPing nəticələrini təhlil etmək mümkün olmadı."
                format_output(f"Interface: {intf} - Description: {desc}", result)
            except Exception as e:
                format_output(f"Interface: {intf} - Description: {desc}", f"IP: {ip}\nBu IP ünvanına ping göndərmək mümkün olmadı.")

# net_connect nümunəsi
# net_connect = NetworkDeviceConnection(...)
# ping_to_neighbors(net_connect)




while True:
    command = input("Komandanı daxil edin (və ya 'P' və ya 'N' daxil edin): ")

    if command.upper() == 'P':
        send_ping(switch_ip, net_connect)

    elif command.upper() == 'N':
        ping_to_neighbors(net_connect)
    else:
        output = net_connect.send_command(command)
        print(output)
