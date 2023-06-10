import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the website
url = "https://en.wikipedia.org/wiki/List_of_political_parties_in_Malaysia"
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with ID "hello"
table = soup.find('table', {'class': 'wikitable'})

# Extract the table data into a list of lists
data = []
rows = table.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    data.append([cell.text.strip() for cell in cells])

# Create a Pandas dataframe from the table data
df = pd.DataFrame(data)

# Save the dataframe as a CSV file
csv_file = './data/coalitions_07062023.csv'
df.to_csv(csv_file, index=False)
print(df)
print("Scraping and saving to CSV completed successfully.")
