import pandas as pd

def extract_table_entities(file_path, sheet_name, header_row, columns):
    """
    Extracts a floating table from an Excel sheet into a list of dictionaries.
    
    :param file_path: Path to the Excel file
    :param sheet_name: Name of the sheet
    :param header_row: The 0-indexed row number where the table headers are located
    :param columns: Excel column range (e.g., "C:F" if the table is in columns C through F)
    """
    # Read only the specific range containing the table
    df = pd.read_excel(
        file_path, 
        sheet_name=sheet_name, 
        header=header_row, 
        usecols=columns
    )
    
    # Drop any completely empty rows that might exist below the table
    df.dropna(how='all', inplace=True)
    
    # Optional: Fill NaN values with None or empty strings if your entities require it
    df = df.where(pd.notnull(df), None)
    
    # Convert the dataframe to a list of dictionaries (each row is an entity)
    entities = df.to_dict(orient='records')
    
    return entities

# Example Usage: 
# If your table headers are on row 5 (index 4) and span from column C to F
# if __name__ == "__main__":
#     records = extract_table_entities(
#         file_path="data.xlsx", 
#         sheet_name="Sheet1", 
#         header_row=4,   # 0-indexed, so row 5 in Excel is index 4
#         columns="C:F"   # Only read columns C, D, E, and F
#     )
    
#     for entity in records:
#         print(entity)