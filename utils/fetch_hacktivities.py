"""fetch_hacktivities.py
Summary:
    A script to fetch and interact with hacktivities data from the TryHackMe
    API.

Extended Summary:
    This script provides functionalities to fetch hacktivities data from the
    TryHackMe API, save the response to a JSON file, and display various
    details about the hacktivities.

Returns:
    None: The script doesn't return any value but performs operations based on
    user input.
"""

import logging
import json
import requests

# Set up logging
logging.basicConfig(
    filename='api_interaction.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

API_ENDPOINT = "https://tryhackme.com/api/hacktivities?page="

def fetch_data_from_api(page=1, limit=30):
    """
    Fetch hacktivities data from the TryHackMe API.

    Sends a GET request to the TryHackMe API to retrieve hacktivities data
    based on the specified page and limit. The response is then saved to a JSON
    file.

    Args:
        page (int, optional): The page number to fetch data from. Defaults to 1.
        limit (int, optional): The number of entries to fetch per page.
        Defaults to 30.

    Returns:
        dict: A dictionary containing the parsed JSON data from the API
        response or None if the request fails.
    """
    url = f"{API_ENDPOINT}{page}&limit={limit}"
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        # Save the response to a JSON file
        with open(file='hacktivities.json', mode='w', encoding='utf-8') as file:
            json.dump(response.json(), file)
        logging.info("API response saved to %s.", 'hacktivities.json')
        return response.json()
    logging.error("Failed to fetch data from the API. Status code: %s", response.status_code)
    return None

def display_total_docs(parsed_data):
    """
    Display the total number of documents.

    Prints the total number of documents available in the parsed data.

    Args:
        parsed_data (dict): The parsed JSON data from the API response.
    """
    total_docs = parsed_data["paginator"]["totalDocs"]
    print(f"Total number of documents: {total_docs}")

def list_room_titles(parsed_data):
    """
    List the titles of all rooms.

    Iterates through the parsed data and prints the title of each room.

    Args:
        parsed_data (dict): The parsed JSON data from the API response.
    """
    print("\nList of Room Titles:")
    for room in parsed_data["rooms"]:
        print(room["title"])

def display_room_details(parsed_data, title):
    """
    Display details of a specific room.

    Searches for a room with the specified title in the parsed data and prints
    its details.

    Args:
        parsed_data (dict): The parsed JSON data from the API response.
        title (str): The title of the room whose details are to be displayed.
    """
    for room in parsed_data["rooms"]:
        if room["title"] == title:
            print(f"\nDetails for room '{title}':")
            for key, value in room.items():
                print(f"{key}: {value}")
            break
    else:
        print(f"No room found with title '{title}'.")

def main():
    """
    Main function to drive the script.

    Provides an interactive interface for the user to fetch and interact with
    hacktivities data.
    """
    logging.info("Program started.")
    limit = int(input("Enter the number of entries per page (default is 30): ") or 30)
    page = 1
    while True:
        data = fetch_data_from_api(page, limit)
        if data:
            display_total_docs(data)
            list_room_titles(data)

            action = input(
                "\nChoose an action:"
                "\n1. View room details"
                "\n2. Next page"
                "\n3. Previous page"
                "\n4. Exit"
                "\nEnter your choice: "
            )
            if action == "1":
                room_title = input(
                    "Enter the title of the room you want details for: "
                )
                display_room_details(data, room_title)
            elif action == "2":
                page += 1
            elif action == "3":
                if page > 1:
                    page -= 1
                else:
                    print("You are already on the first page.")
            elif action == "4":
                logging.info("Program exited by user.")
                break
            else:
                print("Invalid choice. Please try again.")
                logging.warning("Invalid choice entered by user.")
        else:
            logging.error("No data received from the API.")

if __name__ == "__main__":
    main()
