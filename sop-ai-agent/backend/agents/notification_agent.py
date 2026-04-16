import os
import json

def check_notification(region_mentioned: str | None) -> dict | None:
    if not region_mentioned:
        return None
        
    config_path = os.path.join(os.path.dirname(__file__), "..", "notifications", "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        contacts = config.get("region_contacts", {})
        contact = contacts.get(region_mentioned, config.get("default_contact"))
        
        if contact:
            return {
                "person_in_charge": contact["person"],
                "role": contact["role"],
                "message": f"Query addressed metrics relating to {region_mentioned}."
            }
    except Exception as e:
        print(f"Failed handling notification config: {e}")
    return None
