from typing import Optional
from tbcml import core


class ModManager:
    def __init__(self):
        self.__mods: Optional[dict[str, core.Mod]] = None
        self.mod_folder = core.Path(core.Config().get(core.ConfigKey.MOD_FOLDER))
        self.mod_folder.generate_dirs()
        self.mod_info_json = self.mod_folder.add("mod_info.json")
        self.load_mod_json()

    @property
    def mods(self) -> dict[str, "core.Mod"]:
        if self.__mods is not None:
            return self.__mods
        mods: dict[str, core.Mod] = {}
        for path in self.mod_folder.get_files():
            if path.get_extension() != "bcmod":
                continue
            mod = core.Mod.load(path)
            if mod is not None:
                mods[mod.get_file_name()] = mod
        self.__mods = mods
        return mods

    @mods.setter
    def mods(self, mods: dict[str, "core.Mod"]):
        self.__mods = mods

    def load_mod_json(self):
        if self.mod_info_json.exists():
            self.json_file = core.JsonFile.from_path(self.mod_info_json)
        else:
            self.init_new_json()
            self.save_mod_json()

    def init_new_json(self):
        self.json_file = core.JsonFile.from_object({"mods": {}})

    def save_mod_json(self):
        self.json_file.save(self.mod_info_json)

    def enable_mod(self, mod: "core.Mod"):
        self.save_mod(mod)
        self.json_file.get_json()["mods"][mod.get_file_name()] = True
        self.save_mod_json()

    def disable_mod(self, mod: "core.Mod"):
        self.save_mod(mod)
        self.json_file.get_json()["mods"][mod.get_file_name()] = False
        self.save_mod_json()

    def is_mod_enabled(self, mod: "core.Mod") -> bool:
        if mod.get_file_name() not in self.json_file.get_json()["mods"]:
            return True
        return self.json_file.get_json()["mods"][mod.get_file_name()]

    def get_enabled_mods(self) -> list["core.Mod"]:
        return [mod for mod in self.mods.values() if self.is_mod_enabled(mod)]

    def get_disabled_mods(self) -> list["core.Mod"]:
        return [mod for mod in self.mods.values() if not self.is_mod_enabled(mod)]

    def increase_priority(self, mod: "core.Mod"):
        if mod.get_file_name() not in self.json_file.get_json()["mods"]:
            return
        self.json_file.get_json()["mods"].insert(
            0,
            mod.get_file_name(),
            self.json_file.get_json()["mods"].pop(mod.get_file_name()),
        )
        self.save_mod_json()

    def decrease_priority(self, mod: "core.Mod"):
        if mod.get_file_name() not in self.json_file.get_json()["mods"]:
            return
        self.json_file.get_json()["mods"].append(
            mod.get_file_name(),
            self.json_file.get_json()["mods"].pop(mod.get_file_name()),
        )
        self.save_mod_json()

    def get_mods(self) -> list["core.Mod"]:
        return list(self.mods.values())

    def get_mod(self, id: str) -> Optional["core.Mod"]:
        if not id.endswith(".bcmod"):
            id = id + ".bcmod"
        return self.mods.get(id)

    def get_mod_by_full_name(self, full_name: str) -> Optional["core.Mod"]:
        for mod in self.mods.values():
            if mod.get_full_mod_name() == full_name:
                return mod
        return None

    def add_mod(self, mod: "core.Mod"):
        self.mods[mod.get_file_name()] = mod
        self.save_mod(mod)
        self.json_file.get_json()["mods"][mod.get_file_name()] = True
        self.save_mod_json()

    def save_mod(self, mod: "core.Mod"):
        self.mods[mod.get_file_name()] = mod
        mod.save(self.mod_folder.add(mod.get_file_name()))
        self.save_mod_json()

    def remove_mod(self, mod: "core.Mod"):
        try:
            self.mods.pop(mod.get_file_name())
        except KeyError:
            pass
        self.mod_folder.add(mod.get_file_name()).remove()
        try:
            self.json_file.get_json()["mods"].pop(mod.get_file_name())
        except KeyError:
            pass
        self.save_mod_json()

    def get_mod_folder(self) -> "core.Path":
        return self.mod_folder

    def save_mods(self):
        for mod in self.mods.values():
            self.save_mod(mod)

    def get_mod_path(self, mod: "core.Mod") -> "core.Path":
        return self.mod_folder.add(mod.get_file_name())

    def regenerate_mod_json(self):
        self.init_new_json()
        for mod in self.mods.values():
            self.json_file.get_json()["mods"][mod.get_file_name()] = True
        self.save_mod_json()
