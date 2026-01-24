from urllib.request import (
    Request,
    urlopen
)
from urllib.error import (
    URLError
)
from http.client import (
    HTTPResponse
)
from json import (
    loads as json_loads,
)
from re import (
    search as re_search,
)
from typing import (
    Generator
)
from pylucas.basic import Result

class GitHubReleases():
    def __init__(self, data: dict):
        self.data: dict = data
        self._search_ = self.Search(self.data)

    class Search():
        def __init__(self, data: dict):
            self.data = data

        def with_tag(self, name: str = ".*", assets: str = ".*") -> Generator[dict, None, None]:
            for release in self.data:
                if not "name" in release: continue
                if re_search(name, release["name"]) is None: continue

                for asset in release["assets"]:
                    if not "name" in asset: continue
                    if re_search(assets, asset["name"]) is None: continue
                    
                    result: dict = {
                        "name": release["name"],
                        "file": asset["name"],
                        "url": asset["browser_download_url"],
                        "digest": asset["digest"]
                    }
                    yield result

    def search(self):
        return self._search_

class GitHub():
    @classmethod
    def get_releases(cls, owner: str, repo: str, latest: bool = True) -> Result[bool, str | GitHubReleases]:
        try:
            request: Request = Request(f"https://api.github.com/repos/{owner}/{repo}/releases" + ("/latest" if latest else ""))
            request.add_header("User-Agent", "Python-urllib")
            response: HTTPResponse = urlopen(request)
            github_releases: dict = json_loads(response.read().decode())
        except URLError as E:
            return Result(False, E.reason)
        except Exception as E:
            return Result(False, str(E))
        else:
            return Result(True, GitHubReleases([github_releases] if latest else github_releases))

if __name__ == "__main__":
    from sys import exit
    import json
    
    gr: Result[bool, GitHubReleases] = GitHub.get_releases(owner = "mosheng1", repo = "QuickClipboard", latest=False)

    if gr:
        gr: GitHubReleases = gr.data
    else:
        with open("test.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        gr: GitHubReleases = GitHubReleases(data)

    matched_gr: dict = next(gr.search().with_tag("QuickClipboard.*", ".*_x64-setup.exe"), None)

    if matched_gr is None: exit("No matched release asset found.")

    from pylucas.net import download_file

    download_file(matched_gr["url"], file_name=matched_gr["file"])