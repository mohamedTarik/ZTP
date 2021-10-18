import csv
from jinja2 import Template
from netmiko import ConnectHandler

switch = {'ip': '192.168.30.70', 'user': 'kit', 'pass': 'kit123'}
print("Connecting...\n")

conn = ConnectHandler(secret='kit123', ip=switch['ip'], username=switch['user'], password=switch['pass'],
                      device_type='cisco_ios')
conn.enable()
print("Connected")

vlan_csv = "vlan.csv"
vlan_temp = "vlan-template.j2"

with open(vlan_temp) as j:
    v_template = Template(j.read(), keep_trailing_newline=True)

interface_configs = ""
with open(vlan_csv) as f:
    read = csv.DictReader(f)
    for row in read:
        # put all the expected variables for template inside render function
        vlan_config = v_template.render(

            vlanNumber=row["vlanNumber"],
            vlanName=row["vlanName"]
        )
        print(vlan_config)
        interface_configs += vlan_config
        config_set = interface_configs.split('\n')

# config_set must be a list
print(config_set)
x = conn.send_config_set(config_set)
print(x)
print("Done...")

with open("interface_configs.txt", "w") as w:
    w.write(interface_configs)


import ansible

