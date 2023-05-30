# Battle Cats Mod Loader

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M53M4MN)

The Battle Cats Mod Loader (TBCML) is a tool for easily creating and managing mods for the mobile game The Battle Cats.

[![wakatime](https://wakatime.com/badge/user/ab1fc9e5-e285-49d1-8dc6-2f2e0198c8f6/project/0350bd63-7366-48f1-8a0d-72dab553a007.svg)](https://wakatime.com/badge/user/ab1fc9e5-e285-49d1-8dc6-2f2e0198c8f6/project/0350bd63-7366-48f1-8a0d-72dab553a007)

## Getting Started

### Installation

#### From pypi

```bash
pip install tbcml
```

#### From source

```bash
git clone https://github.com/fieryhenry/tbcml.git
cd tbcml
pip install -e .
```

## Basic Usage

Create `script.py`

```python
from tbcml.core import (
    CountryCode,
    GameVersion,
    Apk,
    GamePacks,
    Mod,
    Path,
    Dependency,
    ModEdit,
    ModManager,
)

# Choose the country code
cc = CountryCode.EN

# Choose a game version
gv = GameVersion.from_string("12.3.0")

# Apk Path (optional - defaults to home/tbcml/APKs or appdata/tbcml/APKs directory if not specified)
apk_folder = Path("apks")

# Get the apk
apk = Apk(gv, cc, apk_folder)
apk.download_apk()
apk.extract()

# Download server files data
apk.download_server_files()
apk.copy_server_files()

# Get the game data
game_packs = GamePacks.from_apk(apk)

# Create a mod id, or use an existing one
mod_id = Mod.create_mod_id()

# Create a mod, not all information is required
mod = Mod(
    name="Test Mod",
    author="Test Author",
    description="Test Description",
    mod_id=mod_id,
    mod_version="1.0.0",
    contributors=["fieryhenry"],
    dependencies=[Dependency(mod_id="JwxAbcSQIEZOqwZI", mod_version="1.0.0")],
)

# Make a mod edit to edit the basic cat's name to "Test Cat"
mod_edit = ModEdit(["cats", 0, "forms", 0, "name"], "Test Cat")

# Add the mod edit to the mod
mod.add_mod_edit(mod_edit)

# Add the mod to the mod manager
ModManager().add_mod(mod)

# Add the mod to the game packs
apk.load_mods([mod], game_packs)

# open the apk folder in the file explorer
apk_folder.open()
```

Run the script

```bash
python script.py
```
