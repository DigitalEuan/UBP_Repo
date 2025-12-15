# Cell 99 from UBP_UNIFIED_SYSTEM_1.ipynb

import json
import matplotlib.pyplot as plt

with open("muon_tau_ubp_big_landscape.json") as f:
    data = json.load(f)

norms = [row["Norm²"] for row in data]
mu_mev = [row["mu/e (MeV)"] for row in data]
tau_mev = [row["tau/e (MeV)"] for row in data]

plt.plot(norms, mu_mev, label="μ/e (MeV)")
plt.plot(norms, tau_mev, label="τ/e (MeV)")
plt.yscale("log")
plt.xlabel("Norm²")
plt.ylabel("Mass (MeV)")
plt.legend()
plt.show()
