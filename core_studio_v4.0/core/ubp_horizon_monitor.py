"""
UBP Horizon Monitor v1.0 (Production)
=====================================
A topological diagnostic tool for detecting phase transitions in growing systems.
Maps scalar values against the three fundamental UBP Horizons.

Usage:
    from ubp_horizon_monitor import HorizonMonitor
    monitor = HorizonMonitor()
    monitor.check(2048, "My System")
"""
import math

class HorizonMonitor:
    def __init__(self):
        self.HORIZONS = {
            "GENOMIC (Base-4)": 6.0,    # 4096
            "BINARY (Base-2)": 12.0,    # 4096
            "BIOLOGIC (Phi)": 18.0      # ~4181 (F_19)
        }
        # The Observer Constant (Efficiency Limit)
        self.Y = 0.264675
        self.SAFE_LOAD = 1.0 - self.Y  # ~73.5%

    def check(self, value, name="Metric"):
        """Checks a value against all horizons."""
        if value <= 0: return
        
        print(f"\n[HORIZON CHECK] {name}: {value}")
        
        # Calculate Logarithmic Densities
        densities = {
            "GENOMIC": math.log(value, 4),
            "BINARY": math.log(value, 2),
            "BIOLOGIC": math.log(value, 1.61803398875)
        }
        
        for h_name, limit in self.HORIZONS.items():
            current = densities[h_name.split()[0]]
            dist = limit - current
            load_pct = (current / limit)
            
            # Determine Status
            if dist < 0:
                status = "CRITICAL (Post-Horizon)"
                color = "RED"
            elif dist < 0.1:
                status = "CONTACT (Singularity)"
                color = "FLASHING RED"
            elif load_pct > self.SAFE_LOAD:
                status = "WARNING (High Pressure)"
                color = "YELLOW"
            else:
                status = "STABLE"
                color = "GREEN"
                
            print(f"  > {h_name:<16} | Load: {load_pct*100:.1f}% | {color} {status}")

if __name__ == "__main__":
    # Self-Test
    hm = HorizonMonitor()
    hm.check(137, "Alpha")
    hm.check(4096, "Golay Limit")