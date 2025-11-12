# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """
  Chosse the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session

# Get fruit names from Snowflake as a Python list
fruit_rows = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
fruit_names = [row['FRUIT_NAME'] for row in fruit_rows]

# Show multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names,
    max_selections=5
)


if ingredients_list:
    ingredients_string = ''

    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""

    # st.write(my_insert_stmt)
    time_to_insert= st.button('Submit Order!')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


    
