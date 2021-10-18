from jinja2 import Template
from netmiko import ConnectHandler
from pythonping import ping


switch = {'ip': '192.168.30.70', 'user': 'admin', 'pass': 'cisco'}
print("Connecting...\n")

conn = ConnectHandler(secret='kit123', ip=switch['ip'], username=switch['user'], password=switch['pass'],
                      device_type='cisco_ios')
conn.enable()
print("Connected")
file = "interfaces.csv"
template = "switchport-template.j2"

with open(template) as j:
    interface_template = Template(j.read(), keep_trailing_newline=True)
interface_configs = ""
with open(file) as f:
    read = csv.DictReader(f)
    for row in read:
        # put all the expected variables for template inside render function
        interface_config = interface_template.render(
            Interface=row["Interface"],
            Vlan=row["Vlan"],
            Descrption=row["Descrption"],
            Trunk=row["Trunk"]
        )
        interface_configs += interface_config
        config_set = interface_configs.split('\n')

# config_set must be a list
print(config_set)
conn.send_config_set(config_set, exit_config_mode=False)
print("Done...")

with open("interface_configs.txt", "w") as w:
    w.write(interface_configs)