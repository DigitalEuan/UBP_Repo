import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from electromagnetic_realm import ElectromagneticRealm
realm = ElectromagneticRealm()
result = realm.model_dipole_antenna_resonance(frequency_GHz=2.4, antenna_length_cm=6.25, input_power_W=1.0)
with open('/home/ubuntu/ubp_3.3/examples/results/em_01_antenna.json', 'w') as f:
    json.dump(result, f, indent=2)
print("\n✓ Dipole antenna example complete")
