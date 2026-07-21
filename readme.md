# CatChecker Source (Leak)

Restored source code for CatChecker. This is not an official release. 

**Original Developer:** [No_S1gnalA12](https://t.me/No_S1gnalA12)

## What is this?
A Python/PySide6 GUI tool used to extract hardware and activation info from iOS devices via USB. It pulls parameters like UDID, IMEI, true storage capacity, and iOS build versions. 

## Stuff inside
* Fetches data using `usbmux` and `ideviceinfo` under the hood.
* Simple button to copy the entire log to clipboard.
* Dark/Light UI themes and ASCII art tabs.

## How to run
**Important:** Use Python 3.12. If you try running this on 3.13, pip will fail trying to build `lzfse` from source unless you have MSVC installed.

I recommend using `uv` for a clean install:

```bash
git clone https://github.com/KSN2redawew/CatChecker-SORCE-CODE.git
cd CatChecker-SORCE-CODE

# create env
uv venv --python 3.12 .venv
.venv\Scripts\activate

# install dependencies
uv pip install pymobiledevice3 PySide6

# run
python ksks.py
