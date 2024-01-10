st.divider()
st.markdown(":red[**Tracking Daily Revenue 🗓️💵**]")


Country_ONLINERETAIL_df["date"] = pd.to_datetime(Country_ONLINERETAIL_df["INVOICEDATE"])
Country_ONLINERETAIL_df["day"] = Country_ONLINERETAIL_df["date"].dt.date


daily_totals = Country_ONLINERETAIL_df.groupby("day")["Total_price"].sum()


start_date, end_date = st.date_input(
    "Select date range:",
    [Country_ONLINERETAIL_df["day"].min(), Country_ONLINERETAIL_df["day"].max()],
)


daily_totals = daily_totals.reset_index()
df_filtered = daily_totals[(daily_totals["day"] >= start_date) & (daily_totals["day"] <= end_date)]


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
st.altair_chart(chart, use_container_width=True)
