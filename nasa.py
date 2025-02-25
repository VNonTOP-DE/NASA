import requests
import os
from colorama import Fore, Style, init
from datetime import datetime
from openai import OpenAI
# Initialize colorama
init(autoreset=True)

# API Keys (Replace with your own)
NASA_API_KEY = "bhdKicgOsCgszzYCgSlnkNERrhXAbeJakSTTf5E8"  # Replace with your NASA API key
DEEPSEEK_API_KEY = "sk-2b6025fa93fa431697334b0d9422a502"  # Replace with your DeepSeek AI key

# NASA APOD API Request
def fetch_apod(date):
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        print(Fore.RED + "❌ Invalid date! Please enter a correct date (YYYY-MM-DD).")
    else:
        print(Fore.RED + f"❌ Error fetching data: {response.status_code}")
    
    return None

# DeepSeek AI Request for Fortune-Telling Story


# Initialize OpenAI client
client = OpenAI(api_key="sk-2b6025fa93fa431697334b0d9422a502", base_url="https://api.deepseek.com")

# ...

# DeepSeek AI Request for Fortune-Telling Story
def generate_fortune_story(description):
    prompt = (f"Turn this space event description into a human curiosity-driven story, predicting fate and emotions: "
              f"'{description}'. Make it sound mystical, rare, and full of wonder.")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        
        return response.choices[0].message.content if response.choices else "No story generated."
    
    except Exception as e:
        print(Fore.RED + f"❌ Failed to get a story from DeepSeek AI: {str(e)}")
        return None

# ...

# Download Image
def download_image(image_url, date):
    if not image_url:
        print(Fore.YELLOW + "⚠ No image available for this date.")
        return

    image_name = f"{date}.jpg"
    image_path = os.path.join(os.getcwd(), image_name)

    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(Fore.GREEN + f"📥 Image downloaded as: {image_name}")
    else:
        print(Fore.RED + "❌ Failed to download image.")

# Main CLI Function
def main():
    print(Fore.CYAN + "🔭 Welcome to the NASA APOD Fortune Teller 🔭")
    birth_date = input(Fore.YELLOW + "Enter your birth date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(birth_date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        print(Fore.RED + "❌ Invalid date format! Please use YYYY-MM-DD.")
        return

    apod_data = fetch_apod(birth_date)

    if apod_data:
        print("\n🌌 " + Fore.MAGENTA + Style.BRIGHT + "NASA Astronomy Picture of the Day 🌌")
        print(Fore.CYAN + f"📅 Date: {apod_data['date']}")
        print(Fore.LIGHTBLUE_EX + f"🌟 Title: {apod_data['title']}")
        print(Fore.GREEN + f"📷 Image URL: {apod_data.get('hdurl', apod_data.get('url', 'No image'))}")

        # Download image
        download_image(apod_data.get('hdurl', apod_data.get('url', None)), birth_date)

        # Generate Fortune Story
        print("\n🔮 " + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Your Space-Inspired Fortune 🔮")
        fortune_story = generate_fortune_story(apod_data["explanation"])
        print(Fore.LIGHTCYAN_EX + fortune_story if fortune_story else "✨ The universe is silent today, but the stars still shine for you. ✨")

if __name__ == "__main__":
    main()
