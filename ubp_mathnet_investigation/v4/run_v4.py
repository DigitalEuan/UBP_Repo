"""
Run UBP Swarm TCT v4.0 — full MathNet benchmark
Pure UBP substrate, no external LLMs, no numpy
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
os.chdir(os.path.join(os.path.dirname(__file__), 'core'))

from ubp_swarm_tct_mathnet_v4 import UBPSwarmMathNetV4

swarm = UBPSwarmMathNetV4()
steps, report_path, results_path = swarm.run(
    problem_set_path='../data/ubp_mathnet_problem_set.json',
    output_dir='../results'
)

print(f"\nDone. Report: {report_path}")
print(f"Results: {results_path}")
