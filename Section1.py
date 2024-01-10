@st.cache_resource
def create_session():
   #Creates a Snowflake session and caches it for performance optimization.
    return Session.builder.configs(
        {"user" :"Datasnowflake",
        "password" : "Karthiksara@2123",
        "account" : "wyb73440.us-east-1",
        "warehouse" : "COMPUTE_WH",
        "database" : "DB_ONLINE_RETAIL",
        "schema" : "PUBLIC"}).create()

# Create and retrieve the Snowflake session
session=create_session()
session = get_active_session()# Ensure we have the active session

# Set parameters for data retrieval
page_size = 20000  # Number of rows per page
current_page = 1  # Initial page number
start_index = (current_page - 1) * page_size

# SQL query to retrieve data from the Snowflake table
sql_query = f"""
    SELECT *
    FROM ONLINERETAILTABLE  
    LIMIT {page_size} OFFSET {start_index}
"""
ONLINERETAILTABLE_data = session.sql(sql_query).collect()
# Create a Pandas DataFrame for easier data manipulation
ONLINERETAILTABLE_df = pd.DataFrame(ONLINERETAILTABLE_data)
print(ONLINERETAILTABLE_df.shape)
