import pandas as pd

def load_data(filename):   
    df = pd.read_excel('Stress insights.xlsx')
    
    df.dropna(subset=['average_stress_meter'], inplace=True)
    
    columns_to_replace_numbers = ['plans_for_today', 'plans_for_next_days', 'study', 'work',
    'walk_in_nature', 'gym', 'caffeine', 'silence', 'stretch_breathing']
    df[columns_to_replace_numbers] = df[columns_to_replace_numbers].replace({0: False, 1:True})
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    
    return df

def calculate_statistics(df):
    statistics = {
        'average_stress_level': df['average_stress_meter'].mean(),
        'average_night_sleep_quality': df['last_night_sleep_quality'].mean(),
        'number_of_nights_to_stretch': len(df[df['stretch_breathing'] == True])
    }
    return statistics


def calculate_correlation_matrix(df):
    col_to_drop = ['date','most_stressful_time_of_day', 'notes', 'positive_events', 'negative_events']
    df = df.drop(columns=col_to_drop)
    df.dropna(inplace=True)
    # Convert boolean columns to numeric (0 or 1)
    boolean_columns = ['plans_for_today', 'plans_for_next_days', 'study', 'work', 'walk_in_nature', 'gym', 'caffeine', 'silence', 'stretch_breathing']
    for column in boolean_columns:
        df[column] = df[column].astype(int)
    
    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    return correlation_matrix 

def find_most_stressful_time_of_day(df):
    # Remove leading and trailing whitespaces from the 'most_stressful_time_of_day' column
    df['most_stressful_time_of_day'] = df['most_stressful_time_of_day'].str.strip()
    
    # Split multiple time entries and explode the column
    df['most_stressful_time_of_day'] = df['most_stressful_time_of_day'].str.split(', ')
    df = df.explode('most_stressful_time_of_day')
    
    # Count the occurrences of each time entry
    time_counts = df['most_stressful_time_of_day'].value_counts()
    
    # Determine the most common time of day
    most_common_time = time_counts.idxmax()
    
    return most_common_time