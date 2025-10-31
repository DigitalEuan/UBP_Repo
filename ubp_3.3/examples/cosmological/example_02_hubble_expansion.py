import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from cosmological_realm import demonstrate_cosmological_realm
results = demonstrate_cosmological_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/cosmo_02_hubble.json', 'w') as f:
    json.dump(results['expansion'], f, indent=2)
print("\n✓ Hubble expansion example complete")
