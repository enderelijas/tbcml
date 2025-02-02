# TBCML

The Battle Cats Modding Library (TBCML) is a python library designed to make
modding The Battle Cats easier, more automated, and more powerful.

Because the package is a library and you will need to have
programming experience if you want to use it effectively.

Most features are not documented yet and many may not work properly atm.

## Credits

- EasyMoneko for the original keys for decrypting/encrypting:
  <https://www.reddit.com/r/battlecats/comments/41e4l1/is_there_anyone_able_to_access_bc_files_your_help/>
- Battle Cats Ultimate for what some of the numbers mean in various csvs,
  helping me to figure out animation rendering, and for providing the empty form
  icons:  <https://github.com/battlecatsultimate>
- This resource for unit csvs: <https://pastebin.com/JrCTPnUV>
- Vi for enemy csvs

## Functionality

Note that most of these features a work in progress and may not work properly.

- Downloading and extracting apks
- Downloading server files and event data
- Decryption and encryption of pack files
- Parsing of various game data files
- Modification of game data
- Frida gadget hooking
- Smali code injection
- Java to smali code conversion
- Patching of libnative-lib.so file
- Modification of apk assets
- Animation Viewer / Loader
- BCU Pack Imports
- Repacking and signing of modified apks
- Randomization of encryption keys so that your pack files cannot be easily
  decrypted by other people

Note that the scripting functionality is very limited, especially in later
game versions. Once I finish the [game
decompilation](https://github.com/fieryhenry/battlecats) I will be able to
make a much more powerful modding api.

Discord: <https://discord.gg/DvmMgvn5ZB> (The server is the same one which is
used for save editing as I haven't made a modding specific one
yet)

I've spent so much time working on this project because I've changed my mind on
what this tool should do and how to structure it, but due to all of the
re-writes, it really doesn't look like it. So I would really appricate it if you
considered donating to my kofi:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/fieryhenry)

[![wakatime](https://wakatime.com/badge/user/ab1fc9e5-e285-49d1-8dc6-2f2e0198c8f6/project/0350bd63-7366-48f1-8a0d-72dab553a007.svg)](https://wakatime.com/badge/user/ab1fc9e5-e285-49d1-8dc6-2f2e0198c8f6/project/0350bd63-7366-48f1-8a0d-72dab553a007)

## Getting Started

### Installation

To install on android see [Install on Android](#install-on-android)

#### From pypi

```bash
pip install tbcml
```

If you want scripting (frida or smali patching or libnative patching), you will
also need to install tbcml[scripting]

```bash
pip install tbcml[scripting]
```

If you want to use the model viewer, you will also need to install
tbcml[ui]

```bash
pip install tbcml[ui]
```

#### From source

```bash
git clone https://github.com/fieryhenry/tbcml.git
cd tbcml
pip install -r requirements_scripting.txt
pip install -r requirements_ui.txt
pip install -e .
```

You don't need to install the requirements if you don't want to use the
scripting or ui features.

### Basic Usage

You can obviously do more advanced things with this tool, but this is just a
basic example of how to use it.

I don't have time to create a bunch of examples and the documentation is not
finished, so you'll probably have to read the source code to figure out how to
do more advanced things.

Create `script.py`

```python
from tbcml.core import (
    CountryCode,
    GameVersion,
    Apk,
    GamePacks,
    Mod,
    ModEdit,
    CatFormType,
    Cat,
    CatForm,
)

# Choose the country code
cc = CountryCode.EN

# Choose a game version
gv = GameVersion.from_string("12.3.0")

# Get the apk
apk = Apk(gv, cc)
apk.download()
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
    password="test",
)

# Define cat information
cat_id = 0
cat_form_type = CatFormType.FIRST

# Create a form with the name "Test Cat"
form = CatForm(cat_id, cat_form_type, name="Test Cat")

# Create a cat
cat = Cat(cat_id)

# Set the form
cat.set_form(cat_form_type, form)

# Create a mod edit
mod_edit = ModEdit(["cats", cat_id], cat.to_dict())

# Add the mod edit to the mod
mod.add_mod_edit(mod_edit)

# Add the mod to the game packs
apk.load_mods([mod], game_packs)

# open the apk folder in the file explorer (optional)
apk.output_path.open()

```

If you want to do some script modding, you will also need to set
`allowed_script_mods` to `True` when creating the apk object

```python

apk = Apk(gv, cc, allowed_script_mods=True)

```

Run the script

Windows

```bash
py script.py
```

Everything else

```bash
python3 script.py
```

## Install on Android

### Requirements

- Termux (via [F-Droid](https://f-droid.org/en/packages/com.termux/)) You cannot
  use the play store version as it doesn't work
- Make sure you download "Termux Terminal emulator with packages"
- Then run the following commands:
  
  ```bash
  termux-setup-storage
  termux-change-repo
  ```

  When prompted for a mirror, any of them should work, but I picked "GH Mirrors
  by Kcubeterm"

  Then run the following commands:

  ```bash
  pkg install python
  pkg install binutils
  pkg install rust
  pkg install openjdk-17
  pkg install aapt
  pkg install apksigner
  ```

  rust and binutils are needed to build the cryptography package btw, the tool
  is not written in it.

  You can then install the tool from pypi [here](#from-pypi), or
  install the tool from
  source (need to do `pkg install git`) [here](#from-source)

  I recommend adding
  
  ```python
  print(apk.get_final_apk_path())
  ```

  to the end of your script so that you can easily find the apk. Then you can
  copy the file to the Documents folder with the following
  command:

  ```bash
  cp path/to/apk /sdcard/Documents
  ```

  Then you can install it with a file manager.

## Documentation (Not Finished)

For examples see the [examples](examples) folder. Note that some may need the
latest commit to work (see [install from source](#from-source))

<https://tbcml-docs.readthedocs.io/en/latest/>
