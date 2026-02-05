# Standard
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
# Internal
from pylucas.basic import Result
# External

class GitHubReleases():

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

    def __init__(self, data: dict):
        self.data: dict = data
        self.search = self.Search(self.data)

    def last(self, assets: str = ".*") -> Generator[dict, None, None]:
        for release in self.data:
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
            break

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
    from pylucas.net import download_file
    from pylucas.basic.func import terminal_clear
    from json import loads as json_loads, dumps as json_dumps

    terminal_clear()
    
    get_online: bool = False

    release: GitHubReleases = None

    if get_online:
        result: Result[bool, GitHubReleases] = GitHub.get_releases(owner = "mosheng1", repo = "QuickClipboard", latest=False)

        if not result:
            exit(f"Error: {result.data}")

        release = result()

        with open("./tests/github_quickclipboard_releases.json", "w", encoding="utf-8") as file:
            file.write(json_dumps(release.data, indent=4))
    else:
        with open("./tests/github_quickclipboard_releases.json", "r", encoding="utf-8") as file:
            release_data: dict = json_loads(file.read())
        release = GitHubReleases(release_data)

    for matched_release in release.search.with_tag("QuickClipboard v0.2.0-beta.4.*", "x64"):
        print(matched_release)
    
    print("-----")

    for matched_release in release.last_release(assets=r".*x64.*\.exe$"):
        print(matched_release)


    if matched_release is None: exit("No matched release asset found.")
