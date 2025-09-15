import sys
sys.path.append("C:/Curbonomix/curbonomix-public/")
from backend.adapter_specs_db import list_all
import os, json, zipfile
from datetime import datetime
from fpdf import FPDF
from backend.adapter_specs_db import list_all
EXPORT_ROOT = "C:/Curbonomix/exports/adapters"
GEOMETRY_ROOT = "C:/Curbonomix/geometry"

def generate_metadata(spec):
    return {
        "model": spec.model,
        "curb": {
            "length": spec.curb_length_in,
            "width": spec.curb_width_in
        },
        "rtu": {
            "length": spec.rtu_length_in,
            "width": spec.rtu_width_in
        },
        "flange_height": spec.flange_height_in,
        "ducts": {
            "supply": {"x": spec.supply_x_in, "y": spec.supply_y_in},
            "return": {"x": spec.return_x_in, "y": spec.return_y_in}
        },
        "powered_by": "CURBONOMIX"
    }

def generate_pdf(spec, path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.image("C:/Curbonomix/assets/logo.png", x=10, y=8, w=30)
    pdf.ln(30)
    pdf.cell(200, 10, txt=f"Install Notes for {spec.model}", ln=True)
    pdf.cell(200, 10, txt=f"Curb Size: {spec.curb_length_in} x {spec.curb_width_in}", ln=True)
    pdf.cell(200, 10, txt=f"RTU Footprint: {spec.rtu_length_in} x {spec.rtu_width_in}", ln=True)
    pdf.cell(200, 10, txt=f"Flange Height: {spec.flange_height_in}\"", ln=True)
    pdf.cell(200, 10, txt=f"Supply Duct: ({spec.supply_x_in}, {spec.supply_y_in})", ln=True)
    pdf.cell(200, 10, txt=f"Return Duct: ({spec.return_x_in}, {spec.return_y_in})", ln=True)
    pdf.output(path)

def bundle(spec):
    today = datetime.today().strftime("%Y-%m-%d")
    out_dir = f"{EXPORT_ROOT}/{today}/{spec.model}"
    os.makedirs(out_dir, exist_ok=True)

    # === Paths
    fcstd_path = f"{GEOMETRY_ROOT}/{spec.model}.FCStd"
    dxf_path = f"{out_dir}/adapter.dxf"  # Placeholder for DXF export
    pdf_path = f"{out_dir}/install_notes.pdf"
    meta_path = f"{out_dir}/metadata.json"
    zip_path = f"{out_dir}/install_packet.zip"

    # === Generate Metadata + PDF
    with open(meta_path, "w") as f:
        json.dump(generate_metadata(spec), f, indent=2)
    generate_pdf(spec, pdf_path)

    # === Bundle ZIP
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(fcstd_path, arcname="adapter.FCStd")
        zipf.write(dxf_path, arcname="adapter.dxf")
        zipf.write(pdf_path, arcname="install_notes.pdf")
        zipf.write(meta_path, arcname="metadata.json")

    print(f"✅ Bundled: {zip_path}")

# === Usage Example ===
from adapter_specs_db import list_all
for spec in list_all():
    bundle(spec)
