import requests
import json
import re

# Base URL of your API
BASE_URL = "https://web-production-d1ba5.up.railway.app"


def fetch_notifications_by_type(notification_type):
    """Fetches all notifications of a given type from the API."""
    url = f"{BASE_URL}/notifications/{notification_type}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["notifications"]
    else:
        print(f"Error: {response.json().get('error', 'Unknown error')}")
        return None


def extract_placeholders(template):
    """Extracts placeholders from a notification template (e.g., {item_name})."""
    return re.findall(r'\{(.*?)\}', template)


def fill_placeholders(template):
    """Prompts user to input values for placeholders and fills them in."""
    placeholders = extract_placeholders(template)

    if not placeholders:
        return template  # No placeholders, return as is

    user_inputs = {}
    for placeholder in placeholders:
        user_inputs[placeholder] = input(f"Enter value for {placeholder}: ")

    return template.format(**user_inputs)


def main():
    """CLI Menu"""
    print("Welcome to the NotiFetch API Demo!")

    while True:
        notification_type = input(
            "\nEnter notification type (e.g., stock, system, user, alert) or 'quit' to exit: ").strip()

        if notification_type.lower() == "quit":
            print("Exiting... Goodbye! 👋")
            break  # Exit the loop

        notifications = fetch_notifications_by_type(notification_type)

        if not notifications:
            print("No notifications found.")
            continue  # Ask the user again

        print("\nAvailable Notifications:")
        for i, notif in enumerate(notifications, 1):
            print(f"{i}. {notif['template']}")

        while True:
            try:
                choice = input(
                    "\nSelect a notification to customize (enter number) or 'back' to choose another type: ").strip()
                if choice.lower() == "back":
                    break  # Go back to selecting a notification type

                choice = int(choice) - 1
                if choice < 0 or choice >= len(notifications):
                    print("Invalid selection. Please enter a valid number.")
                    continue

            except ValueError:
                print("Invalid input. Please enter a number or 'back'.")
                continue

            selected_template = notifications[choice]["template"]
            print("\nFilling in placeholders...")
            final_message = fill_placeholders(selected_template)

            print("\n✅ Customized Message:")
            print(final_message)

            # Ask the user if they want to continue
            again = input("\nDo you want to generate another notification? (yes/no): ").strip().lower()
            if again != "yes":
                print("Exiting... Goodbye! 👋")
                return  # Exit the program


if __name__ == "__main__":
    main()
