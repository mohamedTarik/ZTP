from jinja2 import Template
from netmiko import ConnectHandler
from pythonping import ping
import csv
import time
import speedtest

switch = {'ip': '192.168.30.70', 'user': 'kit', 'pass': 'kit123'}
# it will be CSV file also
Switch_MAC = " "

Open_interfaces_template = "switchport-template.j2"
Open_interfaces_CSV = "interfaces.csv"

Open_vlans_template = "vlan-template.j2"
Open_vlans_CSV = "vlan.csv"

while True:
    replay = ping(switch["ip"], count=1)
    if replay.success():
        print("Please Wait While Connecting")
        time.sleep(40)
        try:
            print("Connecting to {0}".format(switch["ip"]))
            conn = ConnectHandler(secret='kit123', ip=switch['ip'], username=switch['user'], password=switch['pass'],
                                  device_type='cisco_ios')
            conn.enable()
            print("Connected to {0}".format(switch["ip"]))
            MAC_Table = conn.send_command("show mac address-table")
            MAC_List = MAC_Table.split(' ')
            if "Vl1" in MAC_List:
                index = MAC_List.index("Vl1")
                # RestConf
                MAC_index = index - 10
                Switch_MAC = MAC_List[MAC_index]

            if Switch_MAC == "6c03.09a3.20c7":
                with open(Open_vlans_template) as z:
                    vlan_template = Template(z.read(), keep_trailing_newline=True)

                with open(Open_vlans_CSV) as w:
                    vlan_configs = " "
                    vlan_csv = csv.DictReader(w)
                    for vlan_row in vlan_csv:
                        vlan_config = vlan_template.render(Vlan=vlan_row["vlan"], Name=vlan_row["name"])
                        vlan_configs += vlan_config

                with open(Open_interfaces_template) as j:
                    interface_template = Template(j.read(), keep_trailing_newline=True)

                with open(Open_interfaces_CSV) as f:
                    interfaces_csv = csv.DictReader(f)
                    interface_configs = " "
                    all_configs = " "
                    for interface_row in interfaces_csv:
                        interface_config = interface_template.render(Interface=interface_row["interface"],
                                                                     Vlan=interface_row["vlan"],
                                                                     Descrption=interface_row["description"],
                                                                     Trunk=interface_row["trunk"])
                        interface_configs += interface_config

                conn.send_config_set(["hw-module beacon on switch 1"])

                all_configs = interface_configs + vlan_configs

                config_set = all_configs.split('\n')

                conn.send_config_set(config_set, exit_config_mode=False)
        except:
            print("Please Wait ..")
        break
    else:
        print("{0} is down ".format(switch["ip"]))
        continue
