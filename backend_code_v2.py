def calculate_limits_v2(data):
    """
    Calculate financial limits based on input data and facility margins.

    Args:
        data (dict): Input data including turnover, purchases, WC cycle details, and facilities with margins.

    Returns:
        dict: Calculated limits for enabled facilities.
    """
    limits = {}

    # Extract input data
    turnover = data['turnover']
    domestic_share = data['domestic_sales_share']
    receivables = data['receivables_domestic']
    inventory = data['inventory_days']
    payables = data['payables_domestic']
    facilities = data['facilities']

    # Cash Credit (CC) Calculation
    if facilities['cc']['enabled']:
        wc_days = receivables + inventory - payables
        cc_limit = (turnover * domestic_share * wc_days / 365) * (1 - facilities['cc']['margin'])
        limits['cc'] = round(cc_limit, 1)  # Round to 1 decimal point

    # Other facilities
    if facilities['lc']['enabled']:
        lc_limit = turnover * (1 - facilities['lc']['margin'])
        limits['lc'] = round(lc_limit, 1)

    if facilities['pif']['enabled']:
        pif_limit = turnover * (1 - facilities['pif']['margin'])
        limits['pif'] = round(pif_limit, 1)

    if facilities['pre_shipment']['enabled']:
        pre_shipment_limit = turnover * (1 - facilities['pre_shipment']['margin'])
        limits['pre_shipment'] = round(pre_shipment_limit, 1)

    if facilities['post_shipment']['enabled']:
        post_shipment_limit = turnover * (1 - facilities['post_shipment']['margin'])
        limits['post_shipment'] = round(post_shipment_limit, 1)

    if facilities['ebd']['enabled']:
        ebd_limit = turnover * (1 - facilities['ebd']['margin'])
        limits['ebd'] = round(ebd_limit, 1)

    if facilities['sif']['enabled']:
        sif_limit = turnover * (1 - facilities['sif']['margin'])
        limits['sif'] = round(sif_limit, 1)

    if facilities['sbd']['enabled']:
        sbd_limit = turnover * (1 - facilities['sbd']['margin'])
        limits['sbd'] = round(sbd_limit, 1)

    return limits
