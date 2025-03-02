import requests
from bs4 import BeautifulSoup
import json
import csv

# Base URL of your blog
BASE_URL = "https://nepalprabin.github.io"

# Function to fetch all blog links from the main page
def get_blog_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Assuming blog links are in <a> tags within a specific section or class
    blog_links = [
        base_url + a["href"]
        for a in soup.find_all("a", href=True)
        if "/posts/" in a["href"]
    ]
    return list(set(blog_links))

# Function to scrape content from an individual blog post
def scrape_blog_content(blog_url):
    response = requests.get(blog_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract blog title
    title = soup.find("h1").get_text(strip=True)
    
    # Find the main content container (adjust this selector to match your blog structure)
    # This might be an article tag, div with class "content", etc.
    content_container = soup.find("article") or soup.find("div", class_="content") or soup.find("main")
    
    # If we can't find a specific container, use the body
    if not content_container:
        content_container = soup.body
    
    # Initialize an empty list to store content elements in order
    content_elements = []
    
    # Process all direct children of the content container in order
    for element in content_container.find_all(['p', 'pre', 'h2', 'h3', 'h4', 'ul', 'ol'], recursive=True):
        if element.name == 'pre':
            # This is likely a code block
            code_content = element.get_text()
            content_elements.append({"type": "code", "content": code_content})
        elif element.name in ['h2', 'h3', 'h4']:
            # Section headers
            header_text = element.get_text(strip=True)
            content_elements.append({"type": "header", "content": header_text, "level": int(element.name[1])})
        elif element.name in ['ul', 'ol']:
            # List items
            list_items = [li.get_text(strip=True) for li in element.find_all('li')]
            list_text = "\n".join([f"- {item}" for item in list_items])
            content_elements.append({"type": "list", "content": list_text})
        else:
            # Regular paragraph text
            para_text = element.get_text(strip=True)
            if para_text:  # Only add non-empty paragraphs
                content_elements.append({"type": "text", "content": para_text})
    
    # Create a structured representation that maintains the original flow
    return {
        "source": blog_url,
        "title": title,
        # Add a full text version that combines everything in order
        "full_text": "\n\n".join([
            title,
            *[elem["content"] for elem in content_elements]
        ])
    }

# Main function to create the dataset
def create_dataset(base_url):
    dataset = []
    blog_links = get_blog_links(base_url)
    
    for link in blog_links:
        try:
            print(f"Scraping: {link}")
            blog_data = scrape_blog_content(link)
            dataset.append(blog_data)
        except Exception as e:
            print(f"Failed to scrape {link}: {e}")
    
    return dataset

# Save dataset to JSON file
def save_to_json(data, filename="blog_dataset.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_to_csv(data, filename="blog_dataset.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "full_text", "title"])
        writer.writeheader()
        writer.writerows(data)

# Run the scraper
if __name__ == "__main__":
    print("Starting scraper...")
    dataset = create_dataset(BASE_URL)
    save_to_json(dataset)
    save_to_csv(dataset)
    print("Scraping complete. Dataset saved to 'blog_dataset.json'.")
    print("Scraping complete. Dataset saved to 'blog_dataset.csv'.")
