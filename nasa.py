import json
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
    prompt = (f"Craft a mystical, poetic birthday analysis inspired by the celestial imagery of the Perseid meteor shower. "
              f"Use the following elements from this description as symbolic guides: '{description}'\n\n"
              f"Structure the analysis with:\n"
              f"- A mystical title and core theme\n"
              f"- Opening paragraph with vivid cosmic metaphors\n" 
              f"- 3-4 major opportunities as bullet points\n"
              f"- Celestial cycles section linking to life areas\n"
              f"- Star ratings for Personal Growth, Wealth, Health, Love, Family\n"
              f"- Closing with actionable cosmic wisdom\n\n"
              f"Make it enchanting yet empowering, blending cosmic wonder with grounded guidance.")

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

        # Save results to JSON
        result = {
            "date": apod_data['date'],
            "title": apod_data['title'],
            "image_url": apod_data.get('hdurl', apod_data.get('url', 'No image')),
            "fortune_story": fortune_story
        }

        save_results_to_json(result)

def save_results_to_json(result):
    file_path = "nasa_apod_results.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(result)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()