Universal Binary Theory: Clay Millennium Prize Problems Solutions
Euan Craig, New Zealand, 2025.


cd ~/ubp_arXiv_mpp1

source ~/ubp_arXiv_mpp1/ubp_env/bin/activate

pip install numpy scipy matplotlib memory_profiler
pip install seaborn

python3 ubp_visualization_generator.py

python3 bsd_hodge_validator.py

python3 millennium_validator.py