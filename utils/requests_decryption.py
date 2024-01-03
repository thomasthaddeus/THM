"""requests_decryption.py

This script is designed to process and analyze data from an XML file containing 
base64 encoded elements. It includes functionality to decode base64 encoded 
content, strip HTTP headers from the decoded data, transform it into a pandas 
DataFrame, and write the cleaned data to various file formats. Additionally, it 
provides a visualization of the length distribution of the processed response 
strings.

The script starts by prompting the user to specify an output file format. It 
then processes an XML file containing base64 encoded data, decodes this data, 
and cleans it by stripping HTTP headers. The processed data is converted into a 
pandas DataFrame for easy manipulation. The user can choose to export this data 
to a CSV, JSON, Excel, or plain text file. Finally, the script visualizes the 
lengths of the response strings in the data, providing insights into the 
distribution of response sizes.

Returns:
    None: This script does not return any value but produces side effects such as file outputs and plots.
"""

import json
import base64
from xml.etree import ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def main():
    """
    The main function of the script. It orchestrates the flow of the program by 
    calling other functions to process data, write to a file in the specified 
    format, and visualize data.

    This function starts by defining the paths for input and output files and 
    asking the user to specify the output file format. It then calls the 
    process_data function to process the XML data, the write_to_file function 
    to save the processed data in the desired format, and the visualize_data 
    function to display a histogram of response lengths.

    The main function serves as the entry point of the script. It is 
    responsible for initializing file paths, handling user input for file 
    format selection, and coordinating the sequence of data processing, file 
    writing, and data visualization.

    Returns:
        None: This function does not return a value.
    """
    file_path = "D:/tryhackme_urls.json"
    output_path = "D:/responses/output"

    # Ask the user for the file format
    file_format = input("Enter the file format (csv, json, excel, txt): ")
    output_path += "." + file_format

    df = process_data(file_path)
    write_to_file(df, output_path, file_format)
    visualize_data(df)


def decode_base64_in_xml(file_path):
    """
    Decodes base64 encoded data within XML elements. This function parses an 
    XML file, locates elements with a base64 attribute set to 'true', decodes 
    their content from base64 to hexadecimal format, and returns the results in 
    a JSON format.

    Args:
        file_path (str): The path to the XML file to be processed.

    Returns:
        str: A JSON string representing the decoded hexadecimal data of each base64 element.
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find elements with base64="true"
    elements = root.findall(".//*[@base64='true']")

    # Decode base64 for each element and store results
    results = []
    for elem in elements:
        cdata = elem.text
        # Remove CDATA
        cdata = cdata.replace("<![CDATA[", "").replace("]]>", "")
        # Decode from base64
        decoded = base64.b64decode(cdata)
        # Convert binary data to hex string
        hex_string = decoded.hex()
        # Store in results
        results.append({elem.tag: hex_string})

    # Return the results in JSON format
    return json.dumps(results, indent=4)


def strip_http_headers(data):
    """
    Strips HTTP headers from a hex-encoded string of HTTP response data. 
    Converts the hex string to bytes, decodes it into a UTF-8 string, and then 
    separates and discards the headers to keep only the body of the response.

    Args:
        data (str): The hex-encoded string containing the HTTP response data.

    Returns:
        str: The body of the HTTP response after stripping off the headers, or the original data
        if it can't be processed.
    """
    # Convert hex to bytes
    try:
        byte_data = bytes.fromhex(data)
    except (TypeError, ValueError):
        return data

    # Try to convert bytes to string
    try:
        text_data = byte_data.decode("utf-8")
    except UnicodeDecodeError:
        return data

    # Strip headers
    try:
        headers, body = text_data.split("\r\n\r\n", 1)
    except ValueError:
        return text_data

    return body


def process_data(file_path):
    """
    Processes data from an XML file containing base64 encoded elements. This 
    function decodes the base64 data, converts it to a pandas DataFrame, drops 
    unnecessary columns, and applies the strip_http_headers function to clean 
    the data.

    Args:
        file_path (str): The path to the XML file containing the data.

    Returns:
        pandas.DataFrame: A DataFrame containing the processed data.
    """
    # Run the function to get the results
    json_output = decode_base64_in_xml(file_path)

    # Parse the JSON output
    data = json.loads(json_output)

    # Convert the results into a DataFrame
    df = pd.DataFrame(data)

    # Drop the "request" column
    df = df.drop(["request"], axis=1)

    # Apply the function to the "response" column
    df["response"] = df["response"].apply(strip_http_headers)

    return df


def write_to_file(df, output_path, file_format):
    """
    Writes a DataFrame to a file in a specified format. The function supports 
    exporting the DataFrame to CSV, JSON, Excel, or plain text files.

    Args:
        df (pandas.DataFrame): The DataFrame to be written to a file.
        output_path (str): The path where the output file will be saved.
        file_format (str): The format of the output file. Options are 'csv', 
        'json', 'excel', or 'txt'.
    """
    if file_format == 'csv':
        df.to_csv(output_path, index=False)
    elif file_format == 'json':
        df.to_json(output_path)
    elif file_format == 'excel':
        df.to_excel(output_path, index=False)
    elif file_format == 'txt':
        response_text = '\n'.join(df['response'].dropna())
        with open(output_path, 'w') as f:
            f.write(response_text)
    else:
        print(f'Unsupported file format: {file_format}')


def visualize_data(df):
    """
    Generates a histogram of the lengths of response strings in a DataFrame. 
    This function adds a new column to the DataFrame for the length of each 
    response and plots a histogram to visualize the distribution of these 
    lengths.

    Args:
        df (pandas.DataFrame): The DataFrame containing the response strings.
    """
    # Create a new column for the length of each response
    df["response_length"] = df["response"].str.len()

    # Plot the lengths of the responses
    df["response_length"].plot(kind="hist", edgecolor="black")
    plt.title("Response Lengths")
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.show()


# Run the main function
if __name__ == "__main__":
    main()
