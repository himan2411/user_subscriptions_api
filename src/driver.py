""" This is the driver to perform the pipeline operations"""
from utils import loader
from config.config import USER_TABLE, MESSAGE_TABLE, SUBSCRIPTION_TABLE
from utils.logger import ETL_logger

logger = ETL_logger('driver')

def main():
    logger.log("Get the data from API")
    loader_obj = loader.Loader()
    df_user = loader_obj.load_users()
    df_messages = loader_obj.load_messages()
    df_subscriptions = loader_obj.load_subscriptions()

    logger.log("Push the data to SQL")
    loader_obj.push_to_sql(df_user, USER_TABLE)
    loader_obj.push_to_sql(df_messages, MESSAGE_TABLE)
    loader_obj.push_to_sql(df_subscriptions, SUBSCRIPTION_TABLE)

if __name__ == "__main__":
    main()

