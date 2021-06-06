
#
#E4FI AJOUT pour run les tests. 
#
#Extrait du rapport:
#Ensuite les analyses qualitatives font varier différents paramètres, qu’on peut retrouver dans le code.
#Le « analysisQualitativeRun.py » lance le code « Watershed.py » avec les différents paramètres. 
#Il faut cependant préciser au script le path de l’exe python dans l’environnement virtuel où tous les requirements.txt sont installés.
# Le path doit être similaire à celui utiliser pour activer l’environnement, en remplaçant « activate » par python. 
#Par exemple sous visual studio code, j’utilise « .venv\scripts\activate », et donc j’utilise 
#python analysisQualitativePreprocessed.py 
#python analysisQualitativeRun.py -v ".venv/scripts/python"

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

command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "0.059", "-sd","1", "-rn",imgFinishName+"a" , "-dt","manhattan","-mm", "True", "-se", "3"], capture_output=True)
command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "0.143", "-sd","1", "-rn",imgFinishName+"b" ,"-dt","manhattan", "-mm", "True", "-se", "3"], capture_output=True)
command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "0.2", "-sd","1", "-rn",imgFinishName+"c" , "-dt","manhattan", "-mm", "True", "-se", "3"], capture_output=True)
command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "25", "-a", "1", "-sd","1", "-rn",imgFinishName+"d" , "-dt","manhattan", "-mm", "True", "-se", "3"], capture_output=True)


imgProcessedPath="./Images/2D/fig2bis.png"
imgFinishName="./Images/2D/fig2"
command = subprocess.run([venvPython, "Watershed.py","-p",imgProcessedPath, "-d", "27", "-a", "0.091","-g","morpho","-sd","1", "-rn",imgFinishName+"a" ,"-dt","manhattan", "-mm", "True", "-se", "3"], capture_output=True)

sys.stdout.buffer.write(command.stdout)
sys.stderr.buffer.write(command.stderr)
sys.exit(command.returncode)
