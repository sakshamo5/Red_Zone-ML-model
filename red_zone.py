import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder

# Load data
data_path = "Crime_Data.csv"
df = pd.read_csv(data_path)

# Encode categorical variables
label_encoders = {}
categorical_cols = ['Location']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Determine high-risk locations
df['High_Risk'] = df['Frequency_in_Last_30_Days'] > df['Frequency_in_Last_30_Days'].median()
df['High_Risk'] = df['High_Risk'].astype(int)

# Safety options data
safety_options = {
    "Police Station": [
        ("Station A", "https://www.google.com/maps/search/police+station+1"),
        ("Station B", "https://www.google.com/maps/search/police+station+2"),
        ("Station C", "https://www.google.com/maps/search/police+station+3")
    ],
    "Hospital": [
        ("Hospital X", "https://www.google.com/maps/search/hospital+1"),
        ("Hospital Y", "https://www.google.com/maps/search/hospital+2"),
        ("Hospital Z", "https://www.google.com/maps/search/hospital+3")
    ],
    "Safe Haven": [
        ("Community Center 1", "https://www.google.com/maps/search/safe+haven+1"),
        ("Community Center 2", "https://www.google.com/maps/search/safe+haven+2")
    ]
}

# Streamlit UI with custom CSS for background and text color
st.markdown(
    """
    <style>
        body {
            background-color: #D8B6D0; /* Pastel Purple */
            color: black;
        }
        h1, h2, h3, h4, h5, h6 {
            color: black;
        }
        .css-18e3th9 {
            color: black;
        }
    </style>
    """, unsafe_allow_html=True
)

st.title("Red Zone Classifier")
st.write("This is an ML powered web application which classifies different locations on the basis of crime data of that locality.")

# User selects a location
location = st.selectbox("Select Location", ["Select a Location"] + list(label_encoders['Location'].classes_))

if location != "Select a Location":
    # Encode input location
    encoded_location = label_encoders['Location'].transform([location])[0]
    
    # Get risk status from data
    risk_status = df[df['Location'] == encoded_location]['High_Risk'].iloc[0]
    
    # Display result
    st.markdown(f"<h2 style='text-align: center; color: {'red' if risk_status else 'green'};'> {'Red Zone Area' if risk_status else 'Not a Redzone Area'} </h2>", unsafe_allow_html=True)
    
    # Show safety options if high risk
    if risk_status:
        st.subheader("Nearby Safety Options:")
        for key, values in safety_options.items():
            st.write(f"**{key}:**")
            for name, link in values:
                st.markdown(f"- [{name}]({link})")
else:
    st.warning("Please select a location.")  
