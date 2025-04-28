import streamlit as st
import requests
import random
import datetime
import base64
from PIL import Image
import os  
from dotenv import load_dotenv
load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="Creekside Trails", layout="wide")

# --- Hero Section ---
with st.container():
    st.markdown("""
    <div style="position:relative;height:90vh;background:url('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHZjcmViYnFtZmU2aW5wMDhkdW8yN2Zkcm9xb2c5cmNvZXBrZGN4NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o85xEfx9JC73A6gq4/giphy.gif') center/cover no-repeat;
    display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:white;">
        <div style="background:rgba(0,0,0,0.4);padding:20px;border-radius:10px;">
            <h1>Welcome to Creekside Trails</h1>
            <p>Explore nature with AI — learn, hike, and protect.</p>
            <a href="#trail-map">
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Trail Segments ---
st.markdown('<h2 id="trail-map">Trail Segments</h2>', unsafe_allow_html=True)

trail_data = {
    "Map of William Street to Phelan Avenue": {"image": "images/segment1.png", "risk": 4},
    "Map of Highway 237 Bikeway to Montague Expressway": {"image": "images/segment2.png", "risk": 6},
    "Map of Tully Road to Yerba Buena Road": {"image": "images/segment3.png", "risk": 5},
    "Map of Yerba Buena Road to County jurisdiction": {"image": "images/segment4.png", "risk": 7},
    "Map of Alignment from Berryessa BART to BRT Santa Clara Street": {"image": "images/segment5.png", "risk": 8},
    "Map of 'Odette Morrow Trail'": {"image": "images/segment6.png", "risk": 6},
}

left_col, right_col = st.columns([1, 2])
with left_col:
    st.subheader("📍 Choose a Trail Segment")
    selected_trail = st.selectbox("Select a trail segment:", list(trail_data.keys()))
segment = trail_data[selected_trail]
with right_col:
    st.image(segment["image"], use_container_width=True, caption=selected_trail)

st.divider()

# --- AI Risk Score ---
# --- Combined AI Popularity & Live Weather Comfort Score ---
st.header("🧠 Trail Comfort & Weather Score")

# --- Predict Crowd Level Based on Time ---
hour_of_day = datetime.datetime.now().hour
if 7 <= hour_of_day <= 10:
    crowd_level = 3  # Low morning crowds
elif 11 <= 16:
    crowd_level = 8  # Peak daytime crowds
else:
    crowd_level = 5  # Evening medium

# --- Segment Popularity Adds to Risk ---
segment_popularity = segment["risk"]  # Using your "risk" as segment popularity proxy
crowd_score = min(round((crowd_level + segment_popularity) / 2), 10)

# --- Live Weather Fetch (Santa Clara / Coyote Creek Area) ---
api_key = "283c59d61c54b7d0c71676885db453f8"
weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat=37.2294&lon=-121.7796&units=imperial&appid={api_key}"

try:
    weather_data = requests.get(weather_url).json()

    temperature = weather_data["main"]["temp"]
    wind_speed = weather_data["wind"]["speed"]
    description = weather_data["weather"][0]["description"].capitalize()
    icon_code = weather_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

except Exception as e:
    st.error("⚠️ Unable to fetch live weather data. Comfort score may not be accurate.")
    temperature = 72  # fallback
    wind_speed = 5    # fallback
    description = "Partly Cloudy"
    icon_url = "https://cdn-icons-png.flaticon.com/512/1163/1163661.png"


except Exception as e:
    st.error("⚠️ Unable to fetch live weather data. Comfort score may not be accurate.")
    temperature = 72  # fallback
    wind_speed = 5    # fallback (safe value)
    description = "Partly Cloudy"
    icon_url = "https://cdn-icons-png.flaticon.com/512/1163/1163661.png"

# --- Weather Factors ---
weather_score = 0
if temperature >= 85:
    weather_score += 2  # hot
if "rain" in description.lower():
    weather_score += 3  # rain
if wind_speed >= 15:
    weather_score += 1  # windy

# --- Final Overall Score ---
overall_score = crowd_score + weather_score

if overall_score >= 12:
    st.error(f"🔥 Comfort & Safety Score: {overall_score}/20 – Hot, crowded, and risky conditions today.")
    st.markdown("""
    - 🥵 Consider waiting until evening
    - 💧 Stay hydrated and rest often
    - 🧑‍🤝‍🧑 Expect high trail traffic
    """)
elif overall_score >= 7:
    st.warning(f"⚠️ Comfort & Safety Score: {overall_score}/20 – Conditions are moderate.")
    st.markdown("""
    - 😅 May be warm or lightly crowded
    - 📅 Consider off-peak times
    - 👟 Trail might be damp or breezy
    """)
else:
    st.success(f"✅ Comfort & Safety Score: {overall_score}/20 – Great time for a hike!")
    st.markdown("""
    - 🌞 Ideal temperature and clear skies
    - 🧘‍♂️ Low crowd conditions
    - 🌲 Enjoy the peace and trail space
    """)


st.divider()

# --- Weather and Activities ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Current Weather")
    st.image(icon_url, width=100)
    st.write("🌎 **Location:** Coyote Creek Trail")
    st.write(f"🌡️ **Temperature:** {temperature}°F")
    st.write(f"⛅ **Condition:** {description}")
    st.success("Trail Status: Open")  # You can later make this dynamic too if you want



with col2:
    st.subheader("Trail Activities")
    allActivities = [
        "📸 Take a picture of the prettiest flower you see",
        "🐦 Try to spot a bird and note its color",
        "🥾 Find a uniquely shaped rock",
        "🌳 Touch the bark of a tree and describe how it feels",
        "🛤️ Take a path you've never tried before",
        "🌼 Find 3 different types of flowers",
        "🍂 Pick up 1 piece of trash",
        "🐾 Look for animal footprints on the trail",
        "💧 Listen carefully — can you hear water nearby?",
        "🌲 Hug a tree and close your eyes for 10 seconds",
        "🔍 Spot a butterfly or bee",
        "☀️ Feel the temperature of a sunny vs shaded spot",
        "🧘‍♂️ Sit quietly for 2 minutes and just listen to nature",
        "🛶 Find something floating in a creek or stream",
        "🐜 Watch a line of ants moving and guess what they're carrying"
    ]
    activities = random.sample(allActivities, 5)
    for activity in activities:
        st.info(activity)
    if st.button("🔄 Refresh Activities"):
        st.rerun()

st.divider()

# --- Identify Species Section (OpenAI Vision API) ---
st.header("Identify Species")

st.info("📷 Upload a photo to identify plants or animals. After identification, you can explore more pictures, learn more facts, or listen to an audio!")

uploaded_file = st.file_uploader("Take a photo to identify plants and wildlife", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    with st.spinner("🔎 Identifying species using AI..."):
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            st.error("❌ API key not found. Please set the OPENAI_API_KEY environment variable.")
            st.stop()
        else:
            image_bytes = uploaded_file.getvalue()
            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a wildlife expert. Identify the species from the image and respond with: \nName:\nOverview:\nTop Speed:\nFun Fact:"
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Please identify the species and give Name, Overview, Top Speed, Fun Fact."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 700,
                },
            )

            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]

                # Parse AI reply
                lines = ai_reply.split("\n")
                species_info = {}
                for line in lines:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        species_info[key.strip()] = value.strip()

                st.success("🌱 Species Identified!")
                col1, col2 = st.columns([1, 1])

                with col1:
                        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

                with col2:
                        st.markdown(f"### 🦋 {species_info.get('Name', 'Unknown')}")
                        st.markdown(f"**Overview:** {species_info.get('Overview', 'No overview available.')}")
                        
                        # Top Speed displayed as simple text (NOT a metric box)
                        top_speed = species_info.get('Top Speed', 'Unknown')
                        st.markdown(f"**Top Speed:** {top_speed}")

                        # Fun Fact
                        st.info(f"Fun Fact: {species_info.get('Fun Fact', 'N/A')}")


                # --- AFTER Upload and AI Results: Show Action Buttons ---
                st.divider()
                st.subheader("Explore More:")

                button_col1, button_col2, button_col3 = st.columns(3)

                with button_col1:
                    more_pic_clicked = st.button("📸 See More Pictures")

                with button_col2:
                    learn_more_clicked = st.button("🔎 Learn More About It")

                with button_col3:
                    listen_audio_clicked = st.button("🔊 Listen to Overview")

                # Handle button actions
                if more_pic_clicked:
                    st.subheader("🖼️ AI-Generated Picture")
                    dalle_response = requests.post(
                        "https://api.openai.com/v1/images/generations",
                        headers={
                            "Authorization": f"Bearer {openai_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "dall-e-3",
                            "prompt": f"A realistic beautiful high-quality photograph of a {species_info.get('Name', 'animal')} in the wild",
                            "n": 1,
                            "size": "1024x1024",
                            "response_format": "url"
                        }
                    )

                    if dalle_response.status_code == 200:
                        dalle_image_url = dalle_response.json()['data'][0]['url']
                        st.image(dalle_image_url, caption="Generated by AI", use_container_width=True)
                    else:
                        st.error("❌ Failed to generate image. Try again.")

                if learn_more_clicked:
                    st.subheader("📚 Detailed Information")
                    learn_more_response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {openai_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "gpt-4o",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": f"You are a wildlife expert. Provide detailed facts, behavior, interesting traits, and conservation status about a {species_info.get('Name', 'animal')}."
                                },
                                {
                                    "role": "user",
                                    "content": "Tell me more in a friendly detailed paragraph."
                                }
                            ],
                            "max_tokens": 1000,
                        }
                    )

                    if learn_more_response.status_code == 200:
                        detailed_info = learn_more_response.json()['choices'][0]['message']['content']
                        st.write(detailed_info)
                    else:
                        st.error("❌ Failed to fetch more info. Try again.")

                if listen_audio_clicked:
                    st.subheader("🎧 Overview Audio")
                    audio_response = requests.post(
                        "https://api.openai.com/v1/audio/speech",
                        headers={
                            "Authorization": f"Bearer {openai_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "tts-1",
                            "input": species_info.get('Overview', 'This is a species overview.'),
                            "voice": "nova",
                            "response_format": "mp3"
                        }
                    )

                    if audio_response.status_code == 200:
                        st.audio(audio_response.content, format="audio/mp3")
                    else:
                        st.error("❌ Failed to generate audio.")

            else:
                st.error("❌ Failed to identify species. Please try again.")

else:
    # No upload: don't show anything
    pass


# --- Emergency Bar ---
st.markdown("""
<div style="background:#d00000;color:white;text-align:center;padding:10px;font-weight:bold;
position:fixed;bottom:0;width:100%;z-index:1000;">
   🚨 Emergency SOS
</div>
""", unsafe_allow_html=True)
