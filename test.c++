gaps create images/pillars.jpg puzzle.jpg --size=64
gaps run puzzle.jpg solution.jpg --generations=20 --population=600 --debug
python3 gaps/cli.py run puzzle.jpg solution.jpg --size=64 --generations=20 --population=600 --debug
python3 gaps/cli.py run puzzle.jpg solution.jpg --size=64 --generations=20 --population=600 --mutation-rate=0.02 --debug
pip install . --force-reinstall --no-cache-dir


gaps create images/pillars.jpg puzzle.jpg --size=64
gaps run puzzle.jpg solution.jpg --generations=20 --population=600 --mutation-rate=0.02 --debug