import joblib
import pandas as pd
import streamlit as st
from data_organizing_func import organizer

# Web Design
st.set_page_config(
    page_title="CarbonTrack", 
    page_icon="🌿",  
    layout="centered",  
)
@st.cache_data
def get_custom_css():
    return """
        <style>
        /* Genel Sayfa Ayarları */
        .stApp {
            background: linear-gradient(to bottom, #e8f5e9, #f1f8e9); /* Yeşil beyaz gradient arka plan */
            color: #2e7d32; /* Doğal yeşil ton */
            font-family: 'Roboto', sans-serif; /* Modern yazı fontu */
        }

        /* Başlık ve Alt Başlıklar */
        .main-title {
            color: #1b5e20; /* Güçlü koyu yeşil ton */
            font-size: 3.5rem;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        .sub-title {
            color: #4caf50; /* Yumuşak yeşil ton */
            font-size: 1.8rem;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Kart Tasarımı */
        .info-card {
            background-color: #ffffff;
            border: 1px solid #c8e6c9;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: 20px auto;
            max-width: 900px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .info-card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }
        .info-card h3 {
            color: #1b5e20; /* Derin koyu yeşil ton */
            font-size: 1.8rem;
            margin-bottom: 10px;
        }
        .info-card p {
            color: #4a4a4a;
            font-size: 1rem;
            line-height: 1.6;
        }

        /* Buton Stili */
        .stButton button {
            background-color: #2e7d32; /* Güçlü koyu yeşil */
            color: white;
            font-size: 16px;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .stButton button:hover {
            background-color: #1b5e20; /* Daha koyu yeşil */
            transform: scale(1.05);
        }

        /* Sonuç Gösterimi */
        .result-box {
            background-color: #c8e6c9;
            border-left: 6px solid #2e7d32;
            padding: 20px;
            margin: 30px 0;
            font-size: 1.25rem;
            color: #2e7d32;
            border-radius: 8px;
        }
        .result-highlight {
            color: #d32f2f; /* Vurgulu kırmızı */
            font-weight: bold;
        }

        /* Açıklama Stili */
        .description {
            background-color: #c8e6c9; /* Açık yeşil arka plan */
            color: #1b5e20; /* Koyu yeşil yazı rengi */
            padding: 10px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            margin-bottom: 10px;
            display: inline-block;
        }
        /* Radio Butonları Şıkları için Stil */
        div.stRadio > div > label {
            background-color: #c8e6c9; /* Açık yeşil arka plan */
            padding: 8px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            margin-bottom: 9px;
            display: inline-block;
            transition: background-color 0.3s ease, color 0.3s ease; /* Hover geçiş efektleri */
        }

        /* Radio Butonları Hover Durumu */
        div.stRadio > div > label:hover {
            background-color: #a5d6a7; /* Daha açık yeşil hover arka plan */
            color: #1b5e20; /* Koyu yeşil yazı rengi */
        }
        hr.custom-divider {
            border: 2;
            height: 2px; /* Çizgi kalınlığı */
            background: linear-gradient(to right, #c8e6c9, #1b5e20); /* Renk geçişi */
            margin: 20px 0; /* Üst ve alt boşluk */
        }
        /* Multi-Select Container Stil */
        div[data-baseweb="select"] {
            background-color: #c8e6c9; /* Açık yeşil arka plan */
            border-radius: 10px;
            border: 2px solid #1b5e20; /* Koyu yeşil çerçeve */
            padding: 5px;
            color: #1b5e20; /* Yazı rengi */
            font-weight: bold;
            transition: box-shadow 0.3s ease, transform 0.2s ease;
        }
        div[data-baseweb="select"]:hover {
            box-shadow: 0 0 5px #1b5e20; /* Hover efekti */
            transform: scale(1.01); /* Hafif büyüme efekti */
        }

        /* Seçilen Öğeler İçin Stil */
        div[data-baseweb="tag"] {
            background-color: #a5d6a7; /* Hafif açık yeşil */
            color: #1b5e20; /* Yazı rengi */
            font-weight: bold;
            border-radius: 5px;
            padding: 2px 5px;
        }

        /* Çarpı İşareti (Silme Butonu) */
        div[data-baseweb="tag"] svg {
            color: #1b5e20; /* Çarpı rengini yeşil yap */
        }
        </style>
    """   

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Carbon Emission Calculator 🍀</h1>', unsafe_allow_html=True)

