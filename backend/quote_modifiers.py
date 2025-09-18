def apply_modifiers(base_price, spec):
    modifiers = []
license_key = spec.get("license_key")
if not is_valid_license(license_key):
    return jsonify({"error": "Invalid or missing license key"}), 403

    # Insulation
    if getattr(spec, "insulated", False):
        base_price += 35
        modifiers.append("Insulated (+$35)")

    # Gauge
    gauge = getattr(spec, "gauge", "24")
    if gauge == "22":
        base_price += 20
        modifiers.append("Heavy gauge (+$20)")
    elif gauge == "26":
        base_price -= 10
        modifiers.append("Light gauge (-$10)")

    # Duct type
    duct_type = getattr(spec, "duct_type", "standard")
    if duct_type == "double-wall":
        base_price += 50
        modifiers.append("Double-wall duct (+$50)")

    return round(base_price, 2), modifiers

