import numpy as np
import pymysql
import pandas as pd
from datetime import datetime
import glob 
import os 
# EXTRACTION
def extraction(csvfolder):
    location=pd.DataFrame()
    dates=pd.DataFrame()
    weathers=pd.DataFrame()
    for filepath in csvfolder:
        df=pd.read_csv(filepath,sep=",", encoding='cp1252')
        print("file= ",filepath)
        locationdf=df[['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION']]#.drop_duplicates()
        # locationdf.insert(0,'LocationID',range(0,0+len(locationdf)))
        weatherfact= df[['STATION', 'DATE', 'PRCP', 'PRCP_ATTRIBUTES', 'TAVG', 'TAVG_ATTRIBUTES','TMAX', 'TMAX_ATTRIBUTES', 'TMIN', 'TMIN_ATTRIBUTES']]
        datedf=df[['DATE']].drop_duplicates()
        location=pd.concat([location, locationdf], ignore_index=True)
        dates=pd.concat([dates, datedf], ignore_index=True)
        weathers=pd.concat([weathers, weatherfact], ignore_index=True)
        
    return location,dates,weathers

#current_dir = os.path.dirname(os.path.abspath(__file__))
#algeria_folder = os.path.join(current_dir, '..', 'data/Algeria')
#morocco_folder = os.path.join(current_dir, '..', 'data/Morocco')
#tunisia_folder = os.path.join(current_dir, '..', 'data/Tunisia')
#csv_files1 = glob.glob(os.path.join(algeria_folder, '*.csv'))
#csv_files2 = glob.glob(os.path.join(morocco_folder, '*.csv'))
#csv_files3 = glob.glob(os.path.join(tunisia_folder, '*.csv'))
csv_files1 = ["data/Algeria/Weather_1920-1929_ALGERIA.csv","data/Algeria/Weather_1930-1939_ALGERIA.csv",
            "data/Algeria/Weather_1940-1949_ALGERIA.csv","data/Algeria/Weather_1950-1959_ALGERIA.csv",
            "data/Algeria/Weather_1960-1969_ALGERIA.csv","data/Algeria/Weather_1970-1979_ALGERIA.csv",
            "data/Algeria/Weather_1980-1989_ALGERIA.csv","data/Algeria/Weather_1990-1999_ALGERIA.csv",
            "data/Algeria/Weather_2000-2009_ALGERIA.csv","data/Algeria/Weather_2010-2019_ALGERIA.csv","data/Algeria/Weather_2020-2022_ALGERIA.csv"]
csv_files2 =[
    "data/Tunisia/Weather_1920-1959_TUNISIA.csv",
    "data/Tunisia/Weather_1960-1989_TUNISIA.csv",
    "data/Tunisia/Weather_1990-2019_TUNISIA.csv",
    "data/Tunisia/Weather_2020-2022_TUNISIA.csv",
]
csv_files3 = ["data/Morocco/Weather_1920-1959_MOROCCO.csv",
            "data/Morocco/Weather_1960-1989_MOROCCO.csv",
            "data/Morocco/Weather_1990-2019_MOROCCO.csv",
            "data/Morocco/Weather_2020-2022_MOROCCO.csv"]



algerialocation,algeriadate,algeriaweather=extraction(csv_files1) #algeria datas
tunisialocation,tunisiadate,tunisiaweather=extraction(csv_files2) #tunisia data
moroccolocation,moroccodate,moroccoweather=extraction(csv_files3) #morocco weather
print('extraction has been succsseful')

#######transformation ########
def traitment(df):
    df2=df.copy()
    for e in df.columns:
        if df[e].dtypes==object:
            df2[e]=df[e].astype(str)
            df2[e]=df[e].fillna(',,E')
        elif df[e].dtypes==float:
            df2[e]=df[e].fillna(value=0)
    return df2

alllocation=pd.concat([algerialocation,tunisialocation,moroccolocation])
alldates=pd.concat([algeriadate,tunisiadate,moroccodate])
alldates=alldates.drop_duplicates()
allweathers=pd.concat([algeriaweather,tunisiaweather,moroccoweather])

allweathers2=traitment(allweathers)

print("our fact table has been treatned")


###########LOAD################## 

#pour cree nos table
def create_table(CURSER, table_name, table_schema):
    
    sql = f"DROP TABLE IF EXISTS {table_name}"
    CURSER.execute(sql)
    sql = f"CREATE TABLE {table_name} ({table_schema})"
    CURSER.execute(sql)
    


# def get_attribute_type_index(schema, attribute_type):
#     row_splt = ","
#     ele_splt = " "

#     # Create a schema matrix, where the first column stores the attribute's name and the second its type
#     temp = schema.split(row_splt)
#     # Using list comprehension as shorthand
#     schema_matrix = [ele.split(ele_splt) for ele in temp]

#     # Get attributes' types list from schema_matrix
#     attributes_types = np.array(schema_matrix)[:, 1]

