#!/bin/bash

# EM examples
cat > electromagnetic/example_01_dipole_antenna.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from electromagnetic_realm import demonstrate_electromagnetic_realm
results = demonstrate_electromagnetic_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/em_01_antenna.json', 'w') as f:
    json.dump(results['dipole'], f, indent=2)
print("\n✓ Dipole antenna example complete")
PY

cat > electromagnetic/example_02_cavity_resonator.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from electromagnetic_realm import demonstrate_electromagnetic_realm
results = demonstrate_electromagnetic_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/em_02_cavity.json', 'w') as f:
    json.dump(results['cavity'], f, indent=2)
print("\n✓ Cavity resonator example complete")
PY

# Gravitational examples
cat > gravitational/example_01_ligo_gw150914.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from gravitational_realm import demonstrate_gravitational_realm
results = demonstrate_gravitational_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/grav_01_ligo.json', 'w') as f:
    json.dump(results['gravitational_wave'], f, indent=2)
print("\n✓ LIGO GW150914 example complete")
PY

cat > gravitational/example_02_jupiter_europa.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from gravitational_realm import demonstrate_gravitational_realm
results = demonstrate_gravitational_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/grav_02_europa.json', 'w') as f:
    json.dump(results['orbital_resonance'], f, indent=2)
print("\n✓ Jupiter-Europa resonance example complete")
PY

# Biological examples
cat > biological/example_01_alpha_waves.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from biological_realm import demonstrate_biological_realm
results = demonstrate_biological_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/bio_01_alpha.json', 'w') as f:
    json.dump(results['brain_waves'], f, indent=2)
print("\n✓ Alpha brain waves example complete")
PY

cat > biological/example_02_dna_breathing.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from biological_realm import demonstrate_biological_realm
results = demonstrate_biological_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/bio_02_dna.json', 'w') as f:
    json.dump(results['dna_breathing'], f, indent=2)
print("\n✓ DNA breathing modes example complete")
PY

# Plasma examples
cat > plasma/example_01_tokamak.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from plasma_realm import demonstrate_plasma_realm
results = demonstrate_plasma_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/plasma_01_tokamak.json', 'w') as f:
    json.dump(results['tokamak'], f, indent=2)
print("\n✓ ITER tokamak example complete")
PY

cat > plasma/example_02_solar_corona.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from plasma_realm import demonstrate_plasma_realm
results = demonstrate_plasma_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/plasma_02_corona.json', 'w') as f:
    json.dump(results['corona'], f, indent=2)
print("\n✓ Solar corona example complete")
PY

# Cosmological examples
cat > cosmological/example_01_cmb.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from cosmological_realm import demonstrate_cosmological_realm
results = demonstrate_cosmological_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/cosmo_01_cmb.json', 'w') as f:
    json.dump(results['cmb'], f, indent=2)
print("\n✓ CMB fluctuations example complete")
PY

cat > cosmological/example_02_hubble_expansion.py << 'PY'
import sys; sys.path.insert(0, '/home/ubuntu/ubp_3.3')
import json
from cosmological_realm import demonstrate_cosmological_realm
results = demonstrate_cosmological_realm()
with open('/home/ubuntu/ubp_3.3/examples/results/cosmo_02_hubble.json', 'w') as f:
    json.dump(results['expansion'], f, indent=2)
print("\n✓ Hubble expansion example complete")
PY

echo "All example files created"
