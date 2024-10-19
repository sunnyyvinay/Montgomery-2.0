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
section_texts = []

# Base URL for absolute links
base_url = 'https://docs.manim.community/en/stable/'

# Function to extract text content from a link
def extract_text_content(link):
    try:
        full_url = base_url + link
        response = requests.get(full_url)
        if response.status_code == 200:
            page_soup = BeautifulSoup(response.content, 'html.parser')
            # Extract main content text (using an appropriate HTML tag)
            content_div = page_soup.find('div', class_='document')
            if content_div:
                # Extract text and strip unnecessary whitespace
                return content_div.get_text(separator=" ").strip()
            else:
                return "No content found"
        else:
            return "Failed to fetch content"
    except Exception as e:
        return f"Error fetching content: {str(e)}"

# Loop through the main sections
for section in sections:
    section_title = section.a.text.strip()
    
    # Find all subsections inside this section
    subsections = section.find_all('li', class_='toctree-l2')
    
    if subsections:
        for subsection in subsections:
            subsection_title = subsection.a.text.strip()
            subsection_link = subsection.a['href']
            # Extract text content for the subsection
            subsection_text = extract_text_content(subsection_link)
            # Append data to the lists
            section_titles.append(section_title)
            subsection_titles.append(subsection_title)
            links.append(base_url + subsection_link)
            section_texts.append(subsection_text + " --- ")
    else:
        # If there are no subsections, treat the section itself as an entry
        section_titles.append(section_title)
        subsection_titles.append('N/A')
        links.append(base_url + section.a['href'])
        section_texts.append(extract_text_content(section.a['href']) + " --- ")

# Create a DataFrame from the scraped data
data = {
    "Section": section_titles,
    "Subsection": subsection_titles,
    "Link": links,
    "Text": section_texts
}
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv("manim_reference_manual_with_text.csv", index=False)
