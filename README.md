# Crypto Trading Insights System

## Overview

The Crypto Trading Insights System is a Python-based tool that performs data analysis on cryptocurrency price data and generates insights to help traders make informed decisions. It uses historical price data to identify trends, patterns, and other valuable information to guide trading strategies.

![System Overview](https://github.com/Levi-Chinecherem/IQVantage_series_1/blob/main/insights/imgs/price_trends.png)

![System Overview](https://github.com/Levi-Chinecherem/IQVantage_series_1/blob/main/insights/imgs/price_volatility.png)

![System Overview](https://github.com/Levi-Chinecherem/IQVantage_series_1/blob/main/insights/imgs/price_change_distribution.png)

## Features

- **Data Cleaning**: The system can clean and preprocess raw cryptocurrency price data.
- **Price Trend Analysis**: It identifies both short-term and long-term trends using moving averages.
- **Support and Resistance Levels**: The system determines key support and resistance levels.
- **Pattern Recognition**: Detects specific price patterns, such as the "Head and Shoulders" pattern.
- **Price Change and Volatility Analysis**: Analyzes price changes and volatility to assess market conditions.
- **Insight Generation**: Generates trading insights based on the analyzed data and patterns.
- **Visualization**: Creates visual representations of data trends, price changes, and volatility for easier understanding.
- **PDF Report**: Outputs insights and visualizations as a PDF report for convenient review.

## Getting Started

### Installation

1. Clone this repository to your local machine.
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Prepare your cryptocurrency price data by following the data cleaning guidelines (provide a link or instructions).
2. Run the `fetchData.py` script to fetch and save the price data.
3. Run the `insights.py` script to perform data analysis and generate insights.
4. The generated insights will be saved as a PDF report in the "insights" folder.

### Customization

You can customize the system by:

- Modifying the data cleaning process.
- Implementing custom pattern recognition algorithms.
- Adapting the analysis and insights generation logic to your trading strategies.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Mention any libraries, frameworks, or data sources you used in this project.

## Authors

- [Levi Chinecherem C.](https://github.com/Levi-Chinecherem) - Provide a link to your GitHub profile.

## Contact

If you have questions or need assistance, feel free to contact [lchinecherem2018@gmail.com].
