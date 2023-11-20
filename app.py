# Libraries to be used
import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(page_title='Total Discount, Profit, Goods Sold for Each Region and State in USA', page_icon=":bar_chart:", layout='wide')

# Storing data in cache to conserve memory
@st.cache_data
def get_data_from_csv():
    store_data = pd.read_csv('SampleSuperstore.csv')
    return store_data

# Calling function into variable
store_data = get_data_from_csv()

# ---SIDEBAR---
st.sidebar.header('Please filter here')

# # Filtering by city
# city = st.sidebar.multiselect("Select the city:", options=store_data['City'].unique(), default=store_data['City'].unique())

# Filtering by region
region = st.sidebar.multiselect("Select the region:", options=store_data['Region'].unique(), default=store_data['Region'].unique())

# Filtering by class of shipping
ship_mode = st.sidebar.multiselect("Select the shipping class:", options=store_data['Ship Mode'].unique(), default=store_data['Ship Mode'].unique())

# Filtering by state
state = st.sidebar.multiselect("Select the state:", options=store_data['State'].unique(), default=store_data['State'].unique())

# Filter by category
category = st.sidebar.multiselect("Select the category:", options=store_data['Category'].unique(), default=store_data['Category'].unique())

# Filter by sub-category
sub_category = st.sidebar.multiselect("Select the sub-category:", options=store_data['Sub-Category'].unique(), default=store_data['Sub-Category'].unique())

# Filtering based on variables
df_selection = store_data.query(
    "(`Region` == @region) & (`State` == @state) & (`Category` == @category) & (`Sub-Category` == @sub_category)"
)

# MAIN PAGE
st.title(":bar_chart: Total Discount, Profit, Goods Sold for Each Region and State in USA")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection['Sales'].sum())
total_profit = round(df_selection['Profit'].sum(), 1)
total_discount = round(df_selection['Discount'].sum(), 1)

# Columns
left_column, middle_column, right_column = st.columns(3)

# Data in columns
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Total Profit")
    st.subheader(f"US $ {total_profit:,}")
with right_column:
    st.subheader("Total Discount")
    st.subheader(f"US $ {total_discount:,}")

# Total Goods Sold by 'Ship Mode'
total_goods_sold_by_ship_mode = df_selection.groupby('Ship Mode')['Quantity'].sum().reset_index()

# Pie Chart for total goods sold by 'Ship Mode'
fig_goods_sold_by_ship_mode = px.pie(
    total_goods_sold_by_ship_mode,
    values='Quantity',
    names='Ship Mode',
    title="<b>Total Goods Sold by Ship Mode<b>",
    template='plotly_white'
)

# Visualizations
st.markdown("---")
st.plotly_chart(fig_goods_sold_by_ship_mode)

# Calculations for visualizations
# By region
total_profit_by_region = df_selection.groupby(by='Region').sum()[['Profit']].sort_values(by='Profit')
total_discount_by_region = df_selection.groupby(by='Region').sum()[['Discount']].sort_values(by='Discount')
total_sales_by_region = df_selection.groupby(by='Region').sum()[['Sales']].sort_values(by='Sales')

# By state
total_profit_by_state = df_selection.groupby(by='State').sum()[['Profit']].sort_values(by='Profit')
total_discount_by_state = df_selection.groupby(by='State').sum()[['Discount']].sort_values(by='Discount')
total_sales_by_state = df_selection.groupby(by='State').sum()[['Sales']].sort_values(by='Sales')

# Visualizations for regions
# For the sales
fig_product_sales = px.bar(
    total_sales_by_region,
    x='Sales',
    y=total_sales_by_region.index,
    orientation='h',
    title="<b>Total Sales Per Region<b>",
    template='plotly_white'
)

# For the profit
fig_product_profit = px.bar(
    total_profit_by_region,
    x='Profit',
    y=total_profit_by_region.index,
    orientation='h',
    title="<b>Total Profit Per Region<b>",
    template='plotly_white'
)

# For the discount
fig_product_discount = px.bar(
    total_discount_by_region,
    x='Discount',
    y=total_discount_by_region.index,
    orientation='h',
    title="<b>Total Discount Per Region<b>",
    template='plotly_white'
)

# Horizontal bar plots
st.plotly_chart(fig_product_sales)
st.plotly_chart(fig_product_profit)
st.plotly_chart(fig_product_discount)

# Visualizations for states
# For the sales
fig_product_sales = px.bar(
    total_sales_by_state,
    x='Sales',
    y=total_sales_by_state.index,
    orientation='h',
    title="<b>Total Sales Per State<b>",
    template='plotly_white'
)

# For the profit
fig_product_profit = px.bar(
    total_profit_by_state,
    x='Profit',
    y=total_profit_by_state.index,
    orientation='h',
    title="<b>Total Profit Per State<b>",
    template='plotly_white'
)

# For the discount
fig_product_discount = px.bar(
    total_discount_by_state,
    x='Discount',
    y=total_discount_by_state.index,
    orientation='h',
    title="<b>Total Discount Per State<b>",
    template='plotly_white'
)

# Horizontal bar plots
st.plotly_chart(fig_product_sales)
st.plotly_chart(fig_product_profit)
st.plotly_chart(fig_product_discount)