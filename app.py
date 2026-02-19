import streamlit as st
import snowflake.connector
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Snowflake Warehouse Usage",
    page_icon="❄️",
    layout="wide"
)

# Title
st.title("❄️ Snowflake Warehouse Usage Visualization")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    days = st.slider("Select number of days", min_value=1, max_value=90, value=7)
    
    st.info(f"Analyzing warehouse usage for the last {days} days")

# Function to connect to Snowflake
@st.cache_resource
def get_snowflake_connection():
    """Create a connection to Snowflake using externalbrowser authenticator"""
    try:
        conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            authenticator='externalbrowser',
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA'),
            role=os.getenv('SNOWFLAKE_ROLE')
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None

# Function to query warehouse usage
def get_warehouse_usage(conn, days):
    """Query warehouse usage from Snowflake for the last N days"""
    try:
        query = f"""
        SELECT 
            TO_DATE(START_TIME) as DATE,
            WAREHOUSE_NAME,
            SUM(CREDITS_USED) as TOTAL_CREDITS,
            COUNT(*) as QUERY_COUNT
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        WHERE START_TIME >= DATEADD(day, -{days}, CURRENT_TIMESTAMP())
        GROUP BY TO_DATE(START_TIME), WAREHOUSE_NAME
        ORDER BY DATE DESC, TOTAL_CREDITS DESC
        """
        
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Fetch results and convert to DataFrame
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        
        cursor.close()
        return df
    except Exception as e:
        st.error(f"Failed to query warehouse usage: {str(e)}")
        return None

# Main app logic
def main():
    # Connect to Snowflake
    with st.spinner("Connecting to Snowflake..."):
        conn = get_snowflake_connection()
    
    if conn is None:
        st.warning("Please configure your Snowflake connection in the .env file")
        st.info("Required variables: SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, SNOWFLAKE_ROLE")
        return
    
    # Query warehouse usage
    with st.spinner(f"Fetching warehouse usage for the last {days} days..."):
        df = get_warehouse_usage(conn, days)
    
    if df is None or df.empty:
        st.warning("No warehouse usage data found for the selected period.")
        return
    
    # Display metrics
    st.header("📊 Summary Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_credits = df['TOTAL_CREDITS'].sum()
        st.metric("Total Credits Used", f"{total_credits:.2f}")
    
    with col2:
        total_queries = df['QUERY_COUNT'].sum()
        st.metric("Total Queries", f"{int(total_queries):,}")
    
    with col3:
        unique_warehouses = df['WAREHOUSE_NAME'].nunique()
        st.metric("Active Warehouses", unique_warehouses)
    
    # Visualizations
    st.header("📈 Usage Trends")
    
    # Credits over time
    st.subheader("Credits Used Over Time")
    daily_credits = df.groupby('DATE')['TOTAL_CREDITS'].sum().reset_index()
    st.line_chart(daily_credits.set_index('DATE'))
    
    # Credits by warehouse
    st.subheader("Credits Used by Warehouse")
    warehouse_credits = df.groupby('WAREHOUSE_NAME')['TOTAL_CREDITS'].sum().reset_index()
    warehouse_credits = warehouse_credits.sort_values('TOTAL_CREDITS', ascending=False)
    st.bar_chart(warehouse_credits.set_index('WAREHOUSE_NAME'))
    
    # Raw data
    st.header("📋 Detailed Data")
    st.dataframe(
        df.sort_values('DATE', ascending=False),
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()
