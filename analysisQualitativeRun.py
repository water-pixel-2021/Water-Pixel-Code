import subprocess
import sys
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-v", "--venvPython", type=str, help="path to virtual environment python executable, ex:.venv/scripts/python")
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


venvPython = args.venvPython

imgProcessedPath="./Images/2D/fig1bis.png"
imgFinishName="./Images/2D/fig1"

# command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "0.059", "-sd","1", "-rn",imgFinishName+"a" , "-mm", "True", "-se", "3"], capture_output=True)
# command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "0.143", "-sd","1", "-rn",imgFinishName+"b" , "-mm", "True", "-se", "3"], capture_output=True)
# command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "0.2", "-sd","1", "-rn",imgFinishName+"c" , "-mm", "True", "-se", "3"], capture_output=True)
# command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "1", "-sd","1", "-rn",imgFinishName+"d" , "-mm", "True", "-se", "3"], capture_output=True)


imgProcessedPath="./Images/2D/fig2bis.png"
imgFinishName="./Images/2D/fig2"
command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "27", "-a", "0.091","-g","morpho","-sd","1", "-rn",imgFinishName+"a" , "-mm", "True", "-se", "3"], capture_output=True)

sys.stdout.buffer.write(command.stdout)
sys.stderr.buffer.write(command.stderr)
sys.exit(command.returncode)
