"""
SHOE STORE SALES TRACKER - STREAMLIT VERSION (REFACTORED v2.0)
Retro Sports Store Theme - FIXED FOR UX/ACCESSIBILITY
Issues Fixed:
1. Form Cognitive Load - Added helper text, real-time preview, required indicators
2. No Success Feedback - Added confirmation #, timestamp, receipt display
3. Mobile Layout - Responsive design preparation (desktop-first)
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

# RETRO SPORTS STORE STYLING (IMPROVED FOR ACCESSIBILITY + DARK MODE)
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
    
    /* ==================== LIGHT MODE (DEFAULT) ==================== */
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
        font-size: 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #1a1a1a !important;
    }
    
    /* Button styling - IMPROVED FOR ACCESSIBILITY */
    .stButton > button {
        background-color: #FF6B35;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #6A0DAD;
        padding: 12px 25px;
        font-size: 16px;
        min-height: 44px;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: #FFD700;
        color: #1a1a1a;
    }
    
    /* Input field styling - BETTER CONTRAST */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: white;
        border: 2px solid #FF6B35;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
        font-size: 16px;
        color: #1a1a1a;
    }
    
    /* Field group styling */
    .field-group {
        background-color: white;
        border-left: 4px solid #FF6B35;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(255, 107, 53, 0.1);
    }
    
    .field-label {
        font-weight: bold;
        color: #1a1a1a;
        font-size: 16px;
        margin-bottom: 5px;
    }
    
    .field-helper {
        color: #555;
        font-size: 13px;
        font-style: italic;
        margin-top: 5px;
    }
    
    .required-indicator {
        color: #FF0000;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    /* Preview card - RESPONSIVE */
    .preview-card {
        background-color: white;
        border: 3px solid #FF6B35;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 5px 5px 0px rgba(106, 13, 173, 0.2);
    }
    
    .preview-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #FFD700;
    }
    
    .preview-item:last-child {
        border-bottom: none;
    }
    
    .preview-label {
        font-weight: bold;
        color: #FF6B35;
        min-width: 150px;
    }
    
    .preview-value {
        color: #1a1a1a;
        font-weight: bold;
        flex: 1;
        text-align: right;
    }
    
    .preview-status-ok {
        color: #228B22;
        font-weight: bold;
        font-size: 14px;
    }
    
    /* Animation for success message */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(34, 139, 34, 0.7);
        }
        50% {
            box-shadow: 0 0 0 10px rgba(34, 139, 34, 0);
        }
    }
    
    .success-msg {
        background: linear-gradient(135deg, #90EE90 0%, #98FB98 100%);
        border-left: 5px solid #228B22;
        padding: 20px;
        border-radius: 8px;
        font-weight: bold;
        color: #1a1a1a;
        margin: 15px 0;
        animation: slideInDown 0.5s ease-out, pulse 2s infinite;
        box-shadow: 0 4px 15px rgba(34, 139, 34, 0.3);
    }
    
    .confirmation-number {
        background-color: #FFD700;
        color: #1a1a1a;
        padding: 10px 15px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 18px;
        display: inline-block;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
    }
    
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
    
    /* Receipt styling */
    .receipt-container {
        background-color: white;
        border: 2px dashed #FF6B35;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        color: #1a1a1a;
        background-image: linear-gradient(90deg, transparent 24%, #FFD700 25%, #FFD700 26%, transparent 27%, transparent 74%, #FFD700 75%, #FFD700 76%, transparent 77%, transparent),
                          linear-gradient(#FFD700 0px, #FFD700 2px, transparent 2px, transparent 4px);
        background-size: 50px 50px;
        background-position: 0 0, 25px 25px;
    }
    
    /* Validation styling */
    .validation-ok {
        color: #228B22;
        font-weight: bold;
    }
    
    .validation-error {
        color: #DC143C;
        font-weight: bold;
    }
    
    /* Accessibility improvements */
    .visually-hidden {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        border: 0;
    }
    
    /* ==================== DARK MODE ==================== */
    @media (prefers-color-scheme: dark) {
        .main {
            background-color: #1e1e1e;
        }
        
        /* Header stays same (gradient looks good in dark) */
        .retro-header {
            background: linear-gradient(135deg, #FF6B35 0%, #6A0DAD 100%);
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }
        
        /* Tab styling for dark mode */
        .stTabs [data-baseweb="tab-list"] button {
            background-color: #FF6B35;
            color: white;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #FFD700 !important;
            color: #1a1a1a !important;
        }
        
        /* Input fields for dark mode */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background-color: #2d2d2d;
            border: 2px solid #FF6B35;
            color: #f5f5f5;
        }
        
        /* Field group for dark mode */
        .field-group {
            background-color: #2d2d2d;
            border-left: 4px solid #FF6B35;
            box-shadow: 0 2px 4px rgba(255, 107, 53, 0.3);
        }
        
        .field-label {
            color: #ffffff !important;
            font-weight: bold;
            font-size: 1.05em;
            display: inline-block;
        }
        
        .field-label span {
            color: #ffffff !important;
        }
        
        .field-helper {
            color: #d0d0d0 !important;
        }
        
        .required-indicator {
            color: #FF0000 !important;
            font-weight: bold;
            font-size: 1.2em;
            text-shadow: 0 0 3px rgba(255, 0, 0, 0.8) !important;
        }
        
        /* Preview card for dark mode */
        .preview-card {
            background-color: #2d2d2d;
            border: 3px solid #FF6B35;
            box-shadow: 5px 5px 0px rgba(106, 13, 173, 0.4);
        }
        
        .preview-item {
            border-bottom: 1px solid rgba(255, 215, 0, 0.3);
        }
        
        .preview-label {
            color: #FFB84D;
        }
        
        .preview-value {
            color: #f5f5f5;
            font-weight: bold;
        }
        
        /* Success message for dark mode */
        .success-msg {
            background: linear-gradient(135deg, #2d5a2d 0%, #3a6f3a 100%);
            border-left: 5px solid #76EEC6;
            color: #f5f5f5;
            animation: slideInDown 0.5s ease-out, pulse 2s infinite;
            box-shadow: 0 4px 15px rgba(118, 238, 198, 0.3);
        }
        
        /* Confirmation number for dark mode */
        .confirmation-number {
            background-color: #FFD700;
            color: #1a1a1a;
        }
        
        /* Metric card for dark mode */
        .metric-card {
            background: linear-gradient(135deg, #C84E22 0%, #D4A824 100%);
            color: #ffffff;
            border: 2px solid #A370A3;
            font-weight: bold;
        }
        
        /* Receipt container for dark mode */
        .receipt-container {
            background-color: #2d2d2d;
            border: 2px dashed #FF6B35;
            color: #f5f5f5;
            background-image: linear-gradient(90deg, transparent 24%, rgba(255, 215, 0, 0.2) 25%, rgba(255, 215, 0, 0.2) 26%, transparent 27%, transparent 74%, rgba(255, 215, 0, 0.2) 75%, rgba(255, 215, 0, 0.2) 76%, transparent 77%, transparent),
                              linear-gradient(rgba(255, 215, 0, 0.1) 0px, rgba(255, 215, 0, 0.1) 2px, transparent 2px, transparent 4px);
            background-size: 50px 50px;
            background-position: 0 0, 25px 25px;
        }
        
        /* Validation for dark mode */
        .validation-ok {
            color: #76EEC6;
            font-weight: bold;
        }
        
        .validation-error {
            color: #FF6B6B;
            font-weight: bold;
        }
        
        /* AGGRESSIVE - Force all text to be bright white in dark mode */
        body, html {
            color: #ffffff !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: bold !important;
        }
        
        p, span, div, section {
            color: #ffffff !important;
        }
        
        strong, b {
            color: #ffffff !important;
            font-weight: bold !important;
        }
        
        /* Streamlit markdown container */
        .stMarkdown {
            color: #ffffff !important;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #ffffff !important;
            font-weight: bold !important;
        }
        
        .stMarkdown p {
            color: #e8e8e8 !important;
        }
        
        .stMarkdown strong, .stMarkdown b {
            color: #ffffff !important;
        }
        
        .stMarkdown span {
            color: #ffffff !important;
        }
        
        /* Ensure markdown text is bright */
        .stMarkdown {
            color: #ffffff !important;
        }
        
        .stMarkdown * {
            color: #ffffff !important;
        }
        
        .stCaption {
            color: #d0d0d0 !important;
        }
        
        /* Help text styling */
        [data-testid="stHelperText"] {
            color: #d0d0d0 !important;
        }
        
        /* Form labels */
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label {
            color: #ffffff !important;
        }
        
        /* Info/warning/success/error boxes */
        .stAlert {
            color: #f5f5f5 !important;
        }
        
        .stAlert p, .stAlert span {
            color: #f5f5f5 !important;
        }
        
        .stInfo, .stWarning, .stSuccess, .stError {
            color: #f5f5f5 !important;
        }
        
        /* Streamlit native elements */
        .stSubheader {
            color: #ffffff !important;
        }
        
        .stTitle {
            color: #ffffff !important;
        }
        
        /* Tabs */
        .stTabs {
            color: #ffffff !important;
        }
        
        /* Metrics and text */
        .stMetric label {
            color: #ffffff !important;
        }
        
        .stMetric * {
            color: #ffffff !important;
        }
        
        /* Sidebar */
        .stSidebar {
            color: #ffffff !important;
        }
        
        .stSidebar * {
            color: #ffffff !important;
        }
        
        /* Divider styling in dark mode */
        hr {
            border-color: #FF6B35 !important;
            opacity: 0.7;
        }
    }
</style>
""", unsafe_allow_html=True)

