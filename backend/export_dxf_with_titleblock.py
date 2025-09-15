import os
import ezdxf
import sys

# Ensure root path is recognized
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.adapter_specs_db import list_all

EXPORT_DIR = "C:/Curbonomix/curbonomix-public/exports/dxf"

def export_dxf(spec):
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Draw curb rectangle
    x_len = spec.curb_length_in
    y_len = spec.curb_width_in
    msp.add_lwpolyline([
        (0, 0),
        (x_len, 0),
        (x_len, y_len),
        (0, y_len),
        (0, 0)
    ], close=True)

    # Add title block
    msp.add_text(f"Model: {spec.model}", dxfattribs={'height': 2}).set_pos((0, -5))
    msp.add_text(f"Size: {x_len} x {y_len} in", dxfattribs={'height': 2}).set_pos((0, -8))
    msp.add_text("Powered by CURBONOMIX", dxfattribs={'height': 2}).set_pos((0, -11))

    # Save DXF
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{spec.model}.dxf")
    doc.saveas(path)
    return path
