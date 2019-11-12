## Getting Started
### Supported Platforms
`insta_hashtag_crawler` has been tested against the following platforms:
* __OS__ : Ubuntu 17.04 LTS, Windows 10
* __Python__ : cPython >= 3.6

### Installation
#### via `pip` (recommended)
* __When python 3 is the only python distribution installed on the system:__
```shell
pip install insta_hashtag_crawler
```
* __With multiple versions of python distributions:__  
  (replace `python3` with the version you want)
```shell
python3 -m pip install insta_hashtag_crawler
```
* __Using `venv`:__  
  + On Linux
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install insta_hashtag_crawler
```
  + On Windows
```cmd
python3 -m venv .venv
cd .venv/Scripts
activate
pip install insta_hashtag_crawler
```
#### via `setup.py`
```shell
git clone https://gitlab.com/point1304/insta_hashtag_crawler.git
cd insta_hashtag_crawler
python3 setup.py bdist
python3 setup.py install
```

### How to
`insta_hashtag_crawler` is shipped with a very simple command line tool  
and this is what you are going to mostly make the use of.

You can start crawling immediately on your `shell` with:
```shell
insta-crawl your-hashtag
```

This command will generates a series of `csv` formatted data in your  
"current working directory".
`csv` file name will be: __${hashtag}_yyyymmdd_(${number}).csv__

## Optional Arguments
* __[--dir] [-d]__  
You can set the directory where crawling results will be generated  
by using [--dir] [-d] option.  
The [--dir] options can take an absolute or relative path as an argument.
```shell
insta-crawl --dir /some/path/to/dir hashtag
insta-crawl --dir some/relative/path hashtag
```

* __[--quiet] [-q]__  
Turn on the [--quiet] [-q] flag if you want to mute the crawling logs,  
which by default are directed to the `stdout`.
This option will redirect any logs to OS-relevant `dev/null`.