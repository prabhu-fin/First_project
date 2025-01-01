import streamlit as st
from backend_code_v2 import calculate_limits_v2

# Streamlit app
st.title("Finance Calculator with Enhanced Layout and Facility Margins")

# Define styles for the boxes
BOX_STYLE = """
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #d9e1f2;
    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
"""

# Basic Sales/Purchase Details section with outer box
with st.expander("Basic Sales/Purchase Details", expanded=True):
    st.markdown(f"<div style='{BOX_STYLE}'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        turnover = st.number_input("Annual Turnover (in Rs Crore)", min_value=0.0, step=0.1)
        purchases = st.number_input("Annual Purchases (in Rs Crore)", min_value=0.0, step=0.1)

    with col2:
        has_sales_exports = st.checkbox("Does the company have export sales?")
        has_purchase_imports = st.checkbox("Does the company have import purchases?")
        if has_sales_exports:
            domestic_sales_share = st.slider("Domestic Sales Share (%)", 0, 100, step=1)
        else:
            domestic_sales_share = 100  # 100% domestic sales
        if has_purchase_imports:
            domestic_purchases_share = st.slider("Domestic Purchases Share (%)", 0, 100, step=1)
        else:
            domestic_purchases_share = 100  # 100% domestic purchases

    st.markdown("</div>", unsafe_allow_html=True)

# WC Cycle section with outer box
with st.expander("WC Cycle Details", expanded=True):
    st.markdown(f"<div style='{BOX_STYLE}'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        receivables_domestic = st.number_input("Receivables - Domestic (Days)", min_value=0, step=1)
        payables_domestic = st.number_input("Payables - Domestic (Days)", min_value=0, step=1)
        inventory_days = st.number_input("Inventory/Processing (Days)", min_value=0, step=1)

    with col2:
        receivables_export = st.number_input("Receivables - Export (Days)", min_value=0, step=1) if has_sales_exports else 0
        payables_import = st.number_input("Payables - Import (Days)", min_value=0, step=1) if has_purchase_imports else 0

    st.markdown("</div>", unsafe_allow_html=True)

# Facilities required section with outer box
with st.expander("Facilities Required", expanded=True):
    st.markdown(f"<div style='{BOX_STYLE}'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Purchase/Processing Facilities**")
        facility_cc = st.checkbox("Cash Credit (CC)")
        margin_cc = st.number_input("Margin for CC (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_cc else 0
        facility_lc = st.checkbox("Letter of Credit (LC)")
        margin_lc = st.number_input("Margin for LC (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_lc else 0
        facility_pif = st.checkbox("Purchase Invoice Finance (PIF)")
        margin_pif = st.number_input("Margin for PIF (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_pif else 0
        facility_pre_shipment = st.checkbox("Pre-shipment Credit") if has_sales_exports else False
        margin_pre_shipment = st.number_input("Margin for Pre-shipment Credit (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_pre_shipment else 0

    with col2:
        st.write("**Sales Finance Facilities**")
        facility_post_shipment = st.checkbox("Post-shipment Finance") if has_sales_exports else False
        margin_post_shipment = st.number_input("Margin for Post-shipment Finance (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_post_shipment else 0
        facility_ebd = st.checkbox("Export Bill Discounting (EBD)") if has_sales_exports else False
        margin_ebd = st.number_input("Margin for EBD (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_ebd else 0
        facility_sif = st.checkbox("Sales Invoice Finance (SIF)")
        margin_sif = st.number_input("Margin for SIF (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_sif else 0
        facility_sbd = st.checkbox("Sales Bill Discounting (SBD)")
        margin_sbd = st.number_input("Margin for SBD (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_sbd else 0

    st.markdown("</div>", unsafe_allow_html=True)

# Margin inputs
margin_cash_credit = st.number_input("Margin for Cash Credit (%)", min_value=0.0, max_value=100.0, step=0.1)

# Prepare input data
input_data_v2 = {
    'turnover': turnover,
    'purchases': purchases,
    'domestic_sales_share': domestic_sales_share / 100,  # Convert to decimal
    'domestic_purchases_share': domestic_purchases_share / 100,  # Convert to decimal
    'receivables_domestic': receivables_domestic,
    'receivables_export': receivables_export,
    'payables_domestic': payables_domestic,
    'payables_import': payables_import,
    'inventory_days': inventory_days,
    'facilities': {
        'cc': {'enabled': facility_cc, 'margin': margin_cc / 100},
        'lc': {'enabled': facility_lc, 'margin': margin_lc / 100},
        'pif': {'enabled': facility_pif, 'margin': margin_pif / 100},
        'pre_shipment': {'enabled': facility_pre_shipment, 'margin': margin_pre_shipment / 100},
        'post_shipment': {'enabled': facility_post_shipment, 'margin': margin_post_shipment / 100},
        'ebd': {'enabled': facility_ebd, 'margin': margin_ebd / 100},
        'sif': {'enabled': facility_sif, 'margin': margin_sif / 100},
        'sbd': {'enabled': facility_sbd, 'margin': margin_sbd / 100},
    },
}

# Calculate and display results
if st.button("Calculate"):
    results_v2 = calculate_limits_v2(input_data_v2)

    st.write("### Results")
    for facility, value in results_v2.items():
        if value > 0:  # Show only facilities with non-zero limits
            st.write(f"{facility.upper()} Limit: {value:.1f} crore")  # Format with a single decimal

