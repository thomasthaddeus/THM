# THM Data Processing and Analysis

## Overview

This project is designed to process and analyze data extracted from [TryHackMe](https://tryhackme.com/) (THM). The primary goal is to decode, clean, and analyze the data for further insights. The extracted data, presumed to be in an XML format with base64 encoded elements, is processed through a series of Python scripts to decode, clean, and visualize the information.

## Key Features

- **Base64 Decoding:** Extracts and decodes base64 encoded data from XML files.
- **Data Cleaning:** Strips HTTP headers from the decoded data for clarity and analysis purposes.
- **Data Transformation:** Converts the cleaned data into a pandas DataFrame for easy manipulation and analysis.
- **Flexible Data Export:** Allows the export of processed data into various formats like CSV, JSON, Excel, and plain text.
- **Data Visualization:** Provides histogram plots of response lengths, offering insights into the distribution of data sizes.

## Prerequisites

To run this project, you will need:
- Python 3.x
- Pandas library
- Matplotlib library
- An XML file containing the base64 encoded data (e.g., `tryhackme_urls.xml`)

## Installation

1. Clone the repository or download the source code.
2. Ensure that Python 3.x is installed on your system.
3. Install the required Python libraries using pip:
   ```bash
   pip install pandas matplotlib
   ```

## Usage

1. Place your XML data file in a known directory.
2. Run the main script (`requests_decryption.py`) from your terminal or command prompt:
   ```bash
   python requests_decryption.py
   ```
3. Follow the on-screen prompts to specify the desired output file format.

## Data Structure

- Input: XML file with base64 encoded data.
- Output: Decoded and cleaned data in one of the chosen formats (CSV, JSON, Excel, or TXT).

## Visualization

The script generates histograms showing the distribution of the lengths of response strings in the dataset, which can be useful for understanding the data characteristics.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request for review.

## License

This project is released under [MIT License](https://opensource.org/licenses/MIT).

## Disclaimer

This project is for educational purposes only. Ensure that you have the right to access and process the data from TryHackMe or any other sources.
