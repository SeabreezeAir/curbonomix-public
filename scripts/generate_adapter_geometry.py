import os
import sys
import importlib
import FreeCAD, Part

try:
    from adapter_specs_db import list_all
except Exception:
    # If adapter_specs_db isn't on sys.path (e.g., running as a script),
    # add the script directory to sys.path and import via importlib.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    list_all = importlib.import_module("adapter_specs_db").list_all

GEOMETRY_ROOT = "C:/Curbonomix/curbonomix-public/geometry"

def build_adapter(spec):
    doc = FreeCAD.newDocument(spec.model)

    # === Create curb base
    curb = Part.makeBox(spec.curb_length_in, spec.curb_width_in, spec.flange_height_in)
    curb.translate(FreeCAD.Vector(0, 0, 0))

    # === Create RTU footprint cutout
    rtu = Part.makeBox(spec.rtu_length_in, spec.rtu_width_in, spec.flange_height_in + 0.1)
    rtu.translate(FreeCAD.Vector(
        (spec.curb_length_in - spec.rtu_length_in) / 2,
        (spec.curb_width_in - spec.rtu_width_in) / 2,
        0
    ))

    # === Subtract RTU from curb
    adapter = curb.cut(rtu)
    Part.show(adapter)

    # === Save model
    out_path = f"{GEOMETRY_ROOT}/{spec.model}.FCStd"
    doc.saveAs(out_path)
    print(f"✅ Geometry saved: {out_path}")

for spec in list_all():
    build_adapter(spec)
