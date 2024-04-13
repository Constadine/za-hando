import pandas as pd

def load_data(filename):   
    df = pd.read_excel('Stress insights.xlsx')
    
    columns_to_replace_numbers = ['caffeine', 'silence', 'stretch_breathing']
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

