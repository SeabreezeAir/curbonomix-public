import os, csv
import FreeCAD, Part
from FreeCAD import Base

INPUT_CSV = "C:/Curbonomix/data/adapter_specs.csv"
OUTPUT_DIR = "C:/Curbonomix/geometry"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_row(row):
    return {
        "model": row["model"].strip(),
        "curb_length": float(row["curb_length"]),
        "curb_width": float(row["curb_width"]),
        "rtu_length": float(row["rtu_length"]),
        "rtu_width": float(row["rtu_width"]),
        "flange_height": float(row.get("flange_height", 2)),
        "supply_x": float(row["supply_x"]),
        "supply_y": float(row["supply_y"]),
        "return_x": float(row["return_x"]),
        "return_y": float(row["return_y"]),
    }

with open(INPUT_CSV, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        spec = parse_row(row)
        doc = FreeCAD.newDocument(spec["model"])

        # === Curb Base ===
        curb = Part.makeBox(spec["curb_length"], spec["curb_width"], spec["flange_height"])
        curb_obj = doc.addObject("Part::Feature", "CurbBase")
        curb_obj.Shape = curb

        # === RTU Footprint ===
        offset_x = (spec["curb_length"] - spec["rtu_length"]) / 2
        offset_y = (spec["curb_width"] - spec["rtu_width"]) / 2
        rtu = Part.makeBox(spec["rtu_length"], spec["rtu_width"], spec["flange_height"])
        rtu.translate(Base.Vector(offset_x, offset_y, spec["flange_height"]))

        # === Duct Cutouts ===
        supply = Part.makeBox(12, 12, spec["flange_height"])
        supply.translate(Base.Vector(spec["supply_x"], spec["supply_y"], spec["flange_height"]))
        return_duct = Part.makeBox(16, 16, spec["flange_height"])
        return_duct.translate(Base.Vector(spec["return_x"], spec["return_y"], spec["flange_height"]))

        rtu_cut = rtu.cut(supply).cut(return_duct)
        rtu_obj = doc.addObject("Part::Feature", "RTUFootprint")
        rtu_obj.Shape = rtu_cut

        # === Fuse Geometry ===
        fused = curb.fuse(rtu_cut)
        fused_obj = doc.addObject("Part::Feature", "AdapterBody")
        fused_obj.Shape = fused

        doc.recompute()
        doc.saveAs(f"{OUTPUT_DIR}/{spec['model']}.FCStd")
        print(f"✅ Saved: {spec['model']}.FCStd")
