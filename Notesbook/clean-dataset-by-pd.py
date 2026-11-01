import pandas as pd

data = {
    "OrderID": [
        1001, 1002, 1003, 1004, 1005,
        1006, 1007, 1008, 1009, 1010,
        1011, 1012, 1013, 1014, 1015,
        1016, 1017, 1018, 1019, 1020
    ],

    "Date": [
        "2026-01-05", "2026-01-08", "2026-01-12",
        "2026-01-15", "2026-01-20", "2026-01-22",
        "2026-02-02", "2026-02-05", "2026-02-10",
        "2026-02-14", "2026-02-18", "2026-02-20",
        "2026-03-01", "2026-03-04", "2026-03-08",
        "2026-03-12", "2026-03-15", "2026-03-18",
        "2026-03-20", "2026-03-25"
    ],

    "Customer": [
        "Ali", "Sara", "Omar", "Ali", "Youssef",
        "Sara", "Mina", "Omar", "Ali", "Sara",
        "Youssef", "Mina", "Omar", "Ali", "Sara",
        "Mina", "Youssef", "Omar", "Sara", "Ali"
    ],

    "Product": [
        "Laptop", "Mouse", "Keyboard", "Laptop", "Monitor",
        "Mouse", "Laptop", "Keyboard", "Monitor", "Mouse",
        "Laptop", "Monitor", "Keyboard", "Laptop", "Mouse",
        "Monitor", "Keyboard", "Laptop", "Mouse", "Laptop"
    ],

    "Category": [
        "Electronics", "Accessories", "Accessories",
        "Electronics", "Electronics", "Accessories",
        "Electronics", "Accessories", "Electronics",
        "Accessories", "Electronics", "Electronics",
        "Accessories", "Electronics", "Accessories",
        "Electronics", "Accessories", "Electronics",
        "Accessories", "Electronics"
    ],

    "Quantity": [
        1, 3, 2, 1, 2, 4, 1, 2, 1, 5,
        1, 2, 3, 1, 2, 1, 4, 1, 3, 2
    ],

    "UnitPrice": [
        7000, 150, 350, 7000, 2500,
        150, 7000, 350, 2500, 150,
        7000, 2500, 350, 7000, 150,
        2500, 350, 7000, 150, 7000
    ],

    "City": [
        "Rabat", "Casablanca", "Sale", "Rabat", "Fes",
        "Casablanca", "Marrakech", "Sale", "Rabat",
        "Casablanca", "Fes", "Marrakech", "Sale",
        "Rabat", "Casablanca", "Marrakech", "Fes",
        "Sale", "Casablanca", "Rabat"
    ],

    "Payment": [
        "Card", "Cash", "Card", "Card", "Cash",
        "Card", "Cash", "Card", "Card", "Cash",
        "Card", "Cash", "Card", "Card", "Cash",
        "Card", "Cash", "Card", "Card", "Cash"
    ],

    "Rating": [
        5, 4, 3, 5, 4, 4, 5, None, 3, 4,
        5, None, 3, 5, 4, 3, None, 5, 4, 5
    ]
}

df = pd.DataFrame(data)

print(df)
# diplay the first and last five rows
print(df.head(5))
print(df.tail(5))
# find the number of rows and columns
print(df.shape)
# Check column types and missing values
print(df.info)
# Calculate descriptive statistics
des=df.describe()
print(round(des,2))
# Create a Revenue column = Quantity × UnitPrice.
df["Revenue"]=df["Quantity"]*df["UnitPrice"]
print(df["Revenue"])
# Convert Date into datetime format.
df["Date"]=pd.to_datetime(df["Date"], errors="coerce")
print(df["Date"])
# Extract the month into a new Month column.
df["Month"]=df["Date"].dt.month
print(df["Month"])
# Find the total revenue of all orders.
Totale_Revenue=df["Revenue"].sum()
print(Totale_Revenue)
# Calculate total revenue by City.
print(df.groupby("City")["Revenue"].sum())
# Calculate total revenue by Product.
print(df.groupby("Product")["Revenue"].sum())
# Find the average Rating for each Product.
print(round(df.groupby("Product")["Rating"].mean(),2))
# Count how many orders each Customer made.
print(df.groupby("Customer")["OrderID"].count())
# Create a pivot table showing total Revenue by Month and City.
summary=df.pivot_table(
    index="Month",
    columns="City",
    values="Revenue",
    fill_value=0
)
print(summary)
# Create another pivot table showing total Revenue by Product and Month.
summary_1=df.pivot_table(
    index="Product",
    columns="Month",
    values="Revenue",
    fill_value=0
)
print(round(summary_1,2))
# Find which city generated the highest revenue in each month.
summary_2=df.pivot_table(
    index="Month",
    columns="City",
    values="Revenue",
    aggfunc="max",
    fill_value=0
)
print(round(summary_2,2))
best_city = summary_2.idxmax(axis=1)
print(best_city)



