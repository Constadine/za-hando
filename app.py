import streamlit as st
import pandas as pd
from analysis import load_data, calculate_statistics, calculate_correlation_matrix, find_most_stressful_time_of_day
from plots import create_heatmap

st.set_page_config(
    page_title="Za-Hando Realm",
    page_icon="🖐",  # You can use an emoji or the URL of an image
    layout="wide",  # You can choose "wide" or "centered"
)


### Load data
df = load_data('Stress insights.xlsx')

###---- Do math ----###
statistics = calculate_statistics(df)

# Calculate correlation matrix
correlation_matrix = calculate_correlation_matrix(df)

# Get the top three factors for increased stress
top_factors = correlation_matrix['average_stress_meter'].sort_values(ascending=False)[1:4]

# Create a list to store formatted strings for each factor
formatted_factors = []

# Iterate over the top factors DataFrame
for i, (factor, correlation) in enumerate(top_factors.items(), 1):
    # Format the factor name and correlation coefficient
    formatted_factor = f"{i}) <b>{factor.capitalize()}</b> ({correlation:.2f} correlation)"
    # Append the formatted string to the list
    formatted_factors.append(formatted_factor)

# Join the formatted strings with line breaks
formatted_factors_string = "<br>".join(formatted_factors)

# Find the most stressful time of day
most_stressful_time = find_most_stressful_time_of_day(df)

#  ----------------- START DISPLAY ----------------- #


    #-#-# START SIDEBAR #-#-#

toggle_df = st.sidebar.toggle("Show Raw Data")

# Create a sidebar where you can select from all available dates
selected_date = st.sidebar.selectbox("Select Date", df['date'].unique())

# Filter the DataFrame based on the selected date
selected_record = df[df['date'] == selected_date]


    #-#-# END SIDEBAR #-#-#

         #..::__MAIN_::..#

# Display the selected record
if not selected_record.empty:
    note_text = selected_record.iloc[0]['notes']
    
    if isinstance(note_text, str):
        # Display the note text with formatting
        st.sidebar.markdown(f"<h5>On {selected_date} I wrote:</h5>", unsafe_allow_html=True)
        st.sidebar.markdown(f"<p style='text-align: center; font-style: italic; font-size: 30px;'>\"{note_text}\"</p>", unsafe_allow_html=True)
    else:
        st.warning(f"No notes available for {selected_date}.")
else:
    st.write("No record found for the selected date.")
    

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
    
st.markdown("<hr>", unsafe_allow_html=True)
    
st.markdown("<h1 style='text-align: center;'>Statistics</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Average Stress Level: <span style='font-size: 24px;'>{:.2f}</span></h2>".format(statistics['average_stress_level']), unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="width: 600px; margin: 0 auto;">
        <div style="background-color: #f1f1f1; border-radius: 5px; padding: 5px;">
            <div style="background-color: {color}; width: {statistics['average_stress_level'] * 10}%; height: 20px; border-radius: 5px; text-align: center; color: white; font-weight: bold; line-height: 20px;">
                {round(statistics['average_stress_level'],2)}/10
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
                {round(statistics['average_night_sleep_quality'],2)}/10
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<h2 style='text-align: center;'>Number of Nights to Stretch:</h2>"
            f"<p style='text-align: center; font-size:25px'>{statistics['number_of_nights_to_stretch']} out of {len(df)}</p>", unsafe_allow_html=True)

# Display the sentence with the formatted top factors
st.markdown(f"<h2 style='text-align: center;'>Most stressful time of day:</h2>"
            f"<p style='text-align: center; font-size:25px'>{most_stressful_time.capitalize()}</p>", unsafe_allow_html=True)

# GRAPHS
st.markdown("<hr>", unsafe_allow_html=True)


if toggle_df:
    st.write(df)

st.markdown("<h1 style='text-align: center;'>Graphs</h1>", unsafe_allow_html=True)

# Create heatmap visualization
heatmap_fig = create_heatmap(correlation_matrix)

# Display heatmap
st.plotly_chart(heatmap_fig, use_container_width=True)


    #..::__END MAIN_::..#


#  ----------------- END DISPLAY ----------------- #
