import os
import ezdxf
from datetime import datetime

TEMPLATE_PATH = "C:/Curbonomix/curbonomix-public/templates/curbonomix_title_block.dxf"
EXPORT_ROOT = "C:/Curbonomix/curbonomix-public/exports/adapters"
GEOMETRY_ROOT = "C:/Curbonomix/curbonomix-public/geometry"

def stamp_dxf(model):
    today = datetime.today().strftime("%Y-%m-%d")
    out_dir = f"{EXPORT_ROOT}/{today}/{model}"
    os.makedirs(out_dir, exist_ok=True)

    adapter_dxf = f"{out_dir}/adapter.dxf"
    stamped_dxf = f"{out_dir}/adapter_stamped.dxf"

    # === Load geometry DXF
    geo_doc = ezdxf.readfile(adapter_dxf)
    geo_msp = geo_doc.modelspace()

    # === Load title block template
    template_doc = ezdxf.readfile(TEMPLATE_PATH)
    template_msp = template_doc.modelspace()

    # === Merge geometry into title block
    for entity in geo_msp:
        template_msp.add_entity(entity)

    # === Stamp metadata
    template_msp.add_text(f"Model: {model}", dxfattribs={
        "height": 2.5,
        "insert": (10, 5)
    })
    template_msp.add_text(f"Date: {today}", dxfattribs={
        "height": 2.5,
        "insert": (10, 2)
    })
    template_msp.add_text("Powered by CURBONOMIX", dxfattribs={
        "height": 2.5,
        "insert": (10, -1)
    })

    template_doc.saveas(stamped_dxf)
    print(f"✅ Stamped DXF: {stamped_dxf}")
