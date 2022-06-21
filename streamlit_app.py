import streamlit

print("Hello World")

streamlit.header('Breakfast Menu for Morning')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect('pick some fruits',list(my_fruit_list.index), ['Avocado','Strawberries'] )
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

import requests
fruityvice_response=requests.get("https://fruityvice.com/api/fruit/all")
fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)


import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit List Contains:")
streamlit.dataframe(my_data_rows)

my_cur.execute("insert into fruit_load_list values ('from Streamlit')")

streamlit.header('Fruitvice Fruit Advice')

try:
  fruit_choice=streamlit.text_input('what fruit would you like infromation about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
      fruitvice_response=requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
      fruitvice_normalized=pandas.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruitvice_normalized)
except URLError as e:
    streamlit.error()
