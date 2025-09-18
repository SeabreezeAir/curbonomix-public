from backend.adapter_specs_db import list_all
from backend.quote_modifiers import apply_modifiers

def score_complexity(spec):
    duct_offset = abs(spec.supply_x_in - spec.return_x_in) + abs(spec.supply_y_in - spec.return_y_in)
    flange_factor = 1 if getattr(spec, "flange_height_in", 0) > 2 else 0
    return round(duct_offset / 10 + flange_factor, 2)

def estimate_labor(spec):
    area = spec.rtu_length_in * spec.rtu_width_in
    duct_count = 2
    return round((area / 144) * 0.5 + duct_count * 0.75, 2)

def calculate_price(spec):
    base = spec.curb_length_in * spec.curb_width_in * 0.12  # $/sq.in
    complexity = score_complexity(spec)
    labor = estimate_labor(spec)
    raw_price = base + complexity * 15 + labor * 40
    final_price, _ = apply_modifiers(raw_price, spec)
    return final_price
license_key = spec.get("license_key")
if not is_valid_license(license_key):
    return jsonify({"error": "Invalid or missing license key"}), 403

def quote_all():
    quotes = []
    for spec in list_all():
        price = calculate_price(spec)
        complexity = score_complexity(spec)
        labor = estimate_labor(spec)
        _, modifiers = apply_modifiers(price, spec)

        quote = {
            "model": spec.model,
            "price": price,
            "complexity": complexity,
            "labor_hours": labor,
            "modifiers": modifiers,
            "powered_by": "CURBONOMIX"
        }
        quotes.append(quote)
    return quotes
