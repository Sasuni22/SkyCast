
# run the code using streamlit run weather_app.py
import streamlit as st
import requests

# ---------------- CONFIG ----------------
API_KEY = "b091d3e7c7564539dcbe51c988e555f8"  # Replace with your OpenWeatherMap API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SkyCast 🌦️", page_icon="🌤️", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #f0f8ff;}
    h1 {color: #2E86C1; text-align: center; margin-bottom: 0px;}
    .card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-top: 5px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>SkyCast 🌦️</h1>", unsafe_allow_html=True)
st.write("Get **real-time weather updates** for any city around the world!")

# ---------------- INPUT ----------------
city_name = st.text_input("Enter city name:")
unit = st.radio("Select Unit", ["Celsius", "Fahrenheit"])

# ---------------- BUTTON ----------------
if st.button("Get Weather"):
    if city_name:
        units = "metric" if unit == "Celsius" else "imperial"
        url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={units}"
        response = requests.get(url)

        try:
            data = response.json()
            if data["cod"] != "404":
                main = data["main"]
                weather = data["weather"][0]
                icon_code = weather["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

                # Dynamic background color
                condition = weather['main'].lower()
                if "cloud" in condition:
                    bg_color = "#d3d3d3"
                elif "rain" in condition or "drizzle" in condition:
                    bg_color = "#a3c2c2"
                elif "clear" in condition:
                    bg_color = "#87ceeb"
                else:
                    bg_color = "#f0f8ff"

                st.markdown(f"<div style='background-color:{bg_color}; padding:10px; border-radius:15px;'>", unsafe_allow_html=True)
                st.subheader(f"Weather in {city_name}")
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.image(icon_url, width=100)
                with col2:
                    st.write(f"🌡️ **Temperature:** {main['temp']}°{unit[0]}")
                    st.write(f"💧 **Humidity:** {main['humidity']} %")
                    st.write(f"🔼 **Pressure:** {main['pressure']} hPa")
                    st.write(f"🌡️ **Feels like:** {main['feels_like']}°{unit[0]}")
                    st.write(f"🌥️ **Condition:** {weather['description'].capitalize()}")

                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.error("❌ City not found!")
        except:
            st.error("❌ Error fetching data!")
    else:
        st.warning("Please enter a city name!")
