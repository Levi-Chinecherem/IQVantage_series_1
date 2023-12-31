# insights.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import os
import talib as ta

# Function to load cleaned data
def load_cleaned_data():
    # Load the cleaned data from the CSV file generated by fetchData.py
    cleaned_data = pd.read_csv('data/cleaned_BTCUSDT_2023-01-01_2023-01-31.csv')
    return cleaned_data

data = load_cleaned_data()

# Function to perform data analysis and generate insights
def generate_insights(data):
    insights = []

    # Identify the long-term trend using 200-day moving average
    data['200-day MA'] = data['Close'].rolling(window=200).mean()

    # Identify the short-term trend using 20-day moving average
    data['20-day MA'] = data['Close'].rolling(window=20).mean()

    # Determine support and resistance levels
    support = data['Low'].min()
    resistance = data['High'].max()

    # Calculate price change
    data['Price Change'] = data['Close'].diff()

    # Calculate price volatility
    data['Volatility'] = data['Price Change'].rolling(window=20).std()

    
    # Recognize price patterns
    # Example: Using TA-Lib to detect multiple patterns
    pattern_detected = ta.CDL2CROWS(data['Open'], data['High'], data['Low'], data['Close'])
    
    # TA-Lib CDL2CROWS pattern:
    # 2 Crows (Two Crows): This pattern is a bearish reversal pattern and suggests a possible change in trend.

    if pattern_detected > 0:
        pattern_name = "Two Crows (Bearish Reversal)"
    elif pattern_detected < 0:
        pattern_name = "Bullish Reversal Pattern Detected"
    else:
        pattern_name = "No Pattern Detected"

    # Check for crossover of short-term and long-term moving averages
    crossover = False
    if data['20-day MA'].iloc[-1] > data['200-day MA'].iloc[-1] and data['20-day MA'].iloc[-2] < data['200-day MA'].iloc[-2]:
        crossover = True

     # Generate insights
    insights.append("Price Trends:")
    insights.append("- Long-term trend: Check for crossovers of 200-day moving average.")
    insights.append("- Short-term trend: Check for crossovers of 20-day moving average.")
    insights.append(f"- Support level: {support}")
    insights.append(f"- Resistance level: {resistance}")
    insights.append("Price Patterns:")
    insights.append(f"- Pattern Detected: {pattern_name}")

    # Analyze price change and volatility
    price_change = data['Price Change'].iloc[-1]
    volatility = data['Volatility'].iloc[-1]
    insights.append("Price Change and Volatility:")
    insights.append(f"- Price Change (Today): {price_change:.2f}")
    insights.append(f"- Volatility (20-day): {volatility:.2f}")

    # Visualize price trends
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Close'], label='Price', color='blue')
    plt.plot(data['Date'], data['200-day MA'], label='200-day MA', color='orange')
    plt.plot(data['Date'], data['20-day MA'], label='20-day MA', color='green')
    plt.title('Price Trends')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    
    # Define the folder path for images
    img_folder_path = 'insights/imgs'
    
    # Check if the folder exists, and create it if not
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)
    
    # Save the plot inside the 'imgs' folder
    trend_plot_filename = os.path.join(img_folder_path, 'price_trends.png')
    plt.savefig(trend_plot_filename)
    plt.close()
    
    # Visualize price change
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Price Change'], kde=True, color='blue')
    plt.title('Price Change Distribution')
    plt.xlabel('Price Change')
    plt.ylabel('Frequency')
    
    # Save the plot inside the 'imgs' folder
    price_change_plot_filename = os.path.join(img_folder_path, 'price_change_distribution.png')
    plt.savefig(price_change_plot_filename)
    plt.close()

    # Visualize volatility
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Volatility'], label='Volatility', color='red')
    plt.title('Price Volatility (20-day)')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    
    # Save the plot inside the 'imgs' folder
    volatility_plot_filename = os.path.join(img_folder_path, 'price_volatility.png')
    plt.savefig(volatility_plot_filename)
    plt.close()

    # Provide trading recommendations based on insights
    recommendations = []
    if crossover:
        recommendations.append("Consider a long position due to a short-term moving average crossover.")
    if pattern_detected == "Head and Shoulders":
        recommendations.append("Be cautious as a head and shoulders pattern is detected.")
    if data['Price Change'].iloc[-1] > 0 and data['Volatility'].iloc[-1] > 0.5:
        recommendations.append("Consider a bullish trade with high volatility.")
    if data['Price Change'].iloc[-1] < 0 and data['Volatility'].iloc[-1] > 0.5:
        recommendations.append("Consider a bearish trade with high volatility")
    
    insights.extend(recommendations)

    return insights

# Function to save insights as PDF
def save_insights_as_pdf(insights, currency_pair):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")  # Format the date and time
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Insights for {currency_pair} - {formatted_date}", ln=True, align='C')
    pdf.ln(10)

    # Define the folder path
    folder_path = 'insights'

    # Check if the folder exists, and create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Replace invalid characters in the currency pair with underscores
    currency_pair = currency_pair.replace("/", "_")

    # Add each insight to the PDF
    for insight in insights:
        pdf.multi_cell(0, 10, insight)
        pdf.ln()

    # Generate a valid filename
    pdf_filename = f'{folder_path}/insight_{currency_pair}_{formatted_date}.pdf'
    pdf.output(pdf_filename)

def main():
    # Load cleaned data
    cleaned_data = load_cleaned_data()
    
    # Perform data analysis and generate insights
    insights = generate_insights(cleaned_data)
    
    # Save insights as a PDF with a unique name
    save_insights_as_pdf(insights, "BTCUSDT")

if __name__ == "__main__":
    main()
