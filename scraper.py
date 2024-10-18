import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL for the Manim Reference Manual
url = 'https://docs.manim.community/en/stable/reference.html'

# Send an HTTP request to get the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Page fetched successfully.")
else:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all sections from the reference manual
sections = soup.find_all('li', class_='toctree-l1')

# Prepare lists to store extracted data
section_titles = []
subsection_titles = []
links = []

# Loop through the main sections
for section in sections:
    section_title = section.a.text.strip()
    
    # Find all subsections inside this section
    subsections = section.find_all('li', class_='toctree-l2')
    
    if subsections:
        for subsection in subsections:
            subsection_title = subsection.a.text.strip()
            subsection_link = subsection.a['href']
            # Append data to the lists
            section_titles.append(section_title)
            subsection_titles.append(subsection_title)
            links.append(subsection_link)
    else:
        # If there are no subsections, treat the section itself as an entry
        section_titles.append(section_title)
        subsection_titles.append('N/A')
        links.append(section.a['href'])

# Create a DataFrame from the scraped data
data = {
    "Section": section_titles,
    "Subsection": subsection_titles,
    "Link": links
}
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv("manim_reference_manual.csv", index=False)

# Optionally, also save to Excel
df.to_excel("manim_reference_manual.xlsx", index=False)

print("Data successfully saved to manim_reference_manual.csv and manim_reference_manual.xlsx")