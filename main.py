# Imports
from get_car import generate_car
from get_image import get_car_image
from publish_pic import post_to_instagram
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask

# Create html using pre-made template
def generate_html(title, image_url):

    # Read the template HTML file
    with open('template.html', 'r') as file:
        html_template = file.read()

    # Replace placeholders with generated content
    html_content = html_template.replace('{{ title }}', title).replace('{{ image_url }}', image_url)

    # Save the edited HTML to new file
    with open('car_news.html', 'w') as file:
        file.write(html_content)

    print("\nHTML file 'car_news.html' has been generated.")

    return 'car_news.html'

# Screenshot the generated html and save as png
def generate_image_from_html(html_file, car_info):
    try:
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1200x800")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Use newer service setup
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Initialize the Chrome driver with updated options
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
        # Get current directory and setup paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_html_file = f'file:///{os.path.join(current_dir, html_file).replace(os.sep, "/")}'
        screenshot_path = os.path.join(current_dir, "generated_pic.png")
        
        # Take screenshot
        driver.get(input_html_file)
        time.sleep(2)  # Wait for page to load
        driver.save_screenshot(screenshot_path)
        driver.quit()
        
        print(f"Screenshot saved as {screenshot_path}")
        return screenshot_path
        
    except Exception as e:
        print(f"Error generating image from HTML: {e}")
        return None

def create_app():
    app = Flask(__name__)
    
    @app.route('/generate', methods=['POST'])
    def generate_post():
        # Generate info to be used in car post
        news_title, car_name, caption = generate_car()
        
        if car_name != "Unknown Car":
            # Get image using generated car name
            image_path = get_car_image(car_name)
            
            if image_path:
                print(f"\nImage generated successfully at: {image_path}")
                    
                # Generate html file with title and image path
                html_file = generate_html(news_title, image_path)
                
                # Generate png image from html file
                screenshot_path = generate_image_from_html(html_file, car_name)
                
                if screenshot_path:
                    # Post pic to Instagram
                    username = os.getenv("USER")
                    password = os.getenv("PASSWORD")
                    ig_caption = f"{caption}\n\n#cars #automotive #carlife"
                    post_to_instagram(username, password, screenshot_path, ig_caption)
                    return {"status": "success", "message": "Post created successfully"}
            
            return {"status": "error", "message": "Failed to generate image"}, 500
        
        return {"status": "error", "message": "No valid car name extracted"}, 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return {"status": "healthy"}

    return app

# Keep the main() function for local development
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app = create_app()
    app.run(host='0.0.0.0', port=port)
