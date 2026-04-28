import requests
from bs4 import BeautifulSoup
import os

# --- Configuration ---
# The main product page URL
PRODUCT_URL = "https://cycletees.co/products/ride-bikes-pet-cats-t-shirt"
# The specific meta tag property we are looking for (the primary image for sharing/display)
META_TAG_PROPERTY = "og:image"
# ---------------------

def extract_primary_image_url(url, meta_property):
    """
    Fetches the HTML of the product page and extracts the URL from the
    standard Open Graph 'og:image' meta tag.
    """
    print(f"Fetching HTML from: {url}")
    
    try:
        # 1. Fetch the HTML content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise exception for bad status codes
        
        # 2. Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 3. Find the specific meta tag
        # The Open Graph image tag typically looks like: <meta property="og:image" content="[IMAGE_URL]">
        image_meta_tag = soup.find('meta', property=meta_property)
        
        if image_meta_tag:
            image_url = image_meta_tag.get('content')
            print("\n--- Extraction Successful ---")
            print(f"Primary Image URL found via '{meta_property}' tag:")
            return image_url
        else:
            print(f"Error: Could not find the <meta property='{meta_property}'> tag.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    image_link = extract_primary_image_url(PRODUCT_URL, META_TAG_PROPERTY)
    
    if image_link:
        print(f"\n{image_link}")
        
        # You can now easily feed this link into the download script from before.
        print("\nReady to be used for downloading (e.g., with 'requests.get(image_link)').")
