import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from plasma_realm import demonstrate_plasma_realm
results = demonstrate_plasma_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/plasma_02_corona.json', 'w') as f:
    json.dump(results['corona'], f, indent=2)
print("\n✓ Solar corona example complete")
