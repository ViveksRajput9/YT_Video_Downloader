import threading
import json
from pathlib import Path

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__initialize()
            return cls._instance

    def __initialize(self):
        self.meta_data_path = Path.home() / '.ytdownloader' / 'MetaData.json'

    def get_json(self, json_path=None):
        """Load JSON data from file."""

        if self.meta_data_path.exists():
            try:
                with open(self.meta_data_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error reading JSON file: Invalid format")
                return []
            except Exception as e:
                print(f"Error loading JSON: {e}")
                return []
        return []  # Return an empty array if the file doesn't exist

    def __save_json(self, json_path=None, dictionary=None):
        """Save JSON data to file."""
        if json_path is None:
            json_path = self.meta_data_path

        try:
            with open(json_path, 'w') as f:
                json.dump(dictionary, f, indent=2)
                return True
        except Exception as e:
            print(f"Failed to save data: {e}")
            return False

    def add_item(self, item:dict) -> str:
        """Add item to the JSON list if not already present."""
        if not item:
            return "Invalid item data"
        response = self.get_json()
        
        id = item.get('id')
        if id :
           data = {id:item}
           response.append(data)
           return "Item added successfully" if self.__save_json(self.meta_data_path, response) else "Failed to save item"
        else:
            return "id is None"
    def remove_item(self, json_path=None, item=None) -> str:
        """Remove item from the JSON list."""
        if not item:
            return "Invalid item data"

        response = self.get_json(json_path)

        if item not in response:
            return "Item not available"

        response.remove(item)
        return "Item removed successfully" if self.__save_json(json_path, response) else "Failed to remove item"

    def update_item(self, json_path=None, old_item=None, new_item=None) -> str:
        """Update an item in the JSON list."""
        if not old_item or not new_item:
            return "Invalid item data"

        response = self.get_json(json_path)

        if old_item not in response:
            return "Item not found"

        response.remove(old_item)  # Remove old item
        response.append(new_item)  # Add updated item

        return "Item updated successfully" if self.__save_json(json_path, response) else "Failed to update item"

    def clear_json(self, json_path=None) -> str:
        """Clear all JSON data."""
        return "Data cleared successfully" if self.__save_json(json_path, []) else "Failed to clear data"

    def get_data_by_id(self, video_id):
        response = self.get_json()  # Load JSON data
        if not response:
            return False
        for data in response:
            if not isinstance(data, dict):  # Ensure each item is a dictionary
                continue  # Skip invalid entries        
            if video_id == data.get("id", ""):  # Check if the video ID matches
                return data  # Stop searching once found & return data
        return False