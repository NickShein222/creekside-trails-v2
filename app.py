# app.py

import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Creekside Trails", layout="wide")

# --- Hero Section ---
with st.container():
    st.markdown(
        """
        <div style="position:relative;height:90vh;background:url('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHZjcmViYnFtZmU2aW5wMDhkdW8yN2Zkcm9xb2c5cmNvZXBrZGN4NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o85xEfx9JC73A6gq4/giphy.gif') center/cover no-repeat;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:white;">
            <div style="background:rgba(0,0,0,0.4);padding:20px;border-radius:10px;">
                <h1>Welcome to Creekside Trails</h1>
                <p>Explore nature with AI — learn, hike, and protect.</p>
                <a href="#trail-map"><button style="padding:10px 20px;background:#006d77;color:white;border:none;border-radius:8px;">Start Your Hike</button></a>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

# --- Trail Map and Activities ---
st.markdown('<h2 id="trail-map">Trail Map</h2>', unsafe_allow_html=True)
st.components.v1.iframe(
    "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d202920.38280712665!2d-122.01206433141502!3d37.374907650948714!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x808fc9bf5ad06955%3A0xd837faeefb7f0591!2sGuadalupe%20River%20Trail!5e0!3m2!1sen!2sus!4v1744240543990!5m2!1sen!2sus",
    height=400,
    width=700
)
st.button("Start Tracking My Hike")

st.divider()

# --- Weather & Challenges ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Weather")
    st.image("https://cdn-icons-png.flaticon.com/512/1163/1163661.png", width=60)
    st.write("🌎 **Location:** Santa Clara Trails")
    st.write("🌡️ **Temperature:** 72°F")
    st.write("⛅ **Description:** Partly Cloudy")
    st.success("Trail Status: Open")

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

    import random
    activities = random.sample(allActivities, 5)

    for activity in activities:
        st.info(activity)

    if st.button("🔄 Refresh Activities"):
        st.experimental_rerun()

st.divider()

# --- Identify Species Section ---
st.header("Identify Species")

uploaded_file = st.file_uploader("Take a photo to identify plants and wildlife", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    with st.spinner("Identifying species..."):
        files = {"image": uploaded_file.getvalue()}
        response = requests.post("https://api.inaturalist.org/v1/computervision/score_image", files=files)

        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                top_result = data["results"][0]
                species_name = top_result["taxon"]["name"]
                common_name = top_result["taxon"].get("preferred_common_name", "Unknown")
                photo_url = top_result["taxon"]["default_photo"]["square_url"] if "default_photo" in top_result["taxon"] else None

                st.success(f"Common Name: {common_name}")
                st.write(f"Scientific Name: *{species_name}*")

                if photo_url:
                    st.image(photo_url, width=150)
            else:
                st.error("No species identified. Try a clearer picture.")
        else:
            st.error("Failed to identify species. Please try again.")

st.divider()

# --- Smart Audio Guide ---
st.header("Smart Audio Guide")
col1, col2 = st.columns(2)

with col1:
    st.subheader("👧🧒 Kids Audio Guide")
    st.write("Fun and educational trail stories for kids!")

with col2:
    st.subheader("👩🧑 Adults Audio Guide")
    st.write("Engage with deeper nature insights for adults!")

# --- Emergency Bar ---
st.markdown(
    """
    <div style="background:#d00000;color:white;text-align:center;padding:10px;font-weight:bold;position:fixed;bottom:0;width:100%;z-index:1000;">
        🚨 Emergency SOS
    </div>
    """, unsafe_allow_html=True
)
