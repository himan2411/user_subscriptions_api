This is the ETL pipeline written in Python to implement given functionality 

## Workflow
  - We start by getting the data from the given API endpoints.
  - We load the json directly to pandas dataframe using pandas mehtods.
  - To comply with GDPR guidelines we process the data to remove any PIIs. I'm using hashlib to hash these information
  - This new data is then pushed to the MySQL database
  - There are two configs available (cuurently both are same) for development and production
  - You can use environment variable to define the type of environment prod or dev
  - config.py in config folder will automatiicaly read the config from the apropriate json config
  - config.py enables the use of these config properties to rest of the code without exposing the json properties directly

## Usage
  
  - Single point of execution is driver.py (present in the src folder)
  - Internally it uses logger and loader class from utils to implement the extract and load phase


Please feel free to let me know if there is any concerns or if you have any questions :)








