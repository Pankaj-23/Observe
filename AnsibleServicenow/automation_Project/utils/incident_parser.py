import json

def parse_incidents(incident_data):
    """
    Extracts relevant fields from ServiceNow incident data.

    Args:
        incident_data (list): List of incident dictionaries from ServiceNow API.

    Returns:
        List[Dict]: Parsed list of incidents with selected fields.
    """
    parsed = []

    for incident in incident_data:
        parsed_incident = {
            "number": incident.get("number", "N/A"),
            "sys_id": incident.get("sys_id", "N/A"),
            "short_description": incident.get("short_description", "N/A"),
            "state": incident.get("state", "N/A"),
            "priority": incident.get("priority", "N/A"),
            "assigned_to": incident.get("assigned_to", {}).get("display_value", "Unassigned"),
            "opened_at": incident.get("opened_at", "N/A")
        }
        parsed.append(parsed_incident)

    return parsed


def print_incident_summary(parsed_incidents):
    """
    Prints a human-readable summary of parsed incidents.

    Args:
        parsed_incidents (list): List of parsed incidents.
    """
    for inc in parsed_incidents:
        print(f"Incident #{inc['number']} (Priority {inc['priority']})")
        print(f"  Description : {inc['short_description']}")
        print(f"  State       : {inc['state']}")
        print(f"  Assigned to : {inc['assigned_to']}")
        print(f"  Opened at   : {inc['opened_at']}")
        print("----------------------------------------------------")
