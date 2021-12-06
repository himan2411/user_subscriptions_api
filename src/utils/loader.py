""""This is a utility to extract the data from API and load the data to SQL  """
import pandas as pd
import numpy as np
import hashlib
import logging
from numpy import nan as Nan
from dbutils.db_sql import create_sql_engine
from utils.logger import ETL_logger
from config.config import MESSAGE_TABLE, USER_URL, MESSAGE_URL, USER_TABLE, SUBSCRIPTION_TABLE

pd.options.mode.chained_assignment = None

class Loader:
    def __init__(self):
        # Get the environment, config, and initialize the module
        self.conn = create_sql_engine()
        self.logger = ETL_logger()
    
    def load_users(self):
        self.logger.log("Startring the USER table load")
        try:
            df_users = pd.read_json(USER_URL)
            profile_dict = df_users['profile']
            df_profile = pd.DataFrame([x for x in profile_dict])
            df_users = pd.concat([df_users, df_profile], axis=1)
            #Take only the necessary columns and follow camel case for column names
            df_users = df_users[['id','createdAt','updatedAt','firstName','lastName','address','city','country','zipCode','email','birthDate','gender','isSmoking','profession','income']]
            df_users = df_users.rename(columns={"id": "user_id"})
            
            # Hide PII's
            df_users[['firstName','lastName','address','birthDate']] = df_users[['firstName','lastName','address','birthDate']].astype(str)
            columns=['firstName','lastName','address','birthDate']
            for column in columns:
                df_users[column] = df_users[column].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
            
            #extract domain from emails
            df_users['email']=df_users['email'].str.extract('((?<=@).*)')
            self.logger.log("Load of USER table data complete") 

        except Exception as e:
            self.logger.log(f"Failed to load the user data with error {e}")
            df_users = pd.DataFrame()
        
        return df_users

    def load_messages(self):
        self.logger.log("Startring the MESSAGES table load")
        try:  
            df_messages=pd.read_json(MESSAGE_URL)
            
            #hash messages for data compliance
            df_messages['message']=df_messages['message'].astype(str)
            df_messages['message'] = df_messages['message'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
            self.logger.log("Load of MESSAGES table data complete") 

        except Exception as e:
            self.logger.log(f"Failed to load the messages data with error {e}")
            df_messages = pd.DataFrame()
        
        return df_messages

    def load_subscriptions(self):
        self.logger.log("Startring the subscriptions table load")
        try: 
            df_users = pd.read_json(USER_URL)
            subscription_df = df_users[['id','subscription']]
            subscription_df = subscription_df.explode('subscription')
            df = pd.DataFrame(columns = ['createdAt', 'startDate','endDate','status','amount','id'])
            #Populate the dataframe row by row
            for _, row in subscription_df.iterrows():
                if row['subscription'] is not Nan:
                    dicts=row['subscription']
                    dicts['id']=row['id']
                    df = df.append(dicts, ignore_index=True, sort=False)
                else:
                    df2 = {'createdAt': Nan, 'startDate': Nan, 'endDate':Nan, 'status': Nan, 'amount': Nan, 'id': row['id'], }
                    df = df.append(df2, ignore_index = True)

            df = df.rename(columns={"id": "user_id"})
            self.logger.log("Load of USER table data complete")

        except Exception as e:
            self.logger.log(f"Failed to load the sunscription data with error {e}", logging.ERROR)
            df = pd.DataFrame()
        
        return df

    def push_to_sql(self, df, table_name):
        self.logger.log(f"Pushing {table_name} dataframe to SQL")
        try:
            df.to_sql(con=self.conn, name=SUBSCRIPTION_TABLE, if_exists='replace', index=False)
            self.logger.log(f"{table_name} pushed to SQL successfully")

        except Exception as e:
            self.logger.log(f"Failed to load the {table_name} data to SQL with error {e}", logging.ERROR)
    
    def save_as_csv(self, df, file_path):
        self.logger.log(f"Pushing dataframe to SQL")
        try:
            df.to_csv(file_path, delimiter = "|" )
            self.logger.log(f"Dataframe pushed to SQL successfully")

        except Exception as e:
            self.logger.log(f"Failed to save the data to CSV with error {e}", logging.ERROR)


