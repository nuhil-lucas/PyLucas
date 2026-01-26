from os.path import (
    exists as op_exists,
    splitext as op_splitext,
    basename as op_basename,
)

"""
ZIP         .zip            zipfile
TAR         .tar            tarfile
TAR+GZIP    .tar.gz | .tgz  tarfile
TAR+BZIP2   .tar.bz2        tarfile
TAR+XZ      .tar.xz         tarfile
"""


class ZipFile:
    TEMPDIR: str = "./temp"

    def archive(file: str, dest: str):
        pass
        

    def extract(file: str, dest: str):
        file_name: str = None
        file_ext: str = None
        file_name, file_ext = op_splitext(op_basename(file))



    if __name__ == "__main__":
        extract(
            file=r"C:\Users\user\Downloads\example.zip",
            dest=r"C:\Users\user\Downloads\extracted"
        )