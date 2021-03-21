import pandas as pd
import numpy as np
import re
import tabula

table_MN = pd.read_html(
    'https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/country_data/India.csv')
df = table_MN[0]
istableValid = False


def validate_table(column_heads):
    for colums in column_heads:
        if colums == 'Beneficiaries vaccinated' or colums == 'Beneficiariesvaccinated':
            return True

def table_picker(main_table):
    for each_table in main_table:
        try:
            topheads = each_table.loc[0, :]
            istableValid = validate_table(topheads)
            if istableValid:
                return each_table;
        except Exception as e:
            print("table error")
    return None

def validate_pdf(column_heads):
    for columns,values in column_heads.items():
        if columns == 'State/UT':
            return True

def pdf_table_picker(pdf_tables):
    for each_table in pdf_tables:
        topheads = each_table.loc[0, :]
        isValid_pdf_table = validate_pdf(topheads)
        if isValid_pdf_table:
            return each_table
    return None

def convert_webdf_to_obj(df_data, date):
    df = df_data.iloc[1:]
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    path = "C:/vaccinedata/"+date + ".csv"
    df.to_csv (path, index = False, header=True)
    #data_dictionary = df.to_dict('dict')
    #print(data_dictionary)

def convert_pdfdf_to_obj(df, date):
    new_header = df.iloc[0] #grab the first row for the header
    new_header[0] = 'S.  No.'
    new_header[1] = 'State/UT'
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    path = "C:/vaccinedata/"+date + ".csv"
    df.to_csv (path, index = False, header=True)
    #data_dictionary = df.to_dict('dict')
    #print(data_dictionary)



for index, row in df.iterrows():
    try:
        if 'https://pib.gov.in/PressReleseDetailm.aspx?PRID' in row['source_url']:
            all_tables = pd.read_html(row['source_url'])
            states_data = table_picker(all_tables)
            print(row['date'])
            print(row['source_url'])
            convert_webdf_to_obj(states_data,row['date'])
        elif 'http://mohfw.gov.in/pdf/Cumulative' in row['source_url']:
            pdf_tables = tabula.read_pdf(row['source_url'])
            valid_pdf_table = pdf_table_picker(pdf_tables)
            print(row['date'])
            print(row['source_url'])
            convert_pdfdf_to_obj(valid_pdf_table, row['date'])
    except Exception as e:
        print("Something went wrong")
