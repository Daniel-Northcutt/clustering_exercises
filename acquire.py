import os
import pandas as pd
from env import host, user, password
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

#******************* ACQUIRE  ***********************
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
#******************* SQL QUERY IMPORT ***********************
def new_zillow_data():
    '''
    This function reads in Zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    sql_query = """ 
SELECT prop.*, 
       pred.logerror, 
       pred.transactiondate, 
       air.airconditioningdesc, 
       arch.architecturalstyledesc, 
       build.buildingclassdesc, 
       heat.heatingorsystemdesc, 
       landuse.propertylandusedesc, 
       story.storydesc, 
       construct.typeconstructiondesc 

FROM   properties_2017 prop  
INNER JOIN (SELECT parcelid,logerror,
            Max(transactiondate) transactiondate 
            FROM   predictions_2017 
            GROUP  BY parcelid, logerror) pred
           USING (parcelid) 
LEFT JOIN airconditioningtype air USING (airconditioningtypeid) 
LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid) 
LEFT JOIN buildingclasstype build USING (buildingclasstypeid) 
LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid) 
LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid) 
LEFT JOIN storytype story USING (storytypeid) 
LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid) 
WHERE  prop.latitude IS NOT NULL 
AND prop.longitude IS NOT NULL
AND transactiondate < "2018-01-01";
"""

     # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df

#******************* GET THE DATA & CREATE CSV ***********************

def get_zillow_data():
    '''
    This function reads in zillow data from the Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('zillow.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('zillow.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_zillow_data()
        
        # Cache data
        df.to_csv('zillow.csv')
        
    return df