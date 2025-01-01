def calculate_limits_v2(data):
    """
    Calculate limits for the facilities based on input data.

    Args:
        data (dict): Input data structure from the frontend.

    Returns:
        dict: Facility limits.
    """
    # Extract inputs
    turnover = data['turnover']
    purchases = data['purchases']
    export_sales_share = data['export_sales_share']
    import_purchases_share = data['import_purchases_share']
    receivables_domestic = data['receivables_domestic']
    receivables_export = data['receivables_export']
    payables_domestic = data['payables_domestic']
    payables_import = data['payables_import']
    inventory_days = data['inventory_days']

    facilities = data['facilities']

    # Initialize limits dictionary
    limits = {}

    # Facility limit calculations
    # Cash Credit (CC)
    if facilities['cc']['enabled']:
        wc_days = receivables_domestic + inventory_days - payables_domestic
        cc_limit = (turnover * (1 - export_sales_share) * wc_days / 365) * (1 - facilities['cc']['margin'])
        limits['cc'] = cc_limit

    # Letter of Credit (LC)
    if facilities['lc']['enabled']:
        lc_limit = (purchases * import_purchases_share *
                    (facilities['lc']['lead_time'] + facilities['lc']['usance_time']) / 365) * (1 - facilities['lc']['margin'])
        limits['lc'] = lc_limit

    # Purchase Invoice Finance (PIF)
    if facilities['pif']['enabled']:
        pif_limit = (purchases * facilities['pif']['share'] *
                     (payables_domestic if (1 - import_purchases_share) > 0 else payables_import) / 365) * (1 - facilities['pif']['margin'])
        limits['pif'] = pif_limit

    # Pre-shipment Credit
    if facilities['pre_shipment']['enabled']:
        pre_shipment_limit = (turnover * export_sales_share * inventory_days / 365) * (1 - facilities['pre_shipment']['margin'])
        limits['pre_shipment'] = pre_shipment_limit

    # Post-shipment Credit (PSC)
    if facilities['psc']['enabled']:
        post_shipment_limit = (turnover * export_sales_share * receivables_export / 365) * (1 - facilities['psc']['margin'])
        limits['psc'] = post_shipment_limit

    # Export Bill Negotiation (EBN)
    if facilities['ebn']['enabled']:
        ebn_limit = (turnover * export_sales_share * receivables_export / 365) * (1 - facilities['ebn']['margin'])
        limits['ebn'] = ebn_limit

    # Sales Invoice Finance (SIF)
    if facilities['sif']['enabled']:
        sif_limit = (turnover * (1 - export_sales_share) * receivables_domestic / 365) * (1 - facilities['sif']['margin'])
        limits['sif'] = sif_limit

    # Sales Bill Discounting (SBD)
    if facilities['sbd']['enabled']:
        sbd_limit = (turnover * (1 - export_sales_share) * receivables_domestic / 365) * (1 - facilities['sbd']['margin'])
        limits['sbd'] = sbd_limit

    # Return the calculated limits
    return {key: round(value, 1) for key, value in limits.items() if value > 0}
