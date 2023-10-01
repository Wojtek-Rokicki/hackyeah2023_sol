import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np

sio_wydatki = 'raw_data/Sprawozdania[2022][IVKwartał] Wydatki.xml'
def xml_to_dataframe_v3(file_path: str) -> pd.DataFrame:
    
    def xml_to_dict(element):
        if len(element) == 0:
            return element.text
        return {child.tag: xml_to_dict(child) for child in element}

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Convert XML to dictionary
    data_dict = xml_to_dict(root)

    # Extract the jednostki structure
    jednostki_entries = []

    for jednostka in root.findall(".//Jednostki/Jednostka"):
        entry = {}
        entry['Nazwa'] = jednostka.find('Nazwa').text if jednostka.find('Nazwa') is not None else None
        entry['Regon'] = jednostka.find('Regon').text if jednostka.find('Regon') is not None else None
        entry['Sprawozdania'] = []

        for sprawozdanie in jednostka.findall('Sprawozdania/Rb-28s'):
            sprawozdanie_entry = {}
            pozycje = sprawozdanie.find('Pozycje')
            if pozycje is not None:
                sprawozdanie_entry['Pozycje'] = [xml_to_dict(pozycja) for pozycja in pozycje.findall('Pozycja')]
            entry['Sprawozdania'].append(sprawozdanie_entry)

        jednostki_entries.append(entry)

    # Convert the jednostki_entries structure to a DataFrame
    dataframes = []

    for jednostka in jednostki_entries:
        for sprawozdanie in jednostka['Sprawozdania']:
            df_temp = pd.DataFrame(sprawozdanie['Pozycje'])
            df_temp['Nazwa Jednostki'] = jednostka['Nazwa']
            df_temp['Regon'] = jednostka['Regon']
            dataframes.append(df_temp)

    # Combine all dataframes into one
    final_df = pd.concat(dataframes, ignore_index=True)

    # Fill missing columns with 0
    for col in ['WW', 'ZO']:
        if col not in final_df.columns:
            final_df[col] = 0

    # Rearrange columns
    final_df = final_df[['Nazwa Jednostki', 'Regon', 'Dzial', 'Rozdzial', 'Grupa', 'Paragraf', 'P4', 'PL', 'ZA', 'WW', 'ZO']]
    final_df.fillna(0, inplace=True)
    return final_df


df = xml_to_dataframe_v3(sio_wydatki)
df.to_csv('transformed_data/wydatki_2022.csv', index=False)#, encoding='utf-8-sig

