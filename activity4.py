import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# --------------------------
# Database Configuration
# --------------------------
DB_USER = 'root'
DB_PASSWORD = None  # or your actual password as a string
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'foods'  # Replace with your actual DB name

@st.cache_resource
def get_connection():
    if DB_PASSWORD is None:
        connection_url = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_url)

engine = get_connection()

# --------------------------
# Authentication
# --------------------------
st.sidebar.header("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

def authenticate(user, pwd):
    return user == "admin" and pwd == "school123"  # Hardcoded admin login

if authenticate(username, password):
    st.success(f"Welcome, {username} 👋")
    st.title("🏫 School Management Dashboard")

    # --------------------------
    # Table Selector
    # --------------------------
    table = st.selectbox("Select Table", ["menu", "orders"])

    # --------------------------
    # Table Viewer with Filter
    # --------------------------
    st.subheader("📄 Table Viewer")
    filter_query = st.text_input("Optional SQL Filter (e.g., item_name LIKE '%Pizza%')")

    view_query = f"SELECT * FROM {table}"
    if filter_query.strip():
        view_query += f" WHERE {filter_query}"

    with engine.connect() as conn:
        df = pd.read_sql(text(view_query), conn)
    st.dataframe(df)

    # --------------------------
    # Insert New Record
    # --------------------------
    st.subheader(f"➕ Add New Record to `{table}`")
    with st.form(key="insert_form"):
        with engine.connect() as conn:
            if table == "menu":
                item_name = st.text_input("Menu Item Name")
                item_description = st.text_area("Description")
                price = st.number_input("Price", min_value=0.0, format="%.2f")
                submit = st.form_submit_button("Insert Menu Item")
                if submit:
                    conn.execute(text("""
                        INSERT INTO menu (item_name, item_description, price)
                        VALUES (:name, :description, :price)
                    """), {"name": item_name, "description": item_description, "price": price})
                    conn.commit()
                    st.success("✅ Menu item added!")

            elif table == "orders":
                order_date = st.date_input("Order Date")
                customer_name = st.text_input("Customer Name")
                total_amount = st.number_input("Total Amount", min_value=0.0, format="%.2f")
                submit = st.form_submit_button("Insert Order")
                if submit:
                    conn.execute(text("""
                        INSERT INTO orders (order_date, customer_name, total_amount)
                        VALUES (:order_date, :customer_name, :total_amount)
                    """), {"order_date": order_date, "customer_name": customer_name, "total_amount": total_amount})
                    conn.commit()
                    st.success("✅ Order inserted!")

else:
    st.warning("🔐 Please log in with valid credentials.")
