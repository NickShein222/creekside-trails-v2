import streamlit as st
import requests
import random
import datetime
import base64
from PIL import Image
import io
import os  
from dotenv import load_dotenv
load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="Creekside Trails", layout="centered")
st.markdown(
    """
    <style>
    body {
        overflow-x: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)



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

trail_images = {
    "Map of William Street to Phelan Avenue": "images/segment1.png",
    "Map of Highway 237 Bikeway to Montague Expressway": "images/segment2.png",
    "Map of Tully Road to Yerba Buena Road": "images/segment3.png",
    "Map of Yerba Buena Road to County jurisdiction": "images/segment4.png",
    "Map of Alignment from Berryessa BART to BRT Santa Clara Street": "images/segment5.png",
    "Map of 'Odette Morrow Trail'": "images/segment6.png",
}


# Two-column layout: Left = Image, Right = Dropdown
col1, col2 = st.columns(2)  # Wider map area

with col1:
    if "trail_select" not in st.session_state:
        st.session_state["trail_select"] = list(trail_images.keys())[0]

    selected_trail = st.session_state["trail_select"]
    st.image(trail_images[selected_trail], use_container_width=True)

with col2:
    st.subheader("📍 Choose a Trail Segment", divider="rainbow")
    selected = st.selectbox(
        "Select a trail segment:",
        list(trail_images.keys()),
        index=list(trail_images.keys()).index(selected_trail),
        key="trail_select"
    )

st.divider()
# --- Weather and Activities ---
api_key = os.getenv("OPENWEATHER_API_KEY")
weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat=37.2294&lon=-121.7796&units=imperial&appid={api_key}"

try:
    weather_data = requests.get(weather_url).json()
    temperature = weather_data["main"]["temp"]
    wind_speed = weather_data["wind"]["speed"]
    description = weather_data["weather"][0]["description"].capitalize()
    icon_code = weather_data["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
except Exception as e:
    st.error("⚠️ Unable to fetch live weather data.")
    temperature = 72
    wind_speed = 5
    description = "Partly Cloudy"
    icon_url = "https://cdn-icons-png.flaticon.com/512/1163/1163661.png"
# Display weather data
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

# --- Popularity & Comfort Score Section ---
st.header("🧠 Trail Comfort & Popularity Score")

# Segment popularity score (based on known risks)
segment_popularity = {
   "Map of William Street to Phelan Avenue": 4,
   "Map of Highway 237 Bikeway to Montague Expressway": 6,
   "Map of Tully Road to Yerba Buena Road": 5,
   "Map of Yerba Buena Road to County jurisdiction": 7,
   "Map of Alignment from Berryessa BART to BRT Santa Clara Street": 8,
   "Map of 'Odette Morrow Trail'": 6
}

# Live crowd prediction based on time of day
hour_of_day = datetime.datetime.now().hour
if 7 <= hour_of_day <= 10:
    crowd_level = 3  # morning low
elif 11 <= hour_of_day <= 16:
    crowd_level = 8  # afternoon peak
else:
    crowd_level = 5  # evening moderate

# Weather impact score (based on live data you fetched earlier)
weather_score = 0
if temperature >= 85:
    weather_score += 2
if "Rain" in description or "Showers" in description:
    weather_score += 3
if wind_speed >= 15:
    weather_score += 1

# Calculate overall score
popularity = segment_popularity.get(selected_trail, 5)
overall_score = crowd_level + popularity + weather_score

# Normalize for progress bar (0-30)
progress_normalized = min(max(overall_score, 0), 30)

# Display comfort score dynamically
if overall_score >= 18:
    st.error(f"🔥 Comfort & Safety Score: {overall_score}/30 – Hot, crowded, and risky conditions today.")
elif overall_score >= 12:
    st.warning(f"⚠️ Comfort & Safety Score: {overall_score}/30 – Conditions are moderate.")
else:
    st.success(f"✅ Comfort & Safety Score: {overall_score}/30 – Great time for a hike!")

# Animated progress bar
progress_bar = st.progress(0)
for percent_complete in range(progress_normalized + 1):
    progress_bar.progress(percent_complete / 30)


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
                    top_speed = species_info.get('Top Speed', 'Unknown')
                    st.markdown(f"**Top Speed:** {top_speed}")
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
                    listen_audio_clicked = st.button("🔊 Generate Audio")

                # --- Handle each button separately ---
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
                    with st.spinner("Generating audio..."):
                        try:
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

                            if audio_response.status_code == 200 and audio_response.content:
                                audio_bytes = audio_response.content
                                b64_audio = base64.b64encode(audio_bytes).decode()

                                audio_html = f"""
                                <div style="text-align:center;">
                                    <audio controls style="width:90%; max-width:500px; margin-top:10px;">
                                        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                                        Your browser does not support the audio element.
                                    </audio>
                                </div>
                                """
                                st.markdown(audio_html, unsafe_allow_html=True)

                                st.download_button(
                                    label="📥 Download Audio",
                                    data=audio_bytes,
                                    file_name="overview.mp3",
                                    mime="audio/mp3"
                                )
                            else:
                                st.error(f"❌ Failed to generate audio. Status code: {audio_response.status_code}")
                                if audio_response.text:
                                    st.error(f"Error details: {audio_response.text}")
                        except Exception as e:
                            st.error(f"❌ Error generating or playing audio: {str(e)}")

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
