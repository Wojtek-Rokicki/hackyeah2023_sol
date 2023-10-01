# READY TO USE FOR '../data/kutno_dane/SIO etaty.xml' - > DATAFRAME
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

def xml_to_dataframes_v4(xml_path):
    """
    Funkcja przekształcająca arkusze w pliku XML na listę dataframe'ów z uwzględnieniem atrybutu MergeAcross i użyciem wiersza o indeksie 0 jako nagłówka.
    
    Args:
    - xml_path (str): ścieżka do pliku XML.
    
    Returns:
    - List[pd.DataFrame]: lista dataframe'ów odpowiadających arkuszom w pliku XML.
    """
    
    # Wczytanie pliku XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Wczytanie danych z sekcji Worksheet
    worksheets = root.findall('{urn:schemas-microsoft-com:office:spreadsheet}Worksheet')
    
    dataframes = []
    for ws in worksheets:
        df = adjusted_worksheet_to_df_v4(ws)
        dataframes.append(df)

    df = dataframes[0]
    df.columns = df.iloc[1] 
    df = df[1:]
    df = df.drop(1)
    df = df[df['Typ szkoły / placówki'] == 'Szkoła podstawowa']
    df.reset_index(drop=True, inplace=True)
 
    return df

sio_etaty = 'raw_data/SIO etaty.xml'
df = xml_to_dataframes_v4(sio_etaty)
df.to_csv('transformed_data/etaty.csv', index=False)