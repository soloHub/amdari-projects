import pandas as pd 
import json
import csv
import requests
import psycopg2 as pg
import os


# # Extraction Layer
# url = "https://realty-mole-property-api.p.rapidapi.com/randomProperties"

# querystring = {"limit":"1000000"}

# headers = {
# 	"x-rapidapi-key": "2f036616efmshc6340e778ded97bp14698fjsndb5a47a5a5ae",
# 	"x-rapidapi-host": "realty-mole-property-api.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# data = response.json()

# Create the directory if it doesn't exist
# if not os.path.exists('datasheets'):
#     os.makedirs('datasheets')

filename = 'datasheets/PropertyRecords.json'
# with open(filename, 'w') as file:
#     json.dump(data, file, indent=4)


# Create dataframe
propertyrecords_df = pd.read_json(filename)

# Create an index in the dataframe
propertyrecords_df['property_id'] = propertyrecords_df.index 

# Read from dataframe top records
##propertyrecords_df.head()
# Read from dataframe schema
##propertyrecords_df.info()
# Read from dataframe list of columns
##propertyrecords_df.columns.tolist()

# Transformation Layer
# 1st step convert dictionary column to string
propertyrecords_df['features'] = propertyrecords_df['features'].apply(json.dumps)

# 2nd step replace NaN values with appropriate defaults or remove row/column as necessary
propertyrecords_df.fillna({
    'assessorID': 'Unknown',
    'bedrooms': 0,
    'legalDescription': 'Not available',
    'squareFootage': 0,
    'subdivision': 'Not available',
    'yearBuilt': 0,
    'bathrooms': 0,
    'lotSize': 0,
    'propertyType': 'Unknown',
    'lastSalePrice': 0,
    'lastSaleDate': 'Not available',
    'ownerOccupied': 0,
    'features': 'None',
    'taxAssessment': 'Not available',
    'propertyTaxes': 'Not available',
    'owner': 'Unknown',
    'addressLine2': 'Not available',
    'zoning': 'Unknown'
}, inplace=True)

# Create facts table
fact_columns = ['property_id', 'addressLine1', 'city', 'state', 'zipCode', 'formattedAddress', 'squareFootage', 'yearBuilt', 'bathrooms', 'lotSize', 'propertyType', 'longitude', 'latitude']
fact_table = propertyrecords_df[fact_columns]

# Create location dimension
location_dim = propertyrecords_df[['property_id', 'addressLine1', 'city', 'state', 'zipCode', 'county', 'longitude', 'latitude']].drop_duplicates().reset_index(drop=True)
location_dim.index.name = 'location_id'

# Create sale dimension
sales_dim = propertyrecords_df[['property_id', 'lastSalePrice', 'lastSaleDate']].drop_duplicates().reset_index(drop=True)
sales_dim.index.name = 'sales_id'

# Create property features dimension
features_dim = propertyrecords_df[['property_id', 'features', 'propertyType', 'zoning']].drop_duplicates().reset_index(drop=True)
features_dim.index.name = 'features_id'

# Create csv files of tables
fact_table.to_csv('datasheets/property_fact.csv', index=False)
location_dim.to_csv('datasheets/location_dimension.csv', index=True)
sales_dim.to_csv('datasheets/sales_dimension.csv', index=True)
features_dim.to_csv('datasheets/features_dimension.csv', index=True)

# Loading Layer
# develop a function to connect to pgadmin
def get_db_connection():
    connection = pg.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='r00t'
    )
    return connection

# Connect to SQL Database
conn = get_db_connection()


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    create_table_query = '''
                        CREATE SCHEMA IF NOT EXISTS zipcoproperty;

                        DROP TABLE IF EXISTS zipcoproperty.fact_table;
                        DROP TABLE IF EXISTS zipcoproperty.location_dim;
                        DROP TABLE IF EXISTS zipcoproperty.sales_dim;
                        DROP TABLE IF EXISTS zipcoproperty.features_dim;

                        CREATE TABLE zipcoproperty.fact_table(
                            addressLine1 VARCHAR(255),
                            city VARCHAR(100),
                            state VARCHAR(50),
                            zipCode INTEGER,
                            formattedAddress VARCHAR(255),
                            squareFootage FLOAT,
                            yearBuilt FLOAT,
                            bathrooms FLOAT,
                            lotSize FLOAT,
                            propertyType VARCHAR(100),
                            longitude FLOAT,
                            latitude FLOAT
                        );

                        CREATE TABLE zipcoproperty.location_dim(
                            location_id SERIAL PRIMARY KEY,
                            addressLine1 VARCHAR(255),
                            city VARCHAR(100),
                            state VARCHAR(50),
                            zipCode INTEGER,
                            county VARCHAR(100),
                            longitude FLOAT,
                            latitude FLOAT
                        );

                        CREATE TABLE zipcoproperty.sales_dim(
                            sales_id SERIAL PRIMARY KEY,
                            lastSalePrice FLOAT,
                            lastSaleDate DATE
                        );

                        CREATE TABLE zipcoproperty.features_dim(
                            features_id SERIAL PRIMARY KEY,
                            features TEXT,
                            propertyType VARCHAR(100),
                            zoning VARCHAR(100)
                        );
                        '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

create_tables()

# Create function to load data into tables
def load_data_from_csv_to_tables(csv_path, table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # skip the header
        for row in reader:
            placeholders = ', '.join(['%s'] * len(row))
            query = f'INSERT INTO {table_name} VALUES ({placeholders});'
            cursor.execute(query, row)
    conn.commit()
    cursor.close()
    conn.close()

# fact csv to table
fact_csv_path = os.path.abspath('datasheets/property_fact.csv')
load_data_from_csv_to_tables(fact_csv_path, 'zipcoproperty.fact_table')

# location_dim csv to table
loc_dim_csv = os.path.abspath('datasheets/location_dimension.csv')
load_data_from_csv_to_tables(loc_dim_csv, 'zipcoproperty.location_dim')

# features csv to table
feat_dim_csv = os.path.abspath('datasheets/features_dimension.csv')
load_data_from_csv_to_tables(feat_dim_csv, 'zipcoproperty.features_dim')


# Create function to load data into sales tables
def load_data_from_csv_to_sales_table(csv_path, table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # skip the header
        for row in reader:
            # Convert empty strings (or 'Not available') in the date column to None(Null in SQL)
            row = [None if (cell == '' or cell == 'Not available') and col_name == 'lastSaleDate' else cell for cell, col_name in zip(row, sales_dim_columns)]
            placeholders = ', '.join(['%s'] * len(row))
            query = f'INSERT INTO {table_name} VALUES ({placeholders});'
            cursor.execute(query, row)
    conn.commit()
    cursor.close()
    conn.close()

# define the column names in sales_dim table
sales_dim_columns = ['sales_id', 'lastSalePrice', 'lastSaleDate']

# sales_dim csv to table
sales_dim_csv = os.path.abspath('datasheets/sales_dimension.csv')
load_data_from_csv_to_sales_table(sales_dim_csv, 'zipcoproperty.sales_dim')

print('All Data has been loaded into their respective tables in the Postgres Database')