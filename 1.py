import requests
from bs4 import BeautifulSoup
import os

def create_directory_structure(root_path, data):
    for entry in data:
        name = entry["name"]
        path = os.path.join(root_path, name)

        if entry["type"] == "file":
            with open(path, 'w'): pass  # Create an empty file
        else:
            os.makedirs(path)
            if "subdirectories" in entry:
                create_directory_structure(path, entry["subdirectories"])

def parse_modmaven_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    entries = []

    for link in soup.find_all('a', href=True):
        entry = {"name": link["href"], "type": "directory"}
        if link["href"].endswith('/'):
            entry["subdirectories"] = parse_modmaven_page(url + link["href"])
        else:
            entry["type"] = "file"
        entries.append(entry)

    return entries

if __name__ == "__main__":
    modmaven_url = "https://modmaven.dev/"  # Adjust URL if needed
    modmaven_data = parse_modmaven_page(modmaven_url)
    create_directory_structure(".", modmaven_data)
  
