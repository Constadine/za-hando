import streamlit as st
import pandas as pd
from analysis import load_data, calculate_statistics

st.set_page_config(
    page_title="Za-Hando Realm",
    page_icon="🐗",  # You can use an emoji or the URL of an image
    layout="wide",  # You can choose "wide" or "centered"
)


# Load data
df = load_data('Stress insights.xlsx')

# Do math
statistics = calculate_statistics(df)



#  ----------------- START DISPLAY ----------------- #


#-#-# START SIDEBAR #-#-#

toggle_df = st.sidebar.toggle("Show Raw Data")

# Create a sidebar where you can select from all available dates
selected_date = st.sidebar.selectbox("Select Date", df['date'].unique())

# Filter the DataFrame based on the selected date
selected_record = df[df['date'] == selected_date]


#-#-# END SIDEBAR #-#-#

col1, col2, col3 = st.columns([1, 2, 1])  # Create columns with different widths
with col2:
    st.image("zahando.gif", caption="The Hand", use_column_width=True)

# Define the color based on the stress level
if statistics['average_stress_level'] <= 3:
    color = "#68a177"
elif statistics['average_stress_level'] <= 7:
    color = "#bfa76b"
else:
    color = "#bf3232"
    
st.markdown("<h1 style='text-align: center;'>Statistics</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Average Stress Level: <span style='font-size: 24px;'>{:.2f}</span></h2>".format(statistics['average_stress_level']), unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="width: 600px; margin: 0 auto;">
        <div style="background-color: #f1f1f1; border-radius: 5px; padding: 5px;">
            <div style="background-color: {color}; width: {statistics['average_stress_level'] * 10}%; height: 20px; border-radius: 5px; text-align: center; color: white; font-weight: bold; line-height: 20px;">
                {statistics['average_stress_level']}/10
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if statistics['average_night_sleep_quality'] <= 3:
    color = "#bf3232"
elif statistics['average_night_sleep_quality'] <= 7:
    color = "#c2b85f"
else:
    color = "green"
    
st.markdown("<h2 style='text-align: center;'>Average Night Sleep Quality: <span style='font-size: 24px;'>{:.2f}</span></h2>".format(statistics['average_night_sleep_quality']), unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="width: 600px; margin: 0 auto;">
        <div style="background-color: #f1f1f1; border-radius: 5px; padding: 5px;">
            <div style="background-color: {color}; width: {statistics['average_night_sleep_quality'] * 10}%; height: 20px; border-radius: 5px; text-align: center; color: white; font-weight: bold; line-height: 20px;">
                { statistics['average_night_sleep_quality']}/10
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<h2 style='text-align: center;'>Number of Nights to Stretch: <span style='font-size: 24px;'>{}</span></h2>".format(statistics['number_of_nights_to_stretch']), unsafe_allow_html=True)



if toggle_df:
    st.write(df)

# Display the selected record
if not selected_record.empty:
    note_text = selected_record.iloc[0]['notes']
    
    if isinstance(note_text, str):
        # Display the note text with formatting
        st.markdown(f"<h5>On {selected_date} I wrote:</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-style: italic; font-size: 30px;'>\"{note_text}\"</p>", unsafe_allow_html=True)
    else:
        st.warning(f"No notes available for {selected_date}.")
else:
    st.write("No record found for the selected date.")
#  ----------------- END DISPLAY ----------------- #
