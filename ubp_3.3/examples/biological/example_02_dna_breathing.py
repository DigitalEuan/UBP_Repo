import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from biological_realm import demonstrate_biological_realm
results = demonstrate_biological_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/bio_02_dna.json', 'w') as f:
    json.dump(results['dna_breathing'], f, indent=2)
print("\n✓ DNA breathing modes example complete")
