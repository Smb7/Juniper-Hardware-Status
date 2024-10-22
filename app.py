# this gets the data from each of the switches
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.start_shell import StartShell
import json
from datetime import datetime

switch_names = {
    "IP address" : "Switch name"
}

filePath = [
    r"filepath for rsa key"
    ]


results = {}

for host, key_file in zip(switch_names, filePath):
    print(f"Connecting to {host} with key {key_file}")
    try:
        dev = Device(
            host=host,
            user='username',
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
