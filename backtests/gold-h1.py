import pandas as pd
import yfinance as yf

# Sample DataFrame with H1 and 1-minute data (same as before)
# Assume `h1_data` and `m1_data` are DataFrames with columns ['timestamp', 'open', 'high', 'low', 'close']

# Function to determine candle color
def get_candle_color(open_price, close_price):
    return "bullish" if close_price > open_price else "bearish"

# Initialize results list
results = []

# Define the ticker symbol for gold (e.g., GC=F for gold futures)
ticker = 'GC=F'  # Gold futures

# Define the date range for data extraction
start_date = '2024-10-23'
end_date = '2024-10-24'

# Fetch historical data for the specified date range
data = yf.download(ticker, start=start_date, end=end_date, interval='1h')

# Check the columns of the DataFrame
# print(data.columns)  # Add this line to inspect the columns

# Fetch historical data for 1-minute intervals using the same date range
m1_data = yf.download(ticker, start=start_date, end=end_date, interval='1m')

# Initialize a list to store the first minute candles
first_minute_candles = []

# Loop through each H1 candle
for idx, h1_row in data.iterrows():
    h1_start_time = idx  # The start time of the H1 candle
    h1_end_time = h1_start_time + pd.Timedelta(hours=1)  # The end time of the H1 candle
    
    # Find the first minute candle within the H1 candle's time range
    first_minute_candle = m1_data[(m1_data.index >= h1_start_time) & 
                                   (m1_data.index < h1_end_time)]
    
    if not first_minute_candle.empty:
        # Append the first minute candle to the list
        first_minute_candles.append(first_minute_candle.iloc[0])  # Get the first row

# Convert the list of first minute candles to a DataFrame
first_minute_candles_df = pd.DataFrame(first_minute_candles)

# Display the first minute candles DataFrame
# print(first_minute_candles_df)

# Add candle color to H1 data
data['candle_color'] = data.apply(lambda row: get_candle_color(row[('Open', 'GC=F')], row[('Close', 'GC=F')]), axis=1)

# Add candle color to first minute candles DataFrame
first_minute_candles_df['candle_color'] = first_minute_candles_df.apply(lambda row: get_candle_color(row[('Open', 'GC=F')], row[('Close', 'GC=F')]), axis=1)

# Display the H1 data with candle colors
# print(data[['candle_color']])  # Print only the candle color column for H1 data

# # Display the first minute candles DataFrame with candle colors
# print(first_minute_candles_df[['candle_color']])  # Print only the candle color column for M1 data

# Merge H1 and M1 DataFrames on the timestamp
aligned_data = pd.merge(data, first_minute_candles_df, left_index=True, right_index=True, suffixes=('_H1', '_M1'))

# # Display the aligned DataFrame with candle colors
# print(aligned_data[['candle_color_H1', 'candle_color_M1']])

# Calculate the number of matches between H1 and M1 candle colors
matches = (aligned_data['candle_color_H1'] == aligned_data['candle_color_M1']).sum()
total = len(aligned_data)

# Calculate the percentage of matches
percentage_match = (matches / total) * 100 if total > 0 else 0

# Print the percentage of matches
print(f"Percentage of matches between H1 and M1 candle colors: {percentage_match:.2f}%")

