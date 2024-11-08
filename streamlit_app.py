# Import python packages
import streamlit as st
import snowflake.connector
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import requests

# Streamlit title and instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for smoothie name
name_on_order = st.text_input('Name on smoothie:')
st.write("The name on smoothie:", name_on_order)

# Set up the Snowflake connection
connection_parameters = {
    "account": "YOUR_ACCOUNT",
    "user": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "role": "YOUR_ROLE",
    "warehouse": "YOUR_WAREHOUSE",
    "database": "YOUR_DATABASE",
    "schema": "PUBLIC"
}

# Create Snowpark session
session = Session.builder.configs(connection_parameters).create()

# Retrieve fruit options as a list
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()
fruit_options = [row['FRUIT_NAME'] for row in my_dataframe]

# Multi-select for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options)

# Submit order if ingredients are selected
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    
    # Parameterized SQL insert statement
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (%s, %s)
    """
    
    # Button to submit the order
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        try:
            session.execute(my_insert_stmt, (ingredients_string, name_on_order))
            st.success('Your smoothie has been ordered!')
        except Exception as e:
            st.error(f"An error occurred: {e}")
