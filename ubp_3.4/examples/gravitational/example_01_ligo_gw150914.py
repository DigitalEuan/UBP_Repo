# UBP 3.4 Example
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from gravitational_realm import demonstrate_gravitational_realm
results = demonstrate_gravitational_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/grav_01_ligo.json', 'w') as f:
    json.dump(results['gravitational_wave'], f, indent=2)
print("\n✓ LIGO GW150914 example complete")
