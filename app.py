import streamlit as st
import requests
import json
import os
from datetime import datetime
from openai import OpenAI

# API Keys (Replace with your own)
NASA_API_KEY = "bhdKicgOsCgszzYCgSlnkNERrhXAbeJakSTTf5E8"
DEEPSEEK_API_KEY = "sk-2b6025fa93fa431697334b0d9422a502"

# Initialize OpenAI (DeepSeek) client
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def fetch_apod(date):
    """Fetch NASA APOD data for the given date."""
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        st.error("❌ Invalid date! Please enter a correct date (YYYY-MM-DD).")
    else:
        st.error(f"❌ Error fetching data: {response.status_code}")

    return None

def generate_fortune_story(description):
    """Generate a mystical fortune story from DeepSeek AI using APOD description."""
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
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )

        return response.choices[0].message.content if response.choices else "No story generated."

    except Exception as e:
        st.error(f"❌ Failed to get a story from DeepSeek AI: {str(e)}")
        return None

def save_results_to_json(result):
    """Save results to a JSON file."""
    file_path = "nasa_apod_results.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(result)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# 🎨 **Streamlit Web App**
st.title("🔭 NASA APOD Fortune Teller")
st.write("Enter your birth date to see the Astronomy Picture of the Day and receive your space-inspired fortune!")

birth_date = st.text_input("Enter your birth date (YYYY-MM-DD):")

if st.button("🔮 Get My Fortune"):
    try:
        datetime.strptime(birth_date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        st.error("❌ Invalid date format! Please use YYYY-MM-DD.")
    else:
        apod_data = fetch_apod(birth_date)
        if apod_data:
            st.subheader("🌌 NASA Astronomy Picture of the Day")
            st.markdown(f"📅 **Date:** {apod_data['date']}")
            st.markdown(f"🌟 **Title:** {apod_data['title']}")
            st.markdown(f"📖 **Explanation:** {apod_data['explanation']}")

            # Display APOD Image
            image_url = apod_data.get("hdurl", apod_data.get("url", ""))
            if image_url:
                st.image(image_url, caption=apod_data["title"], use_column_width=True)
            else:
                st.warning("⚠ No image available for this date.")

            # Generate Fortune Story
            st.subheader("🔮 Your Space-Inspired Fortune")
            fortune_story = generate_fortune_story(apod_data["explanation"])
            st.write(fortune_story)

            # Save result
            result = {
                "date": apod_data['date'],
                "title": apod_data['title'],
                "image_url": image_url,
                "fortune_story": fortune_story
            }
            save_results_to_json(result)