st.markdown("""
    <div class="info-card">
        <h3>How does this calculator work?</h3>
        <p>
            This tool helps you estimate your yearly carbon emissions based on your daily habits, 
            including transport, diet, and energy consumption. Make environmentally conscious choices 
            and reduce your impact on the planet.
        </p>
    </div>
""", unsafe_allow_html=True)

# Options and descriptions for each category if needed

ordinal_data_info = {
    'Diet': {
        'options': ['vegan', 'vegetarian', 'pescatarian', 'omnivore'],
        'description': "Choose your diet style:"
    },
    'How Often Shower': {
        'options': ['less frequently', 'daily', 'twice a day', 'more frequently'],
        'description': "How often do you shower?"
    },
    'Heating Energy Source': {
        'options': ['electricity', 'wood', 'natural gas', 'coal'],
        'description': "What energy source do you use to get warm at home?"
    },
    'Transport': {
        'options': ['walk/bicycle', 'public', 'private'],
        'description': "What is your main mode of transport?"
    },
    'Social Activity': {
        'options': ['never', 'sometimes', 'often'],
        'description': "How often do you participate in social activities?"
    },
    'Frequency of Traveling by Air': {
        'options': ['never', 'rarely', 'frequently', 'very frequently'],
        'description': "How frequently do you travel by air?"
    },
    'Monthly Grocery Bill': {
        "number input": "",
        'description': "How much do you spend on groceries each month? (Enter amount in currency)"
    },
    'Waste Bag Size': {
        'options': ['small', 'medium', 'large', 'extra large'],
        'description': "What size of plastic bag do you use?"
    },
    "Waste Bag Weekly Count": {
        "number input": "",
        'description': "How many plastic bags do you use weekly?"
    },
    'How Long TV PC Daily Hour': {
        "number input": "",
        'description': "How many hours do you spend in front of a TV or PC each day? (Enter hours)"
    },
    'How Long Internet Daily Hour': {
        "number input": "",
        'description': "How many hours do you spend on the internet each day? (Enter hours)"
    },
    'How Many New Clothes Monthly': {
        "number input": "",
        'description': "How many new clothes do you buy each month? (Enter number of clothes)"
    },
    'Energy efficiency': {
        'options': ['Yes', 'Sometimes', 'No'],
        'description': "Do you prioritize energy efficiency in your household?"
    },
    'Recycling': {
        "multi select": ['Paper', 'Plastic', 'Glass', 'Metal'],
        'description': "Which ones do you recycle?"
    },
    'Cooking_With': {
        "multi select": ['Stove', 'Oven', 'Microwave', 'Grill', 'Airfryer'],
        'description': "Which ones do you use for cooking?"
    },
    "Carbon Emission": {
        "none": ""
    }
}
# Getting info from user
user_info = {
    "Body Type": "",
    "Sex": "",
    "Diet": "",
    "How Often Shower": "",
    "Heating Energy Source": "",
    "Transport": "",
    "Vehicle Type": "",
    "Social Activity": "",
    "Monthly Grocery Bill": "",
    "Frequency of Traveling by Air": "",
    "Vehicle Monthly Distance Km": "",
    "Waste Bag Size": "",
    "Waste Bag Weekly Count": "",
    "How Long TV PC Daily Hour": "",
    "How Many New Clothes Monthly": "",
    "How Long Internet Daily Hour": "",
    "Energy efficiency": "Yes",
    "Recycling": "",
    "Cooking_With": "",
}

currencies = {"Dolar":1,"Turkish Lira": 34.50,"Euro":0.95} 

st.markdown(
    """
    <h1 style='text-align: center;'>Life Habits Test</h1>
    """,
    unsafe_allow_html=True
)

# Special asking for gender
st.markdown(f'<div class="description">Select your gender:</div>', unsafe_allow_html=True)
user_info['Sex'] = st.radio("", options=["male", "female"], key="gender_radio",label_visibility="collapsed")

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# Special asking for body type
st.markdown('<div class="description">Please enter your weight (in kg):</div>', unsafe_allow_html=True)
weight = st.slider("", min_value=30.0, max_value=160.0, step=0.5, key="weight_slider",)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

st.markdown('<div class="description">Please enter your height (in cm):</div>', unsafe_allow_html=True)
height = st.slider("", min_value=100, max_value=220, step=1, key="height_slider")

