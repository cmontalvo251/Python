import requests
import os

def download_image(url, filename):
    """Downloads an image from a URL and saves it to a file."""
    print(f"Starting download from: {url}")

    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Check if the content is likely an image before proceeding
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image'):
            print(f"Error: URL does not point to an image. Content-Type: {content_type}")
            return

        # Write the content in chunks to the file
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    file.write(chunk)

        print(f"Successfully downloaded image to: {os.path.abspath(filename)}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Define the URL of the T-shirt image to download
    IMAGE_URL = "https://cycletees.co/cdn/shop/files/ride-bikes-pet-cats-t-shirt-white-s-cycletees-1169113145.png?v=1751891165&width=600"
    # Let's automatically determine a filename from the URL
    FILENAME = os.path.basename(IMAGE_URL.split("?")[0])
    # Print to inform the user
    print(f"Downloading T-shirt image from: {IMAGE_URL}, saving as: {FILENAME}")
    # Download the image
    download_image(IMAGE_URL, FILENAME)
