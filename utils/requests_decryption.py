"""
_summary_

_extended_summary_

Returns:
    _type_: _description_
"""

import json
import base64
from xml.etree import ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def main():
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
    decode_base64_in_xml _summary_

    _extended_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
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
    strip_http_headers _summary_

    _extended_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
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
    process_data _summary_

    _extended_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
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
    write_to_file _summary_

    _extended_summary_

    Args:
        df (_type_): _description_
        output_path (_type_): _description_
        file_format (_type_): _description_
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
    visualize_data _summary_

    _extended_summary_

    Args:
        df (_type_): _description_
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
