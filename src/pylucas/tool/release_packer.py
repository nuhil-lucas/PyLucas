# https://git-scm.com/docs/gitignore

# Standard
from os.path import (
    exists as path_exists,
    isdir as path_isdir,
    dirname as get_dirname
)
from os import (
    listdir as root_listdir,
    chdir as set_workdir,
    makedirs,
    removedirs,
    remove as file_remove,
    getcwd
)
from sys import (
    argv
)
from zipfile import (
    ZipFile,
    ZIP_DEFLATED
)
from tomllib import (
    load as toml_load
)
# Internal
from pylucas.basic.func import dependency_check
dependency_check("pathspec", "Exception")
# External
from pathspec import GitIgnoreSpec

class ReleasePacker():
    def __init__(self, root: str = ".", name: str = "", output: str = ""):
        self.root_project: str = "/".join([part for part in root.replace("\\", "/").split("/") if not part == ""])
        self.root_release: str = self.root_project + "/release" if output == "" else output
        self.path_repignore: str = self.root_project + "/repignore"
        self.path_pyproject: str = self.root_project + "/pyproject.toml"

        self.name: str = name
        self.version: str = ""
        self.set_metadata()

        self.repignore: GitIgnoreSpec = self.get_rules()
        self.copyneed: list[str] = self.get_copyneed()

    def set_metadata(self):
        if not path_exists(self.path_pyproject):
            return
        
        pyproject: dict = dict()

        with open(self.path_pyproject, "rb") as File:
            pyproject: dict = toml_load(File)

        if not "project" in pyproject: return

        if self.name == "" and "name" in pyproject["project"]:
            self.name = pyproject["project"]["name"]
        
        if self.version == "" and "version" in pyproject["project"]:
            self.version = pyproject["project"]["version"]

    def get_rules(self):
        if not path_exists(self.path_repignore):
            return GitIgnoreSpec.from_lines([])
        with open(file=self.path_repignore, mode="r", encoding="utf-8") as File:
            return GitIgnoreSpec.from_lines(File.readlines())

    def check(self, path: str) -> bool:
        return self.repignore.match_file(path)

    def get_copyneed(self):
        copyneed: list[str] = []
        def get_subfiles(root: str):
            subpath: str = ""
            for file in root_listdir(root):
                subpath = root + "/" + file
                if path_isdir(subpath):
                    get_subfiles(subpath)
                else:
                    if not self.check(subpath):
                        copyneed.append(subpath)
        get_subfiles(self.root_project)
        return copyneed

    def build(self):
        makedirs(name=self.root_release, exist_ok=True)

        path_zip: str = f"{self.root_release}/{self.name.lower()}_{self.version}.zip"
        if path_exists(path_zip):
            if not input("This Release Already Exists. Do You Want To Overwrite It? (y/n)").lower() == "y": return
            file_remove(path_zip)

        copyneed_count: int = self.copyneed.__len__()
        with ZipFile(path_zip, 'w', ZIP_DEFLATED) as File_ZIP:
            print()
            for idx, path in enumerate(self.copyneed):
                print(f"\033[F\033[K[{idx}/{copyneed_count}] {path}")
                File_ZIP.write(path, path)
        
        print(f"Release Zip OutPut To \"{path_zip}\"")

def format_params() -> dict[str]:
    _argv_len_: int = argv.__len__()

    params: dict[str] = {
        "root": getcwd().replace("\\", "/"),
        "name": "",
        "output": ""
    }

    for idx, key in enumerate(argv):
        if not idx & 1: continue
        match key:
            case "-name":
                params["name"] = argv[idx+1] if idx+1 < _argv_len_ else ""
            case "-output":
                params["output"] = argv[idx+1] if idx+1 < _argv_len_ else ""

    return params

if __name__ == "__main__":
    rep: ReleasePacker = ReleasePacker(**format_params())
    rep.build()
