# Standard
import ssl
from ssl import SSLCertVerificationError
from urllib.request import (
    Request,
    ProxyHandler,
    OpenerDirector,
    urlopen,
    build_opener
)
from urllib.error import (
    URLError
)
from http.client import (
    HTTPResponse
)
from time import time
from typing import (
    Literal
)
from asyncio import (
    sleep as asio_sleep,
    create_task as asio_create_task,
    run as asio_run,
    gather as asio_gather
)
# Internal
from pylucas.basic import Result
# External

class ResponseFile():
    def __init__(self, response: HTTPResponse, file_name: str = None, chunk_size: int = 65536, show_process: bool = True):
        self.response: HTTPResponse = response
        self.file_name: str = None
        self.chunk_size: int = chunk_size
        self.show_process: bool = show_process
        self.process: dict[Literal["time_start", "time_use", "total_size", "downloaded", "completed"], float | int | bool] = {
            "time_start": 0.00,  # Second
            "time_use": 0.00, # Second
            "total_size": 0.0 if (total_size:=response.getheader("Content-Length")) is None else int(total_size), # Byte
            "downloaded": 0, # Byte
            "completed": False
        }
        self.refresh_interval: float = 1.0
        self.rate_unit: Literal["Byte", "KB", "MB"] = "MB"
        self.rate_units: dict[str, int] = {
            "Byte": 1,
            "KB": 1024,
            "MB": 1024**2
        }

        if not file_name is None:
            self.file_name: str = file_name
        elif not (filename:=response.getheader("Content-Disposition")) is None and  "filename" in filename:
            file_name = filename[filename.find("filename=")+9:]
            if file_name.startswith('"') and file_name.endswith('"'): file_name = file_name[1: -1]
            self.file_name = file_name
        else:
            self.file_name = self.response.url.split("/")[-1]
        
        for key_char in "<>:\"|?*\\/":
            if key_char in self.file_name:
                raise NameError(f"Non-standard File Name: {self.file_name}")
    
    def download(self):
        async def main():
            if self.show_process:
                await asio_gather(self._download_bychunk_(), self._show_process_())
            else:
                await asio_create_task(self._download_bychunk_())

        asio_run(main())

    async def _show_process_(self):
        last_ptl: int = 0 # last process text len
        this_ptl: int = 0 # this process text len
        print()
        while not self.process["completed"]:
            speed: str = f"-- {self.rate_unit}PS" if self.process['time_use'] == 0 else f"{round(self.process['downloaded']/self.rate_units[self.rate_unit]/self.process['time_use'], 2)} {self.rate_unit}PS"
            downloaded: str = f"{round(self.process['downloaded']/self.rate_units[self.rate_unit], 2)}/{round(self.process['total_size']/self.rate_units[self.rate_unit], 2)} {self.rate_unit}"

            process_text: str = f"{speed} ({downloaded})"
            
            this_ptl = process_text.__len__()

            print(f"\r{process_text}{' '*(last_ptl - this_ptl) if last_ptl > this_ptl else ''}", end="")
            
            last_ptl = process_text.__len__()
            await asio_sleep(self.refresh_interval)

    async def _download_bychunk_(self):
        try:
            with self.response as response:
                with open(self.file_name, 'wb') as File:
                    self.process["time_start"] = time()
                    while True:
                        chunk: bytes = response.read(self.chunk_size)
                        if not chunk: break

                        File.write(chunk)

                        self.process["downloaded"] += len(chunk)
                        self.process["time_use"] = time() - self.process["time_start"]
                        await asio_sleep(0)
        except Exception as E:
            self.process["completed"] = True
            print(f"下载失败: {E}")
        else:
            self.process["completed"] = True
            print(f"下载成功: {self.file_name}")
        finally:
            print()

def download_cacert():
    url: str = "https://curl.se/ca/cacert.pem"
    path: str = "./cacert.pem"
    # path: str = "./certificate/cacert.pem"
    try:
        response: HTTPResponse = urlopen(url)
        ResponseFile(response=response, file_name=path)
    except URLError as E:
        return Result(False, E.reason)
    except Exception as E:
        return Result(False, str(E))
    else:
        return Result(True, )

def download_file(url: str, file_name: str = None, show_process: bool = True) -> Result[bool, str]:
    result: Result = None

    rf: ResponseFile = None

    CVF: bool = False

    try:
        rf = ResponseFile(response=urlopen(url), file_name=file_name, show_process=show_process)
        rf.download()
    except URLError as E:
            if (
                isinstance(E.reason, SSLCertVerificationError) and
                E.reason.reason == "CERTIFICATE_VERIFY_FAILED"
            ):
                CVF = True
            result = Result(False, E.reason)
    except Exception as E:
        result = Result(False, E)
    else:
        result = Result(True, rf.file_name)

    if not result and CVF:
        result_dlcacert: Result = download_cacert()
        if result_dlcacert:
            try:
                ssl_context = ssl.create_default_context(cafile="./cacert.pem")
                rf = ResponseFile(response=urlopen(url, context=ssl_context), file_name=file_name, show_process=show_process)
                rf.download()
            except URLError as E:
                result = Result(False, E.reason)
            except Exception as E:
                result = Result(False, E)
            else:
                result = Result(True, rf.file_name)

    return result

if __name__ == "__main__":
    urls: list[str] = [
        "https://github.com/EcoPasteHub/EcoPaste/releases/download/v0.6.0-beta.3/EcoPaste_0.6.0-beta.3_amd64.AppImage", # 84.5 MB
        "https://github.com/EcoPasteHub/EcoPaste/releases/download/v0.6.0-beta.3/EcoPaste_x64.app.tar.gz.sig", # 408 Bytes
        "https://curl.se/ca/cacert.pem" # 
    ]
    url: str = urls[1]
    result: Result = download_file(url, show_process=False)
    print(result)