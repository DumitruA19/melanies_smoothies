import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """
  Chosse the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

session = st.connection("snowflake").session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))


pd_df = my_dataframe.to_pandas()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Get search value from df
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Show nutrition info
        st.subheader(f"{fruit_chosen} Nutrition Information")
        response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        if response.ok:
            st.dataframe(data=response.json(), use_container_width=True)
        else:
            st.error(f"Could not retrieve info for {fruit_chosen}")
          
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""

    # st.write(my_insert_stmt)
        time_to_insert= st.button('Submit Order!')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



