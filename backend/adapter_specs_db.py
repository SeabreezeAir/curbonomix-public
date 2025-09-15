import csv

class AdapterSpec:
    def __init__(self, row):
        self.model = row.get("model", "").strip()
        self.rtu_length_in = float(row.get("rtu_length_in", 0))
        self.rtu_width_in = float(row.get("rtu_width_in", 0))
        self.curb_length_in = float(row.get("curb_length_in", 0))
        self.curb_width_in = float(row.get("curb_width_in", 0))
        self.supply_x_in = float(row.get("supply_x_in", 0))
        self.supply_y_in = float(row.get("supply_y_in", 0))
        self.return_x_in = float(row.get("return_x_in", 0))
        self.return_y_in = float(row.get("return_y_in", 0))
        self.flange_height_in = float(row.get("flange_height_in", 0))

        # Optional modifiers
        self.insulated = row.get("insulated", "").lower() == "yes"
        self.gauge = row.get("gauge", "24").strip()
        self.duct_type = row.get("duct_type", "standard").strip()

    def __repr__(self):
        return f"<AdapterSpec {self.model}>"

def list_all():
    specs = []
    path = "C:/Curbonomix/curbonomix-public/data/adapter_specs.csv"
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    spec = AdapterSpec(row)
                    specs.append(spec)
                except Exception as e:
                    print(f"⚠️ Error parsing row: {row}\n{e}")
    except FileNotFoundError:
        print(f"❌ Spec file not found: {path}")
    return specs
