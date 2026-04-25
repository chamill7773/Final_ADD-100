"""
SHOE STORE SALES TRACKER - STREAMLIT VERSION
Retro Sports Store Theme
"""

import streamlit as st
import pandas as pd
import datetime
from shoe_order import ShoeOrder
import os

# PAGE CONFIG
st.set_page_config(
    page_title="🏃 Retro Sports Tracker",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# RETRO SPORTS STORE STYLING
st.markdown("""
<style>
    /* Retro Color Scheme - Orange, Yellow, Purple */
    :root {
        --retro-orange: #FF6B35;
        --retro-yellow: #FFD700;
        --retro-purple: #6A0DAD;
        --retro-dark: #1a1a1a;
        --retro-light: #F5F5F5;
    }
    
    .main {
        background-color: #F5F5F5;
    }
    
    /* Header styling */
    .retro-header {
        background: linear-gradient(135deg, #FF6B35 0%, #6A0DAD 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        font-size: 32px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-family: 'Arial Black', sans-serif;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #FF6B35;
        color: white;
        font-weight: bold;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        margin-right: 5px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #1a1a1a !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #FF6B35;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #6A0DAD;
        padding: 10px 25px;
        font-size: 16px;
    }
    
    .stButton > button:hover {
        background-color: #FFD700;
        color: #1a1a1a;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: white;
        border: 2px solid #FF6B35;
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;
    }
    
    /* Card styling */
    .retro-card {
        background-color: white;
        border: 3px solid #FF6B35;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 5px 5px 0px rgba(106, 13, 173, 0.3);
    }
    
    /* Metric styling */
    .metric-card {
        background: linear-gradient(135deg, #FF6B35 0%, #FFD700 100%);
        color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 10px;
        border: 2px solid #6A0DAD;
    }
    
    .retro-subheader {
        color: #FF6B35;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 2px 2px 0px #FFD700;
        margin: 20px 0 10px 0;
    }
    
    /* Success message */
    .success-msg {
        background-color: #90EE90;
        border-left: 5px solid #006400;
        padding: 15px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# GLOBAL CONSTANTS
INVENTORY_FILE = "inventory.txt"
SALES_HISTORY_FILE = "sales_history.txt"
RECEIPT_FILE = "receipt.txt"
DEFAULT_SIZE = 9
DEFAULT_PRICE = 160.00
BRANDS = ("Nike", "Adidas", "Puma", "New Balance", "Brooks")


def load_sales_history():
    """Load and parse sales history from file."""
    if not os.path.exists(SALES_HISTORY_FILE):
        return []
    
    sales = []
    with open(SALES_HISTORY_FILE, "r") as file:
        content = file.read()
        records = content.split("-----------------------------")
        
        for record in records:
            if "Salesperson:" in record:
                lines = record.strip().split("\n")
                sale_dict = {}
                for line in lines:
                    if ": " in line:
                        key, value = line.split(": ", 1)
                        key = key.strip().replace("[", "").replace("]", "")
                        value = value.strip()
                        if key == "SALE RECORD" or key == "":
                            continue
                        sale_dict[key] = value
                
                if sale_dict:
                    sales.append(sale_dict)
    
    return sales


def record_sale(salesperson, sale_data):
    """Record sale to files."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Record to sales history
    with open(SALES_HISTORY_FILE, "a") as file:
        file.write(f"\n[{current_time}] SALE RECORD\n")
        file.write(f"Salesperson: {salesperson}\n")
        file.write(f"Brand: {sale_data.brand}\n")
        file.write(f"Model: {sale_data.model}\n")
        file.write(f"Size: {sale_data.size}\n")
        file.write(f"Price: {sale_data.price}\n")
        file.write("-----------------------------\n")
    
    # Generate receipt file
    with open(RECEIPT_FILE, "w") as file:
        file.write("====================================\n")
        file.write("        SHOE STORE RECEIPT\n")
        file.write("====================================\n")
        file.write(f"Salesperson: {salesperson.upper()}\n")
        file.write(f"BRAND: {sale_data.brand.upper()}\n")
        file.write(f"MODEL: {sale_data.model.upper()}\n")
        file.write(f"SIZE: {sale_data.size}\n")
        file.write(f"PRICE: ${sale_data.price:.2f}\n")
        file.write("------------------------------------\n")
        file.write(f"TIME: {current_time}\n")
        file.write("STATUS: SALE RECORDED\n")
        file.write("====================================\n")


def get_sales_dataframe():
    """Convert sales history to pandas DataFrame."""
    sales = load_sales_history()
    if not sales:
        return pd.DataFrame()
    
    df_data = []
    for sale in sales:
        try:
            df_data.append({
                'Timestamp': sale.get('', ''),
                'Salesperson': sale.get('Salesperson', 'N/A'),
                'Brand': sale.get('Brand', 'N/A'),
                'Model': sale.get('Model', 'N/A'),
                'Size': sale.get('Size', 'N/A'),
                'Price': float(sale.get('Price', 0))
            })
        except:
            continue
    
    return pd.DataFrame(df_data)


# MAIN HEADER
st.markdown('<div class="retro-header">🏃 RETRO SPORTS STORE 🏃<br>SHOE SALES TRACKER</div>', unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown("### 🎮 CONTROL CENTER")
st.sidebar.markdown("---")

# CREATE TABS
tab1, tab2, tab3 = st.tabs(["📝 NEW SALE", "📊 HISTORY", "📈 DASHBOARD"])

# ==================== TAB 1: NEW SALE ====================
with tab1:
    st.markdown('<div class="retro-subheader">CREATE NEW SALE</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 SALESPERSON INFO**")
        salesperson = st.text_input("Sales Team Member Name:", placeholder="Enter name")
    
    with col2:
        st.markdown("**🥾 SHOE DETAILS**")
        brand = st.selectbox("Shoe Brand:", BRANDS)
    
    col3, col4 = st.columns(2)
    with col3:
        model = st.text_input("Shoe Model:", placeholder="e.g., Air Force 1")
    
    with col4:
        size = st.number_input("Shoe Size:", min_value=1, max_value=20, value=DEFAULT_SIZE)
    
    col5, col6 = st.columns(2)
    with col5:
        price = st.number_input("Price ($):", min_value=0.0, value=DEFAULT_PRICE, step=0.01)
    
    with col6:
        st.markdown("")  # Spacing
        st.markdown("")
    
    # PREVIEW SECTION
    st.markdown("---")
    st.markdown('<div class="retro-subheader">SALE PREVIEW</div>', unsafe_allow_html=True)
    
    if salesperson and brand and model:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("**SALESPERSON**")
            st.write(salesperson.upper())
        
        with col2:
            st.markdown("**BRAND**")
            st.write(brand.upper())
        
        with col3:
            st.markdown("**MODEL**")
            st.write(model.upper())
        
        with col4:
            st.markdown("**SIZE**")
            st.write(size)
        
        with col5:
            st.markdown("**PRICE**")
            st.write(f"${price:.2f}")
        
        st.markdown("---")
        
        col_confirm, col_cancel = st.columns(2)
        
        with col_confirm:
            if st.button("✅ CONFIRM & RECORD SALE", use_container_width=True):
                # Create ShoeOrder object
                sale_data = ShoeOrder(
                    salesperson=salesperson,
                    brand=brand,
                    model=model,
                    size=int(size),
                    price=float(price)
                )
                
                # Record the sale
                record_sale(salesperson, sale_data)
                
                st.success("🎉 SALE SUCCESSFULLY RECORDED!", icon="✅")
                st.balloons()
                
                # Display receipt
                st.markdown('<div class="retro-card">', unsafe_allow_html=True)
                st.markdown("### 📄 RECEIPT")
                st.markdown(f"""
                **SALESPERSON:** {salesperson.upper()}  
                **BRAND:** {brand.upper()}  
                **MODEL:** {model.upper()}  
                **SIZE:** {size}  
                **PRICE:** ${price:.2f}  
                **TIME:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
                **STATUS:** SALE RECORDED ✓
                """)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col_cancel:
            if st.button("❌ CANCEL", use_container_width=True):
                st.warning("Sale cancelled.")
    
    else:
        st.info("👉 Fill in all fields above to see preview", icon="ℹ️")


# ==================== TAB 2: SALES HISTORY ====================
with tab2:
    st.markdown('<div class="retro-subheader">SALES HISTORY</div>', unsafe_allow_html=True)
    
    sales = load_sales_history()
    
    if sales:
        df = get_sales_dataframe()
        
        if not df.empty:
            # Remove timestamp column for display
            display_df = df.drop('Timestamp', axis=1, errors='ignore')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Filter options
            st.markdown("**🔍 FILTER OPTIONS**")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_brand = st.selectbox("Filter by Brand:", ["All"] + [b for b in df['Brand'].unique()])
            
            with col2:
                selected_salesperson = st.selectbox("Filter by Salesperson:", ["All"] + [s for s in df['Salesperson'].unique()])
            
            # Apply filters
            filtered_df = df.copy()
            if selected_brand != "All":
                filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
            if selected_salesperson != "All":
                filtered_df = filtered_df[filtered_df['Salesperson'] == selected_salesperson]
            
            if not filtered_df.empty:
                st.markdown("**Filtered Results:**")
                st.dataframe(filtered_df.drop('Timestamp', axis=1, errors='ignore'), use_container_width=True, hide_index=True)
            else:
                st.warning("No records match your filters.")
        else:
            st.warning("⚠️ No sales data found.")
    else:
        st.info("📭 No sales recorded yet. Start by creating a new sale!", icon="ℹ️")


# ==================== TAB 3: DASHBOARD ====================
with tab3:
    st.markdown('<div class="retro-subheader">SALES DASHBOARD</div>', unsafe_allow_html=True)
    
    df = get_sales_dataframe()
    
    if not df.empty:
        # STATISTICS ROW 1
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📊 Total Sales", len(df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("💰 Total Revenue", f"${df['Price'].sum():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📈 Avg Price", f"${df['Price'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("👥 Salespersons", df['Salesperson'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # CHARTS ROW
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Sales by Brand**")
            brand_sales = df['Brand'].value_counts()
            st.bar_chart(brand_sales)
        
        with col2:
            st.markdown("**Revenue by Salesperson**")
            sales_by_person = df.groupby('Salesperson')['Price'].sum().sort_values(ascending=False)
            st.bar_chart(sales_by_person)
        
        st.markdown("---")
        
        # TOP PERFORMERS
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏆 TOP BRAND**")
            top_brand = df['Brand'].value_counts().index[0]
            top_brand_count = df['Brand'].value_counts().values[0]
            st.markdown(f"### {top_brand}\n*{top_brand_count} sales*")
        
        with col2:
            st.markdown("**🏆 TOP SALESPERSON**")
            top_person = df['Salesperson'].value_counts().index[0]
            top_person_count = df['Salesperson'].value_counts().values[0]
            st.markdown(f"### {top_person}\n*{top_person_count} sales*")
        
        with col3:
            st.markdown("**🏆 HIGHEST SALE**")
            highest_price = df['Price'].max()
            highest_item = df[df['Price'] == highest_price].iloc[0]
            st.markdown(f"### ${highest_price:.2f}\n*{highest_item['Brand']} {highest_item['Model']}*")
        
        st.markdown("---")
        
        # SIZE DISTRIBUTION
        st.markdown("**Shoe Sizes Sold**")
        size_dist = df['Size'].value_counts().sort_index()
        st.bar_chart(size_dist)
    
    else:
        st.info("📭 No sales data yet. Record some sales to see dashboard analytics!", icon="ℹ️")


# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #FF6B35; font-weight: bold; margin-top: 30px;">
    🏃 RETRO SPORTS STORE | Shoe Sales Tracker 🏃<br>
    <small>Sprint 4 - Streamlit Edition</small>
</div>
""", unsafe_allow_html=True)
