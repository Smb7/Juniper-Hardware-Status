# cleans and processes json data
import json 
import re

f = open('HardWareStatus.json')

data = json.load(f)

f.close()

import re

class AlarmsExtractor:
    def __init__(self, switch_name, ip_address, system_alarms, chassis_alarms, environment_alarms, snmp_alarms, date):
        self.switch_name = switch_name
        self.ip_address = ip_address
        self.system_alarms = system_alarms
        self.chassis_alarms = chassis_alarms
        self.environment_alarms = environment_alarms
        self.snmp_alarms = snmp_alarms
        self.date = date
        self.cleaned_data = {}

    def clean_alarm_status(self, alarm_output):
        """Cleans the alarm output to extract the status and remove unwanted characters."""
        # Use regex to remove everything before the actual alarm message
        clean_output = re.sub(r'.*?\n([^\n]*)\n%', r'\1', alarm_output).strip()
        return clean_output if clean_output else "No alarms"

    def extract_environment_alarms(self):
        """Extracts the first temperature and status from environment alarms."""
        temp_pattern = re.compile(r"(\d+ degrees C / \d+ degrees F)")
        status_pattern = re.compile(r"(OK|Failed)")
        
        temperatures = temp_pattern.findall(self.environment_alarms)
        statuses = status_pattern.findall(self.environment_alarms)

        # Only grab the first temperature and status
        if temperatures and statuses:
            self.cleaned_data["Environment_Alarm"] = {
                "temperature": temperatures[0],
                "status": statuses[0]
            }
        else:
            self.cleaned_data["Environment_Alarm"] = {"temperature": "N/A", "status": "N/A"}

    def extract_chassis_alarms(self):
        """Extract chassis alarm status."""
        self.cleaned_data["Chassis_Alarm"] = self.clean_alarm_status(self.chassis_alarms)

    def extract_snmp_alarms(self):
        """Extracts the first SNMP alarm temperature and status."""
        temp_pattern = re.compile(r"(\d+ degrees C / \d+ degrees F)")
        status_pattern = re.compile(r"(OK|Failed)")
        
        temperatures = temp_pattern.findall(self.snmp_alarms)
        statuses = status_pattern.findall(self.snmp_alarms)

        # Only grab the first temperature and status
        if temperatures and statuses:
            self.cleaned_data["SNMP_Alarm"] = {
                "temperature": temperatures[0],
                "status": statuses[0]
            }
        else:
            self.cleaned_data["SNMP_Alarm"] = {"temperature": "N/A", "status": "N/A"}

    def extract_system_alarms(self):
        """Extract system alarm status."""
        self.cleaned_data["System_Alarm"] = self.clean_alarm_status(self.system_alarms)

    def generate_json_format(self):
        """Generates the final JSON formatted data in a specific order."""
        self.cleaned_data = {
            "Switch_Name": self.switch_name,
            "Switch_IP": self.ip_address,
            "Date": self.date,
            "System_Alarm": self.cleaned_data["System_Alarm"],
            "Chassis_Alarm": self.cleaned_data["Chassis_Alarm"],
            "Environment_Alarm": self.cleaned_data.get("Environment_Alarm", {}),
            "SNMP_Alarm": self.cleaned_data.get("SNMP_Alarm", {}),
        }
        return self.cleaned_data

    def extract_all_alarms(self):
        """Runs all extraction methods."""
        self.extract_system_alarms()
        self.extract_chassis_alarms()
        self.extract_environment_alarms()
        self.extract_snmp_alarms()
        return self.generate_json_format()

def cleaned_data(): 
    formatted_results = []
    for switch_name, switch_data in data.items():
        ip_address = switch_data["IP_Address"]
        chassis_alarms = switch_data["chassis_alarms"]
        environment_alarms = switch_data["environment_alarms"]
        snmp_alarms = switch_data["snmp_alarms"]
        system_alarms = switch_data["system_alarms"]
        date = switch_data["date"]

        extractor = AlarmsExtractor(
            switch_name, 
            ip_address, 
            system_alarms, 
            chassis_alarms, 
            environment_alarms, 
            snmp_alarms, 
            date
        )
        
        formatted_data = extractor.extract_all_alarms()
        formatted_results.append(formatted_data)

    JsonCleanedData = json.dumps(formatted_results, indent=4)  # Assign the entire formatted_results to JsonCleanedData
    print(JsonCleanedData)
    return JsonCleanedData

cleaned_data()