import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
def adjusted_worksheet_to_df(worksheet):
    """Funkcja przekształcająca arkusz XML w dataframe z uwzględnieniem różnych liczby kolumn w wierszach."""
    rows = worksheet.findall('{urn:schemas-microsoft-com:office:spreadsheet}Table/{urn:schemas-microsoft-com:office:spreadsheet}Row')
    
    data = []
    max_columns = max([len(row.findall('{urn:schemas-microsoft-com:office:spreadsheet}Cell')) for row in rows])
    
    for row in rows:
        cell_values = []
        for cell in row.findall('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            cell_data = cell.find('{urn:schemas-microsoft-com:office:spreadsheet}Data')
            cell_values.append(cell_data.text if cell_data is not None else None)
        
        # Uzupełnienie brakujących wartości
        while len(cell_values) < max_columns:
            cell_values.append(None)
            
        data.append(cell_values)
    
    # Tworzenie dataframe
    df = pd.DataFrame(data[1:], columns=data[0])
    
    return df


import pandas as pd
import xml.etree.ElementTree as ET

def transform_sio_file(file_path):    # Wczytanie pliku XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Przejrzenie struktury XML, aby zrozumieć, jak przekształcić go na dataframe
    xml_structure = {}
    for child in root:
        xml_structure[child.tag] = len(child)

    # Wczytanie danych z sekcji Worksheet
    worksheets = root.findall('{urn:schemas-microsoft-com:office:spreadsheet}Worksheet')

    # Wydobycie nazw arkuszy
    sheet_names = [ws.get('{urn:schemas-microsoft-com:office:spreadsheet}Name') for ws in worksheets]
    def select_schools(df):
        df.columns = df.iloc[4]
        df = df[5:]
        df = df[df['Typ szkoły/placówki'] == 'Szkoła podstawowa']
        df.reset_index(drop=True, inplace=True)
        return df

    def select_teachers(df):
        df.columns = df.iloc[4]
        df = df[5:6]
        
        return df


    df_schools_adjusted = adjusted_worksheet_to_df(worksheets[0])
    df_teachers_adjusted = adjusted_worksheet_to_df(worksheets[1])

    df_schools_adjusted = select_schools(df_schools_adjusted)
    df_teachers_adjusted = select_teachers(df_teachers_adjusted)

    return df_schools_adjusted, df_teachers_adjusted


sio_file = 'raw_data/SIO 30.09.2022.xml'
df_schools, df_teachers = transform_sio_file(sio_file)

df_teachers.to_csv('transformed_data/SIO_30_09_2022_teachers.csv', index=False)#, encoding='utf-8-sig')
df_schools.to_csv('transformed_data/SIO_30_09_2022_schools.csv', index=False)#, encoding='utf-8-sig'
