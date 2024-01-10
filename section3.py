Country_ONLINERETAIL_df['Total_price'] = Country_ONLINERETAIL_df.apply(lambda row: float(row['QUANTITY']) * float(row['UNITPRICE']), axis=1)

st.divider()

sum_total_price=Country_ONLINERETAIL_df['Total_price'].sum()
avg_total_price=Country_ONLINERETAIL_df['Total_price'].mean()

with st.container():

    st.markdown(":red[**Customer Purchase Insights 🛍️💰**]")
    st.write(f"Total Purchase Amount: ${sum_total_price:.2f}")
    st.write(f"Average Purchase Amount: ${avg_total_price:.2f}")

st.divider()

sum_QUANTITY=Country_ONLINERETAIL_df['QUANTITY'].astype(int).sum()
avg_QUANTITY=Country_ONLINERETAIL_df['QUANTITY'].astype(int).mean()

with st.container():

    st.markdown(":red[**Quantity Quickview 📊🎯**]")
    st.write(f"Total Quantity : {sum_QUANTITY:.2f}")
    st.write(f"Average Quantity : {avg_QUANTITY:.2f}")


st.divider()
st.markdown(":red[**Frequently brought Products ⌛🛒**]")
Most_brought_products = Country_ONLINERETAIL_df["DESCRIPTION"].value_counts()
st.write(Most_brought_products)

