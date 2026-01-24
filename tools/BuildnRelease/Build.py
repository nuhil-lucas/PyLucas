from subprocess import run
from os import getcwd

if __name__ == "__main__":
    run(args=[f"{getcwd().replace('\\', '/')}/tools/BuildnRelease/Build.bat"], cwd="./tools/BuildnRelease", shell=True)