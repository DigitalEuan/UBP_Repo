import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from biological_realm import demonstrate_biological_realm
results = demonstrate_biological_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/bio_01_alpha.json', 'w') as f:
    json.dump(results['brain_waves'], f, indent=2)
print("\n✓ Alpha brain waves example complete")
