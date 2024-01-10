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