#     # Get all the indices of attributes of type 'attribute_type'
#     indices = [i for i, e in enumerate(attributes_types) if e.lower() == attribute_type.lower()]
#     return indices
    
# def populate_table(co_cursor, csv_path, table_name, attributes):
#     date_indices = get_attribute_type_index(attributes, 'DATE')
#     data = pd.read_csv(csv_path, sep=",", encoding='cp1252') 
    
#     for index, row in data.iterrows():
#         attribute_number = (row.size * '%s,')[:-1]
#         sql = "INSERT INTO " + table_name + " VALUES (" + attribute_number + ")"

#         # convert DATE attributes to MySQL format
#         if date_indices:
#             for date_index in date_indices:
#                 row[date_index] = datetime.strptime(row[date_index], '%Y/%m/%d').date()

#         co_cursor.execute(sql, tuple(row))
def creatDB(cursor):
    sql='CREATE DATABASE IF NOT EXISTS Weather_DataWarehouse'
    cursor.execute(sql)
    # cursor.close()
def populate_location_table(co_cursor, df):
    columns = ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION']
    for _, row in df.iterrows():
        placeholders = ','.join(['%s'] * len(columns))
        sql = f"INSERT INTO Location ({','.join(columns)}) VALUES ({placeholders})"
        co_cursor.execute(sql, tuple(row[columns]))

def populate_date_table(co_cursor, df):
    columns = ['DATE']
    for _, row in df.iterrows():
        sql = f"INSERT INTO Date ({','.join(columns)}) VALUES (%s)"
        co_cursor.execute(sql, tuple(row[columns]))

def populate_weather_fact_table(co_cursor, df):
    columns = ['STATION', 'DATE', 'PRCP', 'PRCP_ATTRIBUTES', 'TAVG', 'TAVG_ATTRIBUTES', 
               'TMAX', 'TMAX_ATTRIBUTES', 'TMIN', 'TMIN_ATTRIBUTES']
    for _, row in df.iterrows():
        placeholders = ','.join(['%s'] * len(columns))
        sql = f"INSERT INTO WeatherFact ({','.join(columns)}) VALUES ({placeholders})"
        co_cursor.execute(sql, tuple(row[columns]))
    
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                            #  database="Weather_DataWarehouse",
                            #  charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

creatDB(cursor)
table_schema = """
    STATION VARCHAR(50) PRIMARY KEY,
    NAME VARCHAR(255),
    LATITUDE FLOAT,
    LONGITUDE FLOAT,
    ELEVATION FLOAT
"""
create_table(cursor, "Location",table_schema = """
    STATION VARCHAR(50) PRIMARY KEY,
    NAME VARCHAR(255),
    LATITUDE FLOAT,
    LONGITUDE FLOAT,
    ELEVATION FLOAT
""")
print("Table Location created")

#### Create Date Table  
create_table(cursor, "Date", """
    DATE DATE PRIMARY KEY
""")
print("Table Date created")

#### Create WeatherFact Table
create_table(cursor, "WeatherFact", """
    STATION VARCHAR(50),
    DATE DATE,
    PRCP FLOAT,
    PRCP_ATTRIBUTES VARCHAR(10),
    TAVG FLOAT,
    TAVG_ATTRIBUTES VARCHAR(10), 
    TMAX FLOAT,
    TMAX_ATTRIBUTES VARCHAR(10),
    TMIN FLOAT,
    TMIN_ATTRIBUTES VARCHAR(10),
    PRIMARY KEY (STATION, DATE),
    FOREIGN KEY (STATION) REFERENCES Location(STATION),
    FOREIGN KEY (DATE) REFERENCES Date(DATE)
""")
print("Table WeatherFact created")

#### Create Date Algeria  
create_table(cursor, "Algeria", """
    STATION VARCHAR(255),
    NAME VARCHAR(255), 
    LATITUDE DOUBLE,
    LONGITUDE DOUBLE, 
    ELEVATION DOUBLE, 
    DATE DATE, 
    PRCP DOUBLE, 
    PRCP_ATTRIBUTES VARCHAR(255),     
    TAVG DOUBLE, 
    TAVG_ATTRIBUTES VARCHAR(255), 
    TMAX DOUBLE, 
    TMAX_ATTRIBUTES VARCHAR(255),   
    TMIN DOUBLE, 
    TMIN_ATTRIBUTES VARCHAR(255) 
""")
print("Table Algeria created")

# populate_location_table(co_cursor=cursor,df=alllocation)
print("location has been set")
# populate_date_table(co_cursor=cursor,df=alldates)
print("date table has been created")
print("data has been set succesfuly")
# create_table(cursor, "Location", ",STATION CHAR(11) NOT NULL, NAME varchar(25), LATITUDE float, "
                                #   "LONGITUDE float, ELEVATION float, PRIMARY KEY (STATION")

# create_table(cursor,"")

populate_weather_fact_table(co_cursor=cursor,df=allweathers2)
print("the weather fact has been created succssfully")