import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from gravitational_realm import demonstrate_gravitational_realm
results = demonstrate_gravitational_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/grav_02_europa.json', 'w') as f:
    json.dump(results['orbital_resonance'], f, indent=2)
print("\n✓ Jupiter-Europa resonance example complete")
