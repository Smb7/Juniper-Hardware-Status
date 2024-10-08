# this gets the data from each of the switches
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.start_shell import StartShell
import json
from datetime import datetime

switch_names = {
    "10.0.0.2" : "MDF Switch",
    "192.168.254.3" : "IDF3 Switch",
    "192.168.254.4" : "IDF4 Switch",
    "192.168.254.5" : "IDF5 Switch",
    "192.168.254.6" : "IDF6 Switch",
    "192.168.254.7" : "IDF7 Switch",
    "192.168.254.8" : "IDF8 Switch",
    "192.168.254.9" : "IDF9 Switch",
    "192.168.254.11" : "IDF11 Switch"
}

filePath = [
    r"C:\Users\shaneb\.ssh\mdf",
    r"C:\Users\shaneb\.ssh\idf3",
    r"C:\Users\shaneb\.ssh\idf4",
    r"C:\Users\shaneb\.ssh\idf5",
    r"C:\Users\shaneb\.ssh\idf6",
    r"C:\Users\shaneb\.ssh\idf7",
    r"C:\Users\shaneb\.ssh\idf08",
    r"C:\Users\shaneb\.ssh\idf9",
    r"C:\Users\shaneb\.ssh\idf11"
    ]


results = {}

for host, key_file in zip(switch_names, filePath):
    print(f"Connecting to {host} with key {key_file}")
    try:
        dev = Device(
            host=host,
            user='sbrennan',
            ssh_private_key_file=key_file,
            port=22
        )
        dev.open()
        ss = StartShell(dev)
        ss.open()

        system_alarms = ss.run('cli -c "show system alarms"')
        chassis_alarms = ss.run('cli -c "show chassis alarms"')
        environment_alarms = ss.run('cli -c "show chassis environment"')
        snmp_alarms = ss.run('cli -c "show snmp mib walk jnxAlarms"')

        ss.close()
        dev.close()

        results[switch_names.get(host, "Unknown Switch")] = {
            "IP_Address": host,
            "system_alarms": system_alarms[1],
            "chassis_alarms": chassis_alarms[1],
            "environment_alarms": environment_alarms[1],
            "snmp_alarms": snmp_alarms[1],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Successfully retrieved data from {host}")

    except ConnectError as e:
        print(f"Error connecting to {host}: {e}")

# Write the results to a JSON file
with open('HardWareStatus.json', 'w') as f:
    json.dump(results, f, indent=4, sort_keys=True)

print("Successfully created json file with alarms data from all switches.")
