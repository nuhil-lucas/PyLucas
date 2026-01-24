

# PyLucas

一个轻量的 Python 实用工具集，提供结果封装、时间/列表辅助、彩色与 ASCII 输出、配置读写、文件操作、日志管理、下载与 GitHub Releases 查询、简易发布打包等常用能力。

## 特性

- 统一 `Result` 结果封装与异常获取
- 时间戳、索引、依赖检测等基础函数
- 彩色输出与 ASCII 艺术字打印
- Excel 读取与基础清洗（基于 pandas）
- 配置文件编辑（TOML/JSON）
- 文件列表、复制与清理工具
- 日志管理与自动日志文件轮转
- HTTP 下载器与 GitHub Releases 查询
- 发布包打包工具（支持 repignore）

## 安装

```bash
pip install pylucas
```

本项目要求 Python $\ge 3.12$。

依赖（已在包中声明）：`所有依赖均不强制要求, 使用对应功能前请确保依赖已安装`

- tomli-w (配置文件读写)
- art（ASCII 字体制）
- pandas（Excel 读取）
- pathspec（发布包忽略规则）

## 快速开始

```python
from pylucas.basic import Result
from pylucas.basic.func import time_stamp, dependency_check

result = Result(True, {"a": 1}, "ok")
print(bool(result))
print(result())
print(result.Exception)

print(time_stamp())
print(dependency_check("pip", mode="str"))
```

## 模块一览与示例

### basic

**Result 结果封装**

```python
from pylucas.basic import Result

res = Result(True, 123, "ok")
if res:
	print(res())
else:
	raise res.Exception
```

**基础函数**

```python
from pylucas.basic.func import time_stamp, lindex, rindex, dependency_check

print(time_stamp())
print(lindex(["a", "b", "c"], "b"))
print(rindex(["a", "b", "c", "b"], "b"))
print(dependency_check("pip", mode="dict"))
```

### better_print

**彩色输出**

```python
from pylucas.better_print import CPrint

CPrint.info("info")
CPrint.warn("warn")
CPrint.error("error")
CPrint.success("success")
CPrint("custom", color="#00FFAA", reset=True)
```

**ASCII 艺术字（需安装 art）**

```python
from pylucas.better_print import APrint

APrint.tittle("Hello", split_line="#")
```

### cute_panda

**Excel 读取与基础清洗**

```python
from pylucas.cute_panda import read_excel

df = read_excel(
	io="./demo.xlsx",
	sheet_name=0,
	key_tags=["姓名", ["学号", "编号"]],
	search_range=15,
)
print(df.head())
```

### file (计划重构)

**配置文件编辑（TOML/JSON）**

```python
from pylucas.file import ConfigEditor

cfg = ConfigEditor(File="./config.toml", Data={"a": {"b": 1}})
cfg.SetValue("a.c", 2)
print(cfg.GetValue("a.c", ResultType="Self"))
```

**文件列表、复制与清理**

```python
from pylucas.file import ListFiles, FilesCopyer, FilesClear

files = ListFiles("./data", Types=("*.txt",), Includes="log", Mode="Path")
FilesCopyer("./src", "./dst", Mode="Tree")
FilesClear(*files, Mode="File")
```

### loger

**日志管理**

```python
from pylucas.loger import LogManager

logger = LogManager(title="MyApp", dir_log="./log", limit_log_files=5)
logger("hello", level="info")
logger.log("warn message", level="warn", module="demo")
```

### net

**文件下载**

```python
from pylucas.net import download_file

result = download_file("https://example.com/file.zip", show_process=True)
print(result)
```

**GitHub Releases 查询**

```python
from pylucas.net import GitHub

res = GitHub.get_releases(owner="octocat", repo="Hello-World", latest=True)
if res:
	release = res.data
	asset = next(release.search().with_tag(".*", ".*"), None)
	print(asset)
```

### tool

**发布包打包**

```python
from pylucas.tool.release_packer import ReleasePacker

ReleasePacker(root=".").build()
```

支持 repignore 规则文件，格式与 .gitignore 相同（基于 pathspec）。

## 版本与许可证

- 当前版本：4.0.0
- 许可证：见 [LICENSE](LICENSE)