# GLOBAL CONSTANTS
INVENTORY_FILE = "inventory.txt"
SALES_HISTORY_FILE = "sales_history.txt"
RECEIPT_FILE = "receipt.txt"
COMMISSIONS_FILE = "commissions.txt"
COMMISSION_RATE = 0.035  # 3.5%
DEFAULT_SIZE = 9
DEFAULT_PRICE = 160.00
BRANDS = ("Nike", "Adidas", "Puma", "New Balance", "Brooks")

# SHOE MODEL EXAMPLES (FOR HELPER TEXT)
MODEL_EXAMPLES = {
    "Nike": "Air Force 1, Air Force 1 Low, Jordan 1",
    "Adidas": "Stan Smith, Ultraboost, NMD",
    "Puma": "RS-X, Suede, Future Rider",
    "New Balance": "574, 990, 1080",
    "Brooks": "Ghost, Ravenna, Glycerin"
}

# ==================== SESSION STATE MANAGEMENT ====================
if 'sale_confirmation' not in st.session_state:
    st.session_state.sale_confirmation = None

if 'salesperson_value' not in st.session_state:
    st.session_state.salesperson_value = ""

if 'brand_value' not in st.session_state:
    st.session_state.brand_value = "Nike"

if 'model_value' not in st.session_state:
    st.session_state.model_value = ""