bmi = round(weight / ((height / 100) ** 2), 2)
if bmi < 18.5:
    user_info['Body Type'] = "underweight"
elif 18.5 <= bmi < 24.9:
    user_info['Body Type'] = "normal"
elif 25 <= bmi < 29.9:
    user_info['Body Type'] = "overweight"
else:
    user_info['Body Type'] = "obese"

# Getting the questions and the options for the user info with the loop
for category, info in ordinal_data_info.items():
    if category == "Body Type":
        continue  # This one is completed below

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    if category == "Transport":
        st.markdown(f'<div class="description">{info["description"]}</div>', unsafe_allow_html=True,)
        user_info[category] = st.radio("", options=info['options'], key=f"{category}_radio",label_visibility="collapsed")
        
        # Selecting the public or walk/bicycle option indicates the person does not own a personal vehicle.
        if user_info[category] == "private":
            st.markdown('<div class="description">What type of vehicle do you use?</div>', unsafe_allow_html=True)
            user_info['Vehicle Type'] = st.radio(
                "", 
                options=['electric', 'hybrid', 'lpg', 'petrol', 'diesel'],
                key="vehicle_type_radio",
                label_visibility="collapsed"
            )
        else:
            user_info['Vehicle Type'] = None
            
        # Distance traveled by walking or cycling does not affect carbon emissions.
        if user_info[category] in ["public", "private"]:
            st.markdown('<div class="description">How much do you travel in a month (km)?</div>', unsafe_allow_html=True)
            user_info["Vehicle Monthly Distance Km"] = int(st.number_input("", min_value=5, max_value=9999, key="vehicle_distance_input",))
        else:
            user_info['Vehicle Monthly Distance Km'] = 0
    
    else:
        # Seperate each category that contains options, slider, multi-select or number input
        if 'options' in info:
            st.markdown(f'<div class="description">{info["description"]}</div>', unsafe_allow_html=True,)
            user_info[category] = st.radio("", options=info['options'], key=f"{category}_radio")
            
        elif "multi select" in info:
            st.markdown(f'<div class="description">{info["description"]}</div>', unsafe_allow_html=True,)
            user_info[category] = str(st.multiselect("", info["multi select"], key=f"{category}_amount"))

        elif "number input" in info:
            if category == "Monthly Grocery Bill":
                st.markdown(f'<div class="description">Which currency are you using?</div>', unsafe_allow_html=True,)
                parity = st.radio("", ["Turkish Lira", "Dolar", "Euro"], key="currency_radio")
                st.markdown(f'<div class="description">{info["description"]}</div>', unsafe_allow_html=True,)
                amount = int(st.number_input("", step=1, key=f"{category}_amount"))  # Benzersiz key
                user_info[category] = int(amount // currencies[parity])
            else:
                st.markdown(f'<div class="description">{info["description"]}</div>', unsafe_allow_html=True,)
                user_info[category] = st.number_input("", step=1, key=f"{category}_input")  # Benzersiz key

#  Calculating
@st.cache_resource
def load_model():
    return joblib.load("final_xgb_model.pkl")

if st.button("Calculate"):
    user_info_df = pd.DataFrame([user_info])
    organized = organizer(user_info_df)
    model = load_model()
    prediction = model.predict(organized)
    st.markdown(f"""
        <div class="result-box">
            Your estimated yearly carbon emission is <span class="result-highlight">{prediction[0]:.2f} kg CO₂</span>.
        </div>
    """, unsafe_allow_html=True)



# Github and Linkedin Connections
st.markdown("""
    <style>
    .social-icons {
        position: absolute;
        top: 20px; 
        right: 20px;
        display: flex;
        gap: 10px;
    }
    .social-icons a {
        text-decoration: none;
        color: white;
        font-weight: bold;
        padding: 9px 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
        font-size: 14px;
    }
    .linkedin {
        background-color: #0077B5;
    }
    .linkedin:hover {
        background-color: #005582;
    }
    .github {
        background-color: #333333;
    }
    .github:hover {
        background-color: #24292e;
    }
    </style>

    <div class="social-icons">
        <a href="https://www.linkedin.com/in/ahmedhfz/" target="_blank" class="linkedin">LinkedIn</a>
        <a href="https://github.com/ahmedhfz" target="_blank" class="github">GitHub</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<span style="color:#1e4466; font-size:18px;">**Feedback**</span> ➤ **atakan.hfz@hotmail.com** 📧  
""", unsafe_allow_html=True)