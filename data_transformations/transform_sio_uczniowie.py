import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np

def adjusted_worksheet_to_df_v4(worksheet):
    """Funkcja przekształcająca arkusz XML w dataframe z uwzględnieniem różnych liczby kolumn w wierszach, atrybutu MergeAcross oraz użyciem wiersza o indeksie 0 jako nagłówka."""
    rows = worksheet.findall('{urn:schemas-microsoft-com:office:spreadsheet}Table/{urn:schemas-microsoft-com:office:spreadsheet}Row')
    
    data = []
    max_columns = max([len(row.findall('{urn:schemas-microsoft-com:office:spreadsheet}Cell')) for row in rows])
    
    for row in rows:
        cell_values = []
        for cell in row.findall('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            merge_across = int(cell.get('MergeAcross', 0))
            cell_data = cell.find('{urn:schemas-microsoft-com:office:spreadsheet}Data')
            cell_value = cell_data.text if cell_data is not None else None
            # Dodanie wartości komórki oraz odpowiednią liczbę wartości None dla komórek z atrybutem MergeAcross
            cell_values.extend([cell_value] + [None] * merge_across)
        
        # Uzupełnienie brakujących wartości
        while len(cell_values) < max_columns:
            cell_values.append(None)
            
        data.append(cell_values)
    
    # Tworzenie dataframe (użycie wiersza o indeksie 0 jako nagłówka)
    df = pd.DataFrame(data[1:], columns=data[0])
    
    return df

# Ponowne przekształcenie arkusza "Arkusz1" na dataframe
def transform_sio_uczniowie(xml_path):
    """
        Funkcja przekształcająca arkusz "Arkusz1" w pliku XML na dataframe z uwzględnieniem atrybutu MergeAcross i użyciem wiersza o indeksie 1 jako nagłówka.
        """
    tree_uczniowie_new = ET.parse(xml_path)
    root_uczniowie_new = tree_uczniowie_new.getroot()

    worksheet_info_uczniowie = []

    worksheets_uczniowie_new = root_uczniowie_new.findall('{urn:schemas-microsoft-com:office:spreadsheet}Worksheet')

    for ws in worksheets_uczniowie_new:
        ws_name = ws.get('{urn:schemas-microsoft-com:office:spreadsheet}Name')
        row_count = len(ws.findall('{urn:schemas-microsoft-com:office:spreadsheet}Table/{urn:schemas-microsoft-com:office:spreadsheet}Row'))
        worksheet_info_uczniowie.append((ws_name, row_count))


    df_uczniowie = adjusted_worksheet_to_df_v4(worksheets_uczniowie_new[0])
    df = df_uczniowie

    df.columns = df.iloc[1] 
    df = df[1:]

    df.reset_index(drop=True, inplace=True)
    df = df.drop(0)
    df = df[df['Typ szkoły / placówki'] == 'Szkoła podstawowa']
    df.reset_index(drop=True, inplace=True)
    return df

sio_uczniowie = 'raw_data/SIO uczniowie.xml'

df = transform_sio_uczniowie(sio_uczniowie)
df.to_csv('transformed_data/uczniowie.csv', index=False)
