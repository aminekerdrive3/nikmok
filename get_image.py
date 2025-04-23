import os
import requests
from dotenv import load_dotenv

def get_car_image(car_description):
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv("PEXELS_API_KEY")
        
        # Pexels API endpoint
        url = "https://api.pexels.com/v1/search"
        
        # Search parameters
        params = {
            "query": car_description,
            "per_page": 1,
            "orientation": "landscape"
        }
        
        headers = {
            "Authorization": api_key
        }
        
        # Make the request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # Get image URL from response
        data = response.json()
        if data["photos"]:
            image_url = data["photos"][0]["src"]["large"]
            
            # Download the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_path = os.path.join(os.path.dirname(__file__), "generated_car.jpg")
                with open(image_path, "wb") as f:
                    f.write(image_response.content)
                return image_path
        
        return None
        
    except Exception as e:
        print(f"Error getting image: {e}")
        return None