#  Create a wide-format table: revenue by product/month
wide_df = df.pivot_table(
    index="Product",
    columns="Month",
    values="Revenue",
    aggfunc="sum",
    fill_value=0
).reset_index()

print("\n===== WIDE FORMAT =====")
print(wide_df)

#  Convert wide format into long format
long_df = wide_df.melt(
    id_vars="Product",
    var_name="Month",
    value_name="Revenue"
)

print("\n===== LONG FORMAT =====")
print(long_df)



#  Calculate average revenue for each city
df["City_Average"] = (
    df.groupby("City")["Revenue"].transform("mean")
)

print("\n===== CITY AVERAGE =====")
print(df[["City", "Revenue", "City_Average"]])


#  Rank orders by revenue
df["Revenue_Rank"] = df["Revenue"].rank(
    ascending=False,
    method="dense"
)

print("\n===== REVENUE RANKING =====")
print(
    df[["OrderID", "Product", "Revenue", "Revenue_Rank"]]
    .sort_values("Revenue_Rank")
)


#  Classify orders into Low, Medium and High
df["Revenue_Level"] = pd.qcut(
    df["Revenue"],
    q=3,
    labels=["Low", "Medium", "High"]
)

print("\n===== REVENUE LEVEL =====")
print(df[["OrderID", "Revenue", "Revenue_Level"]])


#  Create customer information dataset
customers = pd.DataFrame({
    "Customer": ["Ali", "Sara", "Omar", "Youssef", "Mina"],
    "Age": [28, 32, 25, 35, 29],
    "Membership": ["Gold", "Silver", "Bronze", "Gold", "Silver"]
})

#  Merge orders with customer information
merged_df = pd.merge(
    df,
    customers,
    on="Customer",
    how="left"
)

print("\n===== MERGED DATASET =====")
print(
    merged_df[
        ["OrderID", "Customer", "Age", "Membership", "Revenue"]
    ]
)




#  Total revenue
total_revenue = df["Revenue"].sum()

#  Revenue by product
product_revenue = (
    df.groupby("Product")["Revenue"].sum()
    .sort_values(ascending=False)
)

#  Revenue by city
city_revenue = (
    df.groupby("City")["Revenue"].sum()
    .sort_values(ascending=False)
)

#  Revenue by month
month_revenue = (
    df.groupby("Month")["Revenue"].sum()
    .sort_values(ascending=False)
)

#  Number of orders by customer
customer_orders = (
    df.groupby("Customer")["OrderID"].count()
    .sort_values(ascending=False)
)

#  Average rating
average_rating = df["Rating"].mean()

#  Revenue by payment method
payment_revenue = (
    df.groupby("Payment")["Revenue"].sum()
    .sort_values(ascending=False)
)

#  Highest revenue product, city and month
best_product = product_revenue.idxmax()
best_city = city_revenue.idxmax()
best_month = month_revenue.idxmax()
best_customer = customer_orders.idxmax()

#  Monthly revenue by product
monthly_report = df.pivot_table(
    index="Product",
    columns="Month",
    values="Revenue",
    aggfunc="sum",
    fill_value=0
)




print("\n======================================")
print("       ONLINE STORE BUSINESS REPORT")
print("======================================")

print("\nTOTAL REVENUE:")
print(total_revenue)

print("\nREVENUE BY PRODUCT:")
print(product_revenue)

print("\nBEST PRODUCT:")
print(best_product)

print("\nREVENUE BY CITY:")
print(city_revenue)

print("\nBEST CITY:")
print(best_city)

print("\nREVENUE BY MONTH:")
print(month_revenue)

print("\nBEST MONTH:")
print(best_month)

print("\nNUMBER OF ORDERS BY CUSTOMER:")
print(customer_orders)

print("\nCUSTOMER WITH MOST ORDERS:")
print(best_customer)

print("\nAVERAGE CUSTOMER RATING:")
print(round(average_rating, 2))

print("\nREVENUE BY PAYMENT METHOD:")
print(payment_revenue)

print("\nMONTHLY REVENUE BY PRODUCT:")
print(monthly_report)




df.to_csv("online_store_analysis.csv", index=False)

long_df.to_csv("sales_long_format.csv", index=False)

monthly_report.to_csv("monthly_product_report.csv")

merged_df.to_csv("orders_with_customers.csv", index=False)

print("\nAll reports exported successfully!")
