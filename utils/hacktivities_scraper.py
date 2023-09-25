import requests
import json

API_ENDPOINT = "https://tryhackme.com/api/hacktivities?limit=40&page="

def scrape_and_save_to_file(page=1, total_pages=18, filename='./json/hacktivities_all.json'):
    """
    Recursively scrape text from the webpage and save to a file.

    Fetches data from the TryHackMe API for each page up to the specified total_pages.
    Appends the response to a JSON file.

    Args:
        page (int, optional): The starting page number. Defaults to 1.
        total_pages (int, optional): The total number of pages to scrape. Defaults to 18.
        filename (str, optional): The name of the file to save the data. Defaults to 'hacktivities_all.json'.
    """
    if page > total_pages:
        return

    url = f"{API_ENDPOINT}{page}"
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        # Append the response to a JSON file
        with open(file=filename, mode='a', encoding='utf-8') as file:
            json.dump(response.json(), file)
            file.write("\n")
        # Recursively call the function for the next page
        scrape_and_save_to_file(page=page+1, total_pages=total_pages, filename=filename)
    else:
        print(f"Failed to fetch data for page {page}. Status code: {response.status_code}")

# Call the function to start the scraping process
scrape_and_save_to_file()
