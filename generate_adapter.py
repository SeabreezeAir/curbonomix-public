import FreeCAD, Part
from FreeCAD import Base
import os

# === Adapter Specoks ===
curb_length = 48.0     # inches
curb_width = 36.0
rtu_length = 42.0
rtu_width = 30.0
flange_height = 2.0

# === Paths ===
output_dir = os.path.expanduser("C:/Curbonomix/curbonomix-public/geometry")
output_file = os.path.join(output_dir, "adapter_generator.FCStd")

# === Create Document ===
doc = FreeCAD.newDocument("AdapterGenerator")

# === Create Curb Base ===
curb = Part.makeBox(curb_length, curb_width, flange_height)
curb.translate(Base.Vector(0, 0, 0))
curb_obj = doc.addObject("Part::Feature", "CurbBase")
curb_obj.Shape = curb

# === Create RTU Footprint ===
rtu = Part.makeBox(rtu_length, rtu_width, flange_height)
offset_x = (curb_length - rtu_length) / 2
offset_y = (curb_width - rtu_width) / 2
rtu.translate(Base.Vector(offset_x, offset_y, flange_height))
rtu_obj = doc.addObject("Part::Feature", "RTUFootprint")
rtu_obj.Shape = rtu

# === Fuse Geometry ===
fused = curb.fuse(rtu)
fused_obj = doc.addObject("Part::Feature", "AdapterBody")
fused_obj.Shape = fused

# === Recompute and Save ===
doc.recompute()
doc.saveAs(output_file)

print(f"✅ Adapter generated and saved to: {output_file}")
