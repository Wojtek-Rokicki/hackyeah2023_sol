import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
sio_dochody_IV = 'raw_data/Sprawozdania[2022][IVKwartał] Dochody.xml'
sio_dochody_II = 'raw_data/Sprawozdania[2023][IIKwartał] Dochody.xml'

def extract_pozycje_data(pozycje_element):
    pozycje_data = []
    
    for pozycja in pozycje_element.findall("Pozycja"):
        pozycja_data = {}
        for child in pozycja:
            pozycja_data[child.tag] = child.text
        pozycje_data.append(pozycja_data)
    
    return pozycje_data

def extract_all_jednostki_data(root_element):
    all_jednostki_data = []
    
    for jednostka_element in root_element.findall(".//Jednostka"):
        jednostka_data = extract_xml_to_dict(jednostka_element)
        all_jednostki_data.append(jednostka_data)
    
    return all_jednostki_data

def extract_all_jednostki_to_dataframe(root_element):
    all_rows = []
    
    for jednostka_element in root_element.findall(".//Jednostka"):
        jednostka_data = extract_xml_to_dict(jednostka_element)
        
        for sprawozdanie in jednostka_data["Sprawozdania"]:
            for pozycja in sprawozdanie["Pozycje"]:
                row = {
                    "Nazwa": jednostka_data["Nazwa"],
                    "Regon": jednostka_data["Regon"],
                    "Rok": sprawozdanie["Okres"]["Rok"],
                    "Okres": sprawozdanie["Okres"]["Okres"],
                    "Dzial": pozycja.get("Dzial", np.nan),
                    "Rozdzial": pozycja.get("Rozdzial", np.nan),
                    "Paragraf": pozycja.get("Paragraf", np.nan),
                    "P4": pozycja.get("P4", np.nan),
                    "PL": pozycja.get("PL", np.nan),
                    "NA": pozycja.get("NA", np.nan),
                    "DW": pozycja.get("DW", np.nan),
                    "NO": pozycja.get("NO", np.nan),
                    "NZ": pozycja.get("NZ", np.nan),
                    "NP": pozycja.get("NP", np.nan)
                }
                all_rows.append(row)
    
    return pd.DataFrame(all_rows)

def extract_jednostka_to_dict(jednostka_element):
    jednostka_data = {}
    
    # Extract basic information about "Jednostka"
    for child in jednostka_element:
        if child.tag != "Sprawozdania":
            jednostka_data[child.tag] = child.text

    # Extract "Sprawozdania" data
    sprawozdania_data = []
    for sprawozdanie in jednostka_element.findall("Sprawozdania/Rb-27s"):
        sprawozdanie_data = {}
        
        # Extract "Okres" data
        okres_data = {}
        for okres_child in sprawozdanie.find("Okres"):
            okres_data[okres_child.tag] = okres_child.text
        sprawozdanie_data["Okres"] = okres_data
        
        # Extract "Pozycje" data
        pozycje_element = sprawozdanie.find("Pozycje")
        if pozycje_element is not None:
            sprawozdanie_data["Pozycje"] = extract_pozycje_data(pozycje_element)
        
        sprawozdania_data.append(sprawozdanie_data)
    
    jednostka_data["Sprawozdania"] = sprawozdania_data
    return jednostka_data

def extract_all_jednostki_to_dataframe_corrected(root_element):
    all_rows = []
    
    for jednostka_element in root_element.findall(".//Jednostka"):
        jednostka_data = extract_jednostka_to_dict(jednostka_element)
        
        for sprawozdanie in jednostka_data["Sprawozdania"]:
            for pozycja in sprawozdanie["Pozycje"]:
                row = {
                    "Nazwa": jednostka_data["Nazwa"],
                    "Regon": jednostka_data["Regon"],
                    "Rok": sprawozdanie["Okres"]["Rok"],
                    "Okres": sprawozdanie["Okres"]["Okres"],
                    "Dzial": pozycja.get("Dzial", np.nan),
                    "Rozdzial": pozycja.get("Rozdzial", np.nan),
                    "Paragraf": pozycja.get("Paragraf", np.nan),
                    "P4": pozycja.get("P4", np.nan),
                    "PL": pozycja.get("PL", np.nan),
                    "NA": pozycja.get("NA", np.nan),
                    "DW": pozycja.get("DW", np.nan),
                    "NO": pozycja.get("NO", np.nan),
                    "NZ": pozycja.get("NZ", np.nan),
                    "NP": pozycja.get("NP", np.nan)
                }
                all_rows.append(row)
    df = pd.DataFrame(all_rows)
    df.fillna(0, inplace=True)
    return df


def dochody_to_dataframe(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()
    root = ET.fromstring(xml_content)
    all_jednostki_df_corrected = extract_all_jednostki_to_dataframe_corrected(root)
    return all_jednostki_df_corrected


df_dochody = dochody_to_dataframe(sio_dochody_IV)
df_dochody.to_csv('transformed_data/dochody.csv', index=False)
