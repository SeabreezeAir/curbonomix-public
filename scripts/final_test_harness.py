import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.adapter_specs_db import list_all
from backend.quote_adapter import calculate_price, score_complexity, estimate_labor
from backend.export_dxf_with_titleblock import export_dxf
from backend.install_notes_generator import generate_notes
from backend.bundle_adapter_packet import bundle_packet

def run_tests():
    specs = list_all()
    if not specs:
        print("❌ No specs found. Check adapter_specs.csv.")
        return

    for spec in specs:
        print(f"\n🔍 Testing: {spec.model}")
        print(f"  Price: ${calculate_price(spec)}")
        print(f"  Complexity: {score_complexity(spec)}")
        print(f"  Labor: {estimate_labor(spec)} hrs")

        try:
            export_dxf(spec)
            generate_notes(spec)
            bundle_packet(spec)
            print(f"✅ Packet built for {spec.model}")
        except Exception as e:
            print(f"❌ Error building packet for {spec.model}: {e}")

if __name__ == "__main__":
    run_tests()
