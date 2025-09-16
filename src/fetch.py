import requests

url = "https://www.football-data.co.uk/mmz4281/2526/E0.csv"

save_path = "../data/2026.csv"

try:
    response = requests.get(url)
    response.raise_for_status()

    with open(save_path, "wb") as file:
        file.write(response.content)

    print(f"File downloaded and saved to {save_path}")
except requests.exceptions.RequestException as e:
    print(f"Failed to download the file: {e}")