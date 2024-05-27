def compare_data(existing_data, extracted_data):
    discrepancies = {}

    all_keys = set(existing_data.keys()).union(set(extracted_data.keys()))

    for key in all_keys:
        existing_value = existing_data.get(key, None)
        extracted_value = extracted_data.get(key, None)
        if existing_value != extracted_value:
            discrepancies[key] = {
                "existing": existing_value,
                "extracted": extracted_value
            }
    return discrepancies
