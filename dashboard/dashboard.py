import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from func import DataAnalyzer

sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("dashboard/all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    
    # Title
    st.title("QLIT")
    st.write("Make It Easier")

    #Image
    st.image("dashboard/qlit.png")

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Convert date inputs to pandas Timestamp objects
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)

sum_order_items_df = function.create_sum_order_items_df()
monthly_transactions_df = function.create_monthly_transactions_df()
monthly_sells_df = function.create_monthly_sells_df()
order_status, common_status = function.create_order_status()
state, most_common_state = function.create_bystate_df()
city, most_common_city = function.create_bycity_df()
review_score, common_score = function.review_score_df()


# Title
st.header("✨Welcome to QLIT E-Commerce Dashboard✨")

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

colors = ["#CD5C5C", "#FFA07A", "#FFA07A", "#FFA07A", "#FFA07A",  "#FFA07A",  "#FFA07A",  "#FFA07A",  "#FFA07A",  "#FFA07A"]

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.head(10), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Most sold products", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(10), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least sold product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Monthly Transaction
st.subheader("Monthly Transactions")
main_df = all_df[(all_df["order_approved_at"] >= start_date) & 
                 (all_df["order_approved_at"] <= end_date)]

function = DataAnalyzer(main_df)
monthly_transactions_df = function.create_monthly_transactions_df()

# Plot
fig = plt.figure(figsize=(10, 5))  # Create a figure
plt.plot(
    monthly_transactions_df["order_approved_at"],
    monthly_transactions_df["total_transactions"],
    marker='o',
    linewidth=2,
    color="#CD5C5C")

plt.title("Total customer transactions per month in the last 1 year", loc="center", fontsize=20)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Transactions", fontsize=12)
plt.xticks(fontsize=10, rotation=25)
plt.yticks(fontsize=10)
plt.grid(True)
st.pyplot(fig)

#Monthly Sells
st.subheader("Product Sales per Month")
main_df = all_df[(all_df["order_approved_at"] >= start_date) & 
                 (all_df["order_approved_at"] <= end_date)]

function = DataAnalyzer(main_df)
monthly_sells_df = function.create_monthly_sells_df()

# Plot
fig = plt.figure(figsize=(10, 5))
plt.plot(
    monthly_sells_df["order_approved_at"],
    monthly_sells_df["order_count"],
    marker='o',
    linewidth=2,
    color="#CD5C5C"
)
plt.title("Total Product Sales per Month in 1 Year", loc="center", fontsize=20)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of Sale", fontsize=12)
plt.xticks(fontsize=10, rotation=25)
plt.yticks(fontsize=10)
plt.grid(True)
st.pyplot(fig)


# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2, tab3 = st.tabs(["Order Status", "State", "City"])

with tab1:
    common_status_ = order_status.value_counts().index[0]
    st.markdown(f"Most Common Order Status: **{common_status_}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=order_status.index,
                y=order_status.values,
                order=order_status.index,
                palette=["#CD5C5C" if score == common_status else "#FFA07A" for score in order_status.index]
                )
    
    plt.title("Order Status", fontsize=15)
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.xticks(fontsize=12)
    st.pyplot(fig)


with tab2:
    most_common_state = state.customer_state.value_counts().index[0]
    st.markdown(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state.customer_state.value_counts().index,
                y=state.customer_count.values, 
                data=state,
                palette=["#CD5C5C" if score == most_common_state else "#FFA07A" for score in state.customer_state.value_counts().index]
                    )

    plt.title("Number customers from State", fontsize=15)
    plt.xlabel("State")
    plt.ylabel("Number of Customers")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

with tab3:
    most_common_city = city.customer_city.value_counts().index[0]
    st.markdown(f"Most Common City: **{most_common_city}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=city.customer_city.value_counts().index,
                y=city.customer_count.values, 
                data=city,
                palette=["#CD5C5C" if score == most_common_city else "#FFA07A" for score in city.customer_city.value_counts().index]
                    )

    plt.title("Number customers from City", fontsize=15)
    plt.xlabel("City")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=45, fontsize=10)
    st.pyplot(fig)

# Review Score
st.subheader("Review Score")
col1,col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Average Review Score: **{avg_review_score}**")

with col2:
    most_common_review_score = review_score.value_counts().index[0]
    st.markdown(f"Most Common Review Score: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=review_score.index, 
            y=review_score.values, 
            order=review_score.index,
            palette=["#CD5C5C" if score == common_score else "#FFA07A" for score in review_score.index]
            )

plt.title("Rating by customers for service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
st.pyplot(fig)

st.caption('Copyright (C) Shafira Fimelita Q - 2024')

