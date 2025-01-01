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
        company_name = st.text_input("Company Name")  # Added Company Name
        turnover = st.number_input("Annual Turnover (in Rs Crore)", min_value=0.0, step=0.1)
        purchases = st.number_input("Annual Purchases (in Rs Crore)", min_value=0.0, step=0.1)

    with col2:
        has_sales_exports = st.checkbox("Does the company have export sales?")
        export_sales_share = st.slider("Export Sales Share (%)", 0, 100, step=1) if has_sales_exports else 0
        has_purchase_imports = st.checkbox("Does the company have import purchases?")
        import_purchases_share = st.slider("Import Purchases Share (%)", 0, 100, step=1) if has_purchase_imports else 0

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

    # Purchase/Processing Facilities (LHS)
    with col1:
        st.write("**Purchase/Processing Facilities**")
        
        # Cash Credit (CC)
        facility_cc = st.checkbox("Cash Credit (CC)")
        margin_cc = st.number_input("Margin for CC (%)", min_value=0.0, max_value=100.0, step=0.1) if facility_cc else 0

        # Letter of Credit (LC)
        facility_lc = st.checkbox("Letter of Credit (LC)")
        if facility_lc:
            margin_lc = st.number_input("Margin for LC (%)", min_value=0.0, max_value=100.0, step=0.1)
            share_lc = st.number_input("Share of Purchases via LC (%)", min_value=0.0, max_value=100.0, step=0.1)
            lead_time_lc = st.number_input("Lead Time (days)", min_value=0, step=1)
            usance_time_lc = st.number_input("Usance Time (days)", min_value=0, step=1)

        # Pre Shipment Credit (Only if export sales are enabled)
        if has_sales_exports:
            facility_pre_shipment = st.checkbox("Pre Shipment Credit")
            if facility_pre_shipment:
                margin_pre_shipment = st.number_input("Margin for Pre Shipment Credit (%)", min_value=0.0, max_value=100.0, step=0.1)

        # Purchase Invoice Finance (PIF)
        facility_pif = st.checkbox("Purchase Invoice Finance (PIF)")
        if facility_pif:
            margin_pif = st.number_input("Margin for PIF (%)", min_value=0.0, max_value=100.0, step=0.1)
            share_pif = st.number_input(
                "Share of Purchases to be Financed (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                help="Where Co payables exceed average payables (days)"
            )

    # Sales Finance Facilities (RHS)
    with col2:
        st.write("**Sales Finance Facilities**")

        # Post Shipment Credit (PSC - Only if export sales are enabled)
        if has_sales_exports:
            facility_psc = st.checkbox("Post Shipment Credit")
            if facility_psc:
                margin_psc = st.number_input("Margin for Post Shipment Credit (%)", min_value=0.0, max_value=100.0, step=0.1)

            # Export Bill Negotiation (EBN)
            facility_ebn = st.checkbox("Export Bill Negotiation (EBN)")
            if facility_ebn:
                margin_ebn = st.number_input("Margin for Export Bill Negotiation (%)", min_value=0.0, max_value=100.0, step=0.1)

        # Sales Invoice Finance (SIF)
        facility_sif = st.checkbox("Sales Invoice Finance (SIF)")
        if facility_sif:
            margin_sif = st.number_input("Margin for SIF (%)", min_value=0.0, max_value=100.0, step=0.1)
            share_sif = st.number_input(
                "Share of Sales to be Financed (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                help="Where Co receivables exceed average receivables (days)"
            )

        # Sales Bill Discounting (SBD)
        facility_sbd = st.checkbox("Sales Bill Discounting (SBD)")
        if facility_sbd:
            margin_sbd = st.number_input("Margin for SBD (%)", min_value=0.0, max_value=100.0, step=0.1)
            share_sbd = st.number_input(
                "Share of Sales to be Discounted (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                help="Where Co receivables exceed average receivables (days)"
            )

    st.markdown("</div>", unsafe_allow_html=True)

# Prepare input data
input_data_v2 = {
    'company_name': company_name,  # Added
    'turnover': turnover,
    'purchases': purchases,
    'export_sales_share': export_sales_share / 100,
    'import_purchases_share': import_purchases_share / 100,
    'receivables_domestic': receivables_domestic,
    'receivables_export': receivables_export,
    'payables_domestic': payables_domestic,
    'payables_import': payables_import,
    'inventory_days': inventory_days,
    'facilities': {
        'cc': {'enabled': facility_cc, 'margin': margin_cc / 100},
        'lc': {
            'enabled': facility_lc,
            'margin': margin_lc / 100 if facility_lc else 0,
            'share': share_lc / 100 if facility_lc else 0,
            'lead_time': lead_time_lc if facility_lc else 0,
            'usance_time': usance_time_lc if facility_lc else 0,
        },
        'pif': {
            'enabled': facility_pif,
            'margin': margin_pif / 100 if facility_pif else 0,
            'share': share_pif / 100 if facility_pif else 0,
        },
        'pre_shipment': {
            'enabled': facility_pre_shipment if has_sales_exports else False,
            'margin': margin_pre_shipment / 100 if has_sales_exports and facility_pre_shipment else 0,
        },
        'psc': {
            'enabled': facility_psc if has_sales_exports else False,
            'margin': margin_psc / 100 if has_sales_exports and facility_psc else 0,
        },
        'ebn': {
            'enabled': facility_ebn if has_sales_exports else False,
            'margin': margin_ebn / 100 if has_sales_exports and facility_ebn else 0,
        },
        'sif': {
            'enabled': facility_sif,
            'margin': margin_sif / 100 if facility_sif else 0,
            'share': share_sif / 100 if facility_sif else 0,
        },
        'sbd': {
            'enabled': facility_sbd,
            'margin': margin_sbd / 100 if facility_sbd else 0,
            'share': share_sbd / 100 if facility_sbd else 0,
        },
    },
}

# Calculate and display results
if st.button("Calculate"):
    results_v2 = calculate_limits_v2(input_data_v2)

    st.write("### Results")
    for facility, value in results_v2.items():
        if value > 0:
            st.write(f"{facility.upper()} Limit: {value:.1f} crore")