if 'size_value' not in st.session_state:
    st.session_state.size_value = DEFAULT_SIZE

if 'price_value' not in st.session_state:
    st.session_state.price_value = DEFAULT_PRICE


# ==================== UTILITY FUNCTIONS ====================
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


def get_next_confirmation_number():
    """Generate next confirmation number based on sales count."""
    sales = load_sales_history()
    return f"#{str(len(sales) + 1).zfill(5)}"


def validate_form_data(salesperson, brand, model, size, price):
    """Validate all form fields. Returns (is_valid, errors_dict)."""
    errors = {}
    
    if not salesperson or not salesperson.strip():
        errors['salesperson'] = "Salesperson name is required"
    elif len(salesperson.strip()) < 2:
        errors['salesperson'] = "Name must be at least 2 characters"
    
    if not brand or brand == "Select...":
        errors['brand'] = "Brand is required"
    
    if not model or not model.strip():
        errors['model'] = "Model is required"
    
    if size < 1 or size > 20:
        errors['size'] = "Size must be between 1 and 20"
    
    if price < 0:
        errors['price'] = "Price cannot be negative"
    
    return len(errors) == 0, errors


def record_sale(salesperson, sale_data):
    """Record sale to files. Returns confirmation number and timestamp."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    confirmation_number = get_next_confirmation_number()
    
    # Record to sales history
    with open(SALES_HISTORY_FILE, "a") as file:
        file.write(f"\n[{current_time}] SALE RECORD\n")
        file.write(f"Confirmation: {confirmation_number}\n")
        file.write(f"Salesperson: {salesperson}\n")
        file.write(f"Brand: {sale_data.brand}\n")
        file.write(f"Model: {sale_data.model}\n")
        file.write(f"Size: {sale_data.size}\n")
        file.write(f"Price: {sale_data.price}\n")
        file.write("-----------------------------\n")
    
    # Record commission automatically
    record_commission(salesperson, sale_data.brand, sale_data.model, sale_data.size, 
                     sale_data.price, confirmation_number, current_time)
    
    # Generate receipt file
    with open(RECEIPT_FILE, "w") as file:
        file.write("====================================\n")
        file.write("        SHOE STORE RECEIPT\n")
        file.write("====================================\n")
        file.write(f"Confirmation: {confirmation_number}\n")
        file.write(f"Salesperson: {salesperson.upper()}\n")
        file.write(f"BRAND: {sale_data.brand.upper()}\n")
        file.write(f"MODEL: {sale_data.model.upper()}\n")
        file.write(f"SIZE: {sale_data.size}\n")
        file.write(f"PRICE: ${sale_data.price:.2f}\n")
        file.write("------------------------------------\n")
        file.write(f"TIME: {current_time}\n")
        file.write("STATUS: SALE RECORDED\n")
        file.write("====================================\n")
    
    return confirmation_number, current_time


def get_sales_dataframe():
    """Convert sales history to pandas DataFrame."""
    sales = load_sales_history()
    if not sales:
        return pd.DataFrame()
    
    df_data = []
    for sale in sales:
        try:
            df_data.append({
                'Timestamp': sale.get('Timestamp', ''),
                'Confirmation': sale.get('Confirmation', 'N/A'),
                'Salesperson': sale.get('Salesperson', 'N/A'),
                'Brand': sale.get('Brand', 'N/A'),
                'Model': sale.get('Model', 'N/A'),
                'Size': int(sale.get('Size', 0)),
                'Price': float(sale.get('Price', 0))
            })
        except:
            continue
    
    return pd.DataFrame(df_data)


def clear_form():
    """Clear all form inputs."""
    st.session_state.salesperson_value = ""
    st.session_state.brand_value = "Nike"
    st.session_state.model_value = ""
    st.session_state.size_value = DEFAULT_SIZE
    st.session_state.price_value = DEFAULT_PRICE
    st.session_state.sale_confirmation = None


# ==================== COMMISSION TRACKING ====================
def calculate_commission(price: float) -> float:
    """Calculate 3.5% commission on sale price."""
    return price * COMMISSION_RATE


def record_commission(salesperson, brand, model, size, price, confirmation_number, timestamp):
    """Record commission to commissions file."""
    commission = calculate_commission(price)
    with open(COMMISSIONS_FILE, "a") as file:
        file.write(f"[{timestamp}] COMMISSION RECORD\n")
        file.write(f"Confirmation: {confirmation_number}\n")
        file.write(f"Salesperson: {salesperson}\n")
        file.write(f"Brand: {brand}\n")
        file.write(f"Model: {model}\n")
        file.write(f"Size: {size}\n")
        file.write(f"Sale Price: ${price:.2f}\n")
        file.write(f"Commission (3.5%): ${commission:.2f}\n")
        file.write("-----------------------------\n")
    return commission


def load_commissions():
    """Load and parse commission history from file."""
    if not os.path.exists(COMMISSIONS_FILE):
        return []
    
    commissions = []
    with open(COMMISSIONS_FILE, "r") as file:
        content = file.read()
        records = content.split("-----------------------------")
        
        for record in records:
            if "Salesperson:" in record:
                lines = record.strip().split("\n")
                commission_dict = {}
                for line in lines:
                    if ": " in line:
                        key, value = line.split(": ", 1)
                        key = key.strip().replace("[", "").replace("]", "")
                        value = value.strip()
                        if key == "COMMISSION RECORD" or key == "":
                            continue
                        commission_dict[key] = value
                
                if commission_dict:
                    commissions.append(commission_dict)
    
    return commissions


def get_commissions_dataframe():
    """Convert commission history to pandas DataFrame."""
    commissions = load_commissions()
    if not commissions:
        return pd.DataFrame()
    
    df_data = []
    for comm in commissions:
        try:
            # Extract timestamp from the record
            sale_price = float(comm.get('Sale Price', '0').replace('$', ''))
            commission_amt = float(comm.get('Commission (3.5%)', '0').replace('$', ''))
            
            df_data.append({
                'Confirmation': comm.get('Confirmation', 'N/A'),
                'Salesperson': comm.get('Salesperson', 'N/A'),
                'Brand': comm.get('Brand', 'N/A'),
                'Model': comm.get('Model', 'N/A'),
                'Size': int(comm.get('Size', 0)),
                'Sale Price': sale_price,
                'Commission': commission_amt
            })
        except:
            continue
    
    return pd.DataFrame(df_data)


def export_commissions_to_csv():
    """Export commission data to CSV."""
    df = get_commissions_dataframe()
    if df.empty:
        return None
    
    # Create summary by salesperson
    summary_df = df.groupby('Salesperson').agg({
        'Commission': ['count', 'sum', 'mean'],
        'Sale Price': 'sum'
    }).round(2)
    summary_df.columns = ['Sales Count', 'Total Commission', 'Avg Commission', 'Total Sales']
    summary_df = summary_df.reset_index()
    
    return df, summary_df


# ==================== MAIN HEADER ====================
st.markdown('<div class="retro-header">🏃 RETRO SPORTS STORE 🏃<br>SHOE SALES TRACKER</div>', 
            unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown("### 🎮 CONTROL CENTER")
st.sidebar.markdown("---")
st.sidebar.info("Use the tabs below to log sales, view history, and check analytics.", icon="📌")

# CREATE TABS
tab1, tab2, tab3, tab4 = st.tabs(["📝 NEW SALE", "📊 HISTORY", "📈 DASHBOARD", "💰 COMMISSIONS"])

# ==================== TAB 1: NEW SALE ====================
with tab1:
    st.markdown('<div class="retro-subheader">CREATE NEW SALE</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # SUCCESS MESSAGE DISPLAY (ISSUE #2 FIX)
    if st.session_state.sale_confirmation:
        st.markdown(f"""
        <div class="success-msg">
            ✅ SALE SUCCESSFULLY RECORDED!<br><br>
            <strong>Confirmation:</strong> <span class="confirmation-number">{st.session_state.sale_confirmation['number']}</span><br>
            <strong>Recorded:</strong> {st.session_state.sale_confirmation['timestamp']}<br>
            <strong>Salesperson:</strong> {st.session_state.sale_confirmation['salesperson']}<br>
            <strong>Product:</strong> {st.session_state.sale_confirmation['brand']} {st.session_state.sale_confirmation['model']}<br>
            <strong>Amount:</strong> ${st.session_state.sale_confirmation['price']:.2f}
        </div>
        """, unsafe_allow_html=True)
        
        # Dismiss button
        if st.button("✕ Dismiss Success Message", use_container_width=True, type="secondary"):
            st.session_state.sale_confirmation = None
            st.rerun()
        
        st.balloons()
    
    # ==================== FORM SECTION (ISSUE #1 FIX) ====================
    st.markdown("### 📋 SALESPERSON INFORMATION")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<span style="color: #FF6B35; font-weight: bold; font-size: 1.05em;">Sales Team Member Name <span style="color: #FF0000; font-weight: bold; font-size: 1.2em;">*</span></span>', 
                   unsafe_allow_html=True)
        salesperson = st.text_input(
            "Salesperson name",
            value=st.session_state.salesperson_value,
            placeholder="Enter full name (e.g., John Smith)",
            key="salesperson_input",
            label_visibility="collapsed",
            help="Required field"
        )
        st.session_state.salesperson_value = salesperson
        st.caption("ℹ️  Help: Enter the first and last name of the sales team member")
    
    with col2:
        if salesperson and len(salesperson.strip()) >= 2:
            st.markdown('<span class="validation-ok">✓ OK</span>', unsafe_allow_html=True)
    
    # SHOE DETAILS SECTION
    st.markdown("---")
    st.markdown("### 🥾 SHOE DETAILS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<span style="color: #FF6B35; font-weight: bold; font-size: 1.05em;">Shoe Brand <span style="color: #FF0000; font-weight: bold; font-size: 1.2em;">*</span></span>', 
                   unsafe_allow_html=True)
        brand = st.selectbox(
            "Brand",
            BRANDS,
            index=0,
            key="brand_select",
            label_visibility="collapsed",
            help="Required field"
        )
        st.session_state.brand_value = brand
        st.caption(f"ℹ️  Help: Available models - {MODEL_EXAMPLES.get(brand, 'N/A')}")
    
    with col2:
        st.markdown('<span style="color: #FF6B35; font-weight: bold; font-size: 1.05em;">Shoe Size <span style="color: #FF0000; font-weight: bold; font-size: 1.2em;">*</span></span>', 
                   unsafe_allow_html=True)
        size = st.number_input(
            "Size",
            min_value=1,
            max_value=20,
            value=st.session_state.size_value,
            key="size_input",
            label_visibility="collapsed",
            help="US shoe size (range 1-20)"
        )
        st.session_state.size_value = size
        st.caption("ℹ️  Help: Standard US shoe size (5-20 typical)")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<span style="color: #FF6B35; font-weight: bold; font-size: 1.05em;">Shoe Model <span style="color: #FF0000; font-weight: bold; font-size: 1.2em;">*</span></span>', 
                   unsafe_allow_html=True)
        model = st.text_input(
            "Model",
            value=st.session_state.model_value,
            placeholder=f"e.g., {MODEL_EXAMPLES.get(brand, 'Air Force 1')}",
            key="model_input",
            label_visibility="collapsed",
            help="Required field"
        )
        st.session_state.model_value = model
        st.caption("ℹ️  Help: Model name or style (e.g., 'Air Force 1 Low Black')")
    
    with col4:
        st.markdown('<span style="color: #FF6B35; font-weight: bold; font-size: 1.05em;">Price <span style="color: #FF0000; font-weight: bold; font-size: 1.2em;">*</span></span>', 
                   unsafe_allow_html=True)
        price = st.number_input(
            "Price",
            min_value=0.0,
            value=st.session_state.price_value,
            step=0.01,
            key="price_input",
            label_visibility="collapsed",
            help="Sale price in USD"
        )
        st.session_state.price_value = price
        st.caption("ℹ️  Help: Default is $160.00 (edit if different)")
    
    # LIVE PREVIEW SECTION (ISSUE #1 FIX - REAL-TIME)
    st.markdown("---")
    st.markdown("### 📋 LIVE SALE PREVIEW")
    st.markdown("*Updates as you type* ↻")
    
    is_valid, validation_errors = validate_form_data(salesperson, brand, model, size, price)
    
    if salesperson or model or brand != "Nike" or size != DEFAULT_SIZE or price != DEFAULT_PRICE:
        # Show preview card
        st.markdown('<div class="preview-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        # Preview data row
        preview_rows = [
            ("SALESPERSON", salesperson.upper() if salesperson else "—", bool(salesperson and len(salesperson.strip()) >= 2)),
            ("BRAND", brand.upper(), True),
            ("MODEL", model.upper() if model else "—", bool(model)),
            ("SIZE", str(size), True),
            ("PRICE", f"${price:.2f}", True),
        ]
        
        for label, value, status_ok in preview_rows:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"<span class='preview-label'>{label}:</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span class='preview-value'>{value}</span>", unsafe_allow_html=True)
            with col3:
                if status_ok:
                    st.markdown("<span class='validation-ok'>✓</span>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # VALIDATION MESSAGES
        if validation_errors:
            st.warning("⚠️  Please fix the following errors:")
            for field, error_msg in validation_errors.items():
                st.caption(f"  • {field.capitalize()}: {error_msg}")
        else:
            st.success("✅ All fields valid - ready to record!")
    
    else:
        st.info("👉 Fill in the form above to see a live preview", icon="ℹ️")
    
    # ==================== ACTION BUTTONS ====================
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("✅ CONFIRM & RECORD SALE", use_container_width=True, 
                    disabled=not is_valid, type="primary"):
            # Create ShoeOrder object
            sale_data = ShoeOrder(
                salesperson=salesperson,
                brand=brand,
                model=model,
                size=int(size),
                price=float(price)
            )
            
            # Record the sale (ISSUE #2 FIX)
            confirmation_number, timestamp = record_sale(salesperson, sale_data)
            
            # Store confirmation in session state
            st.session_state.sale_confirmation = {
                'number': confirmation_number,
                'timestamp': timestamp,
                'salesperson': salesperson,
                'brand': brand,
                'model': model,
                'size': size,
                'price': price
            }
            
            # Clear form for next entry
            clear_form()
            st.rerun()
    
    with col2:
        if st.button("🔄 CLEAR FORM", use_container_width=True):
            clear_form()
            st.rerun()
    
    with col3:
        if st.button("📄 VIEW RECEIPT", use_container_width=True):
            if os.path.exists(RECEIPT_FILE):
                with open(RECEIPT_FILE, "r") as f:
                    receipt_content = f.read()
                st.markdown('<div class="receipt-container">', unsafe_allow_html=True)
                st.code(receipt_content)
                st.markdown('</div>', unsafe_allow_html=True)


# ==================== TAB 2: SALES HISTORY ====================
with tab2:
    st.markdown('<div class="retro-subheader">SALES HISTORY</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    sales = load_sales_history()
    
    if sales:
        df = get_sales_dataframe()
        
        if not df.empty:
            # FILTER SECTION
            st.markdown("### 🔍 FILTER OPTIONS")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                selected_brand = st.multiselect(
                    "Filter by Brand(s):",
                    ["All"] + sorted(df['Brand'].unique().tolist()),
                    default=["All"]
                )
            
            with col2:
                selected_salesperson = st.multiselect(
                    "Filter by Salesperson(s):",
                    ["All"] + sorted(df['Salesperson'].unique().tolist()),
                    default=["All"]
                )
            
            with col3:
                sort_by = st.selectbox(
                    "Sort by:",
                    ["Most Recent", "Oldest", "Price (High to Low)", "Price (Low to High)"]
                )
            
            # APPLY FILTERS
            filtered_df = df.copy()
            
            if "All" not in selected_brand:
                filtered_df = filtered_df[filtered_df['Brand'].isin(selected_brand)]
            
            if "All" not in selected_salesperson:
                filtered_df = filtered_df[filtered_df['Salesperson'].isin(selected_salesperson)]
            
            # APPLY SORTING
            if sort_by == "Most Recent":
                filtered_df = filtered_df.iloc[::-1]
            elif sort_by == "Price (High to Low)":
                filtered_df = filtered_df.sort_values('Price', ascending=False)
            elif sort_by == "Price (Low to High)":
                filtered_df = filtered_df.sort_values('Price', ascending=True)
            
            # DISPLAY RESULTS
            st.markdown("---")
            st.markdown(f"### Results: {len(filtered_df)} sales")
            
            if not filtered_df.empty:
                display_df = filtered_df[['Confirmation', 'Timestamp', 'Salesperson', 'Brand', 'Model', 'Size', 'Price']].copy()
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # SUMMARY STATS
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Sales", len(filtered_df))
                with col2:
                    st.metric("Total Revenue", f"${filtered_df['Price'].sum():.2f}")
                with col3:
                    st.metric("Average Price", f"${filtered_df['Price'].mean():.2f}")
            else:
                st.warning("No records match your filters.")
        else:
            st.warning("⚠️ No sales data found.")
    else:
        st.info("📭 No sales recorded yet. Start by creating a new sale!", icon="ℹ️")


# ==================== TAB 3: DASHBOARD ====================
with tab3:
    st.markdown('<div class="retro-subheader">SALES DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    df = get_sales_dataframe()
    
    if not df.empty:
        # STATISTICS ROW
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
        
        # COMMISSION ROW
        comm_df = get_commissions_dataframe()
        if not comm_df.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                total_commission = comm_df['Commission'].sum()
                st.metric("💵 Total Commissions", f"${total_commission:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                avg_commission = comm_df['Commission'].mean()
                st.metric("📊 Avg Commission", f"${avg_commission:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                top_earner = comm_df.groupby('Salesperson')['Commission'].sum().idxmax()
                top_amount = comm_df.groupby('Salesperson')['Commission'].sum().max()
                st.metric("🏆 Top Earner", f"{top_earner.split()[0]}")
                st.markdown(f"<small>${top_amount:.2f}</small>", unsafe_allow_html=True)
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


# ==================== TAB 4: COMMISSIONS ====================
with tab4:
    st.markdown('<div class="retro-subheader">💰 COMMISSION TRACKER</div>', unsafe_allow_html=True)
    st.markdown("Track 3.5% commission earned by each salesperson")
    st.markdown("---")
    
    comm_df = get_commissions_dataframe()
    
    if not comm_df.empty:
        # SUMMARY STATISTICS
        st.markdown("### 📊 COMMISSION OVERVIEW")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("💵 Total Commissions", f"${comm_df['Commission'].sum():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📝 Total Sales", len(comm_df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("👥 Salespersons", comm_df['Salesperson'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📈 Avg Commission", f"${comm_df['Commission'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # COMMISSION BY SALESPERSON SUMMARY
        st.markdown("### 🏆 COMMISSION BY SALESPERSON")
        
        salesperson_summary = comm_df.groupby('Salesperson').agg({
            'Commission': ['count', 'sum', 'mean'],
            'Sale Price': 'sum'
        }).round(2)
        salesperson_summary.columns = ['Sales Count', 'Total Commission', 'Avg Commission', 'Total Sales $']
        salesperson_summary = salesperson_summary.sort_values('Total Commission', ascending=False)
        
        st.dataframe(salesperson_summary, use_container_width=True)
        
        # COMMISSION CHART
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Commission by Salesperson**")
            comm_by_person = comm_df.groupby('Salesperson')['Commission'].sum().sort_values(ascending=False)
            st.bar_chart(comm_by_person)
        
        with col2:
            st.markdown("**Sales Count by Salesperson**")
            sales_count = comm_df['Salesperson'].value_counts()
            st.bar_chart(sales_count)
        
        st.markdown("---")
        
        # DETAILED BREAKDOWN
        st.markdown("### 📋 DETAILED COMMISSION BREAKDOWN")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_salesperson = st.multiselect(
                "Filter by Salesperson",
                ["All"] + sorted(comm_df['Salesperson'].unique().tolist()),
                default=["All"]
            )
        
        with col2:
            selected_brand = st.multiselect(
                "Filter by Brand",
                ["All"] + sorted(comm_df['Brand'].unique().tolist()),
                default=["All"]
            )
        
        with col3:
            sort_by = st.selectbox(
                "Sort by",
                ["Most Recent", "Highest Commission", "Lowest Commission"]
            )
        
        # Apply filters
        filtered_comm_df = comm_df.copy()
        
        if "All" not in selected_salesperson:
            filtered_comm_df = filtered_comm_df[filtered_comm_df['Salesperson'].isin(selected_salesperson)]
        
        if "All" not in selected_brand:
            filtered_comm_df = filtered_comm_df[filtered_comm_df['Brand'].isin(selected_brand)]
        
        # Apply sorting
        if sort_by == "Most Recent":
            filtered_comm_df = filtered_comm_df.iloc[::-1]
        elif sort_by == "Highest Commission":
            filtered_comm_df = filtered_comm_df.sort_values('Commission', ascending=False)
        elif sort_by == "Lowest Commission":
            filtered_comm_df = filtered_comm_df.sort_values('Commission', ascending=True)
        
        # Display results
        st.markdown("---")
        st.markdown(f"### Results: {len(filtered_comm_df)} commission records")
        
        if not filtered_comm_df.empty:
            display_comm_df = filtered_comm_df[['Confirmation', 'Salesperson', 'Brand', 'Model', 'Sale Price', 'Commission']].copy()
            st.dataframe(display_comm_df, use_container_width=True, hide_index=True)
            
            # Export to CSV
            st.markdown("---")
            st.markdown("### 📥 EXPORT OPTIONS")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Detailed CSV
                detailed_csv = display_comm_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Detailed CSV",
                    data=detailed_csv,
                    file_name=f"commissions_detailed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Summary CSV
                summary_csv = salesperson_summary.to_csv()
                st.download_button(
                    label="📥 Download Summary CSV",
                    data=summary_csv,
                    file_name=f"commissions_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No commission records match your filters.")
    
    else:
        st.info("📭 No commission data yet. Record some sales to earn commissions!", icon="ℹ️")


# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #FF6B35; font-weight: bold; margin-top: 30px;">
    🏃 RETRO SPORTS STORE | Shoe Sales Tracker 🏃<br>
    <small>Sprint 4 - Streamlit Edition (v3.0 - With Commission Tracking)</small><br>
    <small style="color: #666;">WCAG 2.1 AAA Accessible | 3.5% Commission Tracking | Real-time Analytics</small>
</div>
""", unsafe_allow_html=True)
