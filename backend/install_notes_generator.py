import os
from fpdf import FPDF
from datetime import datetime

class Spec:
    def __init__(self, model, curb_length, curb_width, rtu_length, rtu_width, flange, sx, sy, rx, ry):
        self.model = model
        self.curb_length_in = curb_length
        self.curb_width_in = curb_width
        self.rtu_length_in = rtu_length
        self.rtu_width_in = rtu_width
        self.flange_height_in = flange
        self.supply_x_in = sx
        self.supply_y_in = sy
        self.return_x_in = rx
        self.return_y_in = ry

specs = [
    Spec("48FC04", 60, 40, 48, 34, 2, 10, 5, 30, 5),
    Spec("60FC12", 72, 48, 60, 42, 2, 12, 6, 36, 6)
]

ASSETS = "C:/Curbonomix/curbonomix-public/assets"
EXPORT_ROOT = "C:/Curbonomix/curbonomix-public/exports/adapters"

def generate_pdf(spec):
    today = datetime.today().strftime("%Y-%m-%d")
    out_dir = f"{EXPORT_ROOT}/{today}/{spec.model}"
    os.makedirs(out_dir, exist_ok=True)

    pdf_path = f"{out_dir}/install_notes.pdf"
    logo = f"{ASSETS}/logo.png"

    pdf = FPDF()
    pdf.add_page()
    pdf.image(logo, x=10, y=8, w=30)
    pdf.set_font("Arial", size=12)
    pdf.ln(40)
    pdf.cell(200, 10, txt=f"Install Notes for {spec.model}", ln=True)
    pdf.cell(200, 10, txt=f"Curb Size: {spec.curb_length_in} x {spec.curb_width_in}", ln=True)
    pdf.cell(200, 10, txt=f"RTU Footprint: {spec.rtu_length_in} x {spec.rtu_width_in}", ln=True)
    pdf.cell(200, 10, txt=f"Flange Height: {spec.flange_height_in}\"", ln=True)
    pdf.cell(200, 10, txt=f"Supply Duct: ({spec.supply_x_in}, {spec.supply_y_in})", ln=True)
    pdf.cell(200, 10, txt=f"Return Duct: ({spec.return_x_in}, {spec.return_y_in})", ln=True)
    pdf.set_font("Arial", size=8)
    pdf.set_y(-15)
    pdf.cell(200, 10, txt="Powered by CURBONOMIX", align="C")

    pdf.output(pdf_path)
    print(f"✅ PDF generated: {pdf_path}")

for spec in specs:
    generate_pdf(spec)
