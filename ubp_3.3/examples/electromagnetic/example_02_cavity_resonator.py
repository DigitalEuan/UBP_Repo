import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from electromagnetic_realm import demonstrate_electromagnetic_realm
results = demonstrate_electromagnetic_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/em_02_cavity.json', 'w') as f:
    json.dump(results['cavity'], f, indent=2)
print("\n✓ Cavity resonator example complete")
