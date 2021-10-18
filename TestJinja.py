import csv
from jinja2 import Template
from netmiko import ConnectHandler

switch = {'ip': '192.168.30.70', 'user': 'kit', 'pass': 'kit123'}
print("Connecting...\n")

conn = ConnectHandler(secret='kit123', ip=switch['ip'], username=switch['user'], password=switch['pass'],
                      device_type='cisco_ios')
conn.enable()
print("Connected")

interfaces_csv = "interfaces.csv"
interface_temp = "switchport-template.j2"
all_configs = " "

with open(interface_temp) as j:
    interface_template = Template(j.read(), keep_trailing_newline=True)

type(interface_template)
with open(interfaces_csv) as f:
    read = csv.DictReader(f)
    for vlan_row in read:
        interface_config = interface_template.render(
            Interface=vlan_row["interface"],
            Description=vlan_row["description"],
            Trunk=vlan_row["trunk"],
            Vlan=vlan_row["vlan"])
        all_configs += interface_config

config_set = all_configs.split('\n')
print(config_set)
conn.send_config_set(config_set, exit_config_mode=False)
