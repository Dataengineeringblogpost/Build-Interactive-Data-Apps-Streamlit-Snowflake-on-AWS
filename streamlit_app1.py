# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd 
import altair as alt
from snowflake.snowpark import Session

@st.cache_resource
def create_session():
   #Creates a Snowflake session and caches it for performance optimization.
    return Session.builder.configs(
        {"user" :"<user name>",
        "password" : "<password>",
        "account" : "<account id>",
        "warehouse" : "<warehouse name>",
        "database" : "<database name>",
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

#Title and Adding a descriptive second text box with emojis 
st.title("Customer Purchase Analytics 📊🛍️")
st.write(
    """
    Dive deep into customer purchase insights! 🕵️‍♂️🔍
    Explore trends, patterns, and key metrics to uncover valuable business information 📈💡.
    Get ready to unlock actionable insights and make data-driven decisions 🚀📊. 
    """
)
st.divider()

#Select a country option 
country_options = ONLINERETAILTABLE_df['COUNTRY'].value_counts().index.to_list()
selected_options = st.selectbox("Choose country 🗺️", country_options)
#Get the country option 
@st.cache_data
def get_selected_options(selected_options):
    st.write(selected_options)
    return selected_options
selected_options=get_selected_options(selected_options)
Country_ONLINERETAIL_df=ONLINERETAILTABLE_df[ONLINERETAILTABLE_df['COUNTRY']==selected_options]

#Creating a new column Total_price using quantity and unitprice columns 
Country_ONLINERETAIL_df['Total_price'] = Country_ONLINERETAIL_df.apply(lambda row: float(row['QUANTITY']) * float(row['UNITPRICE']), axis=1)

st.divider()
#Create sum and avg
sum_total_price=Country_ONLINERETAIL_df['Total_price'].sum()
avg_total_price=Country_ONLINERETAIL_df['Total_price'].mean()
with st.container():

    st.markdown(":red[**Customer Purchase Insights 🛍️💰**]")

    # Display sum_total_price and avg_total_price
    st.write(f"Total Purchase Amount: ${sum_total_price:.2f}")
    st.write(f"Average Purchase Amount: ${avg_total_price:.2f}")

st.divider()
#Create sum and avg
sum_QUANTITY=Country_ONLINERETAIL_df['QUANTITY'].astype(int).sum()
avg_QUANTITY=Country_ONLINERETAIL_df['QUANTITY'].astype(int).mean()
with st.container():

    st.markdown(":red[**Quantity Quickview 📊🎯**]")

    # Display quantity and avg_total_price
    st.write(f"Total Quantity : {sum_QUANTITY:.2f}")
    st.write(f"Average Quantity : {avg_QUANTITY:.2f}")


st.divider()
st.markdown(":red[**Frequently brought Products ⌛🛒**]")
#Displays the product name and its frequency 
Most_brought_products = Country_ONLINERETAIL_df["DESCRIPTION"].value_counts()
st.write(Most_brought_products)

st.divider()
st.markdown(":red[**Tracking Daily Revenue 🗓️💵**]")
Country_ONLINERETAIL_df["date"] = pd.to_datetime(Country_ONLINERETAIL_df["INVOICEDATE"])
Country_ONLINERETAIL_df["day"] = Country_ONLINERETAIL_df["date"].dt.date 
# Calculate daily total price sums
daily_totals = Country_ONLINERETAIL_df.groupby("day")["Total_price"].sum()

start_date, end_date = st.date_input(
    "Select date range:",
    [Country_ONLINERETAIL_df["day"].min(), Country_ONLINERETAIL_df["day"].max()],
)
daily_totals = daily_totals.reset_index()

# Filter data based on selected range
df_filtered = daily_totals[(daily_totals["day"] >= start_date) & (daily_totals["day"] <= end_date)]
# Create the Altair line chart
st.table(df_filtered)
chart = (
    alt.Chart(df_filtered.reset_index())
    .mark_line()
    .encode(
        x="day",  # Specify date as temporal type
        y="Total_price",
    )
    .properties(title=f"Daily Sales - {start_date}-{end_date}")
)

# Display the chart
st.altair_chart(chart, use_container_width=True)
