from enum import Enum
import re


class ParsingError(Exception):
    pass


class TypeZone(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

    @classmethod
    def has_value(cls, value):
        return value in (item.value for item in cls)


class MetaData(Enum):
    ZONE = "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"
    MAX_LINK_CAPACITY = "max_link_capacity"

    @classmethod
    def has_value(cls, value):
        return value in (item.value for item in cls)

    @staticmethod
    def valid_color(color):
        return color in ["blue", "green",'crimson', 'yellow', 'red', 'cyan', 'white','black', 'rainbow','violet', 'maroon','darkred', 'purple', 'orange', 'gray', 'pink', 'magenta', 'lime', 'gold', 'brown']


class ConfigParser:
    def __init__(self, file: str) -> None:
        self.file = file
        self.required = {"nb_drones", "start_hub", "end_hub", "hub", "connection"}
        self.parse_key = set()
        self.config = {}
        self.hub_names = set()
        self.hub_coordinades = set()

    @staticmethod
    def clean_line(line: str) -> str | None:
        line = line.strip()
        if line == "":
            return None
        if line.startswith("#"):
            return None
        return line

    @staticmethod
    def split_metadata(line: str, conx: bool = False):
        match = re.search(r"\[(.*)$", line)
        if not match:
            return line.strip(), {}
        content = match.group(1)
        if "[" in content or content[-1] != "]":
            raise ParsingError("The metadata is invalid, must be for example: '[color=Red]'")
        rest = line.replace(match.group(0), "").strip()
        div_data = content.replace("]", "", 1).split()

        val_keys = ", ".join(item.value for item in MetaData if item != MetaData.MAX_LINK_CAPACITY)
        val_zone = ", ".join(item.value for item in TypeZone)
        metadata = {}
        for d in div_data:
            if "=" not in d:
                raise ParsingError("The metadata is invalid, must be for example: '[color=Red]'")
            key, value = (info.strip() for info in d.split("=", 1))
            if key in metadata:
                raise ParsingError("The metadata cannot has a repeated key!")
            if conx and key != MetaData.MAX_LINK_CAPACITY.value:
                raise ParsingError("The connection only can has 'max_link_capacity' metadata")
            if not MetaData.has_value(key):
                raise ParsingError(f"The Metadata key must be one of {val_keys}")

            if key == MetaData.COLOR.value:
                if not MetaData.valid_color(value):
                    raise ParsingError("Enter a valid color")
            elif key == MetaData.ZONE.value:
                if not TypeZone.has_value(value):
                    raise ParsingError(f"Enter a valid type zone: {val_zone}")
            elif key == MetaData.MAX_DRONES.value:
                val = int(value)
                if not val > 0:
                    raise ValueError 
                metadata[key] = val
                continue
            elif key == MetaData.MAX_LINK_CAPACITY.value:
                if not conx:
                    raise ParsingError("The metadata 'max_link_capacity' only can be in connections!")

            metadata[key] = value

        return rest, metadata

    def parse_line(self, line: str) -> None:
        try:
            hub = False
            if line.startswith("nb_drones"):
                key, value = line.split(":", 1)
                value = int(value)
                if value <= 0:
                    raise ValueError
                return value

            elif (line.startswith("start_hub")
                  or line.startswith("end_hub")
                  or line.startswith("hub")):
                if line.startswith("hub"):
                    hub = True
                key, line = line.split(":", 1)
                line, metadata = self.split_metadata(line.strip())
                line = line.split()
                if len(line) != 3 or key.strip() not in ("start_hub", "end_hub", "hub"):
                    raise ParsingError("The hub must follow the format of the example below\n"
                    "'hub: roof1 3 4 [zone=restricted color=red]'!")

                if "-" in line[0]:
                    raise ParsingError("The hub name cannot has '-' in name")
                if line[0] in self.hub_names:
                    raise ParsingError("Hubs cannot have repeated names.")
                self.hub_names.add(line[0].strip())
                cord = (int(line[1]), int(line[2]))
                if cord in self.hub_coordinades:
                    raise ParsingError("The hub coordinades must be differents!")
                self.hub_coordinades.add(cord)
                if hub:
                    return {line[0].strip(): {"X/Y": cord, "metadata": metadata}}
                return {"name": line[0].strip(), "X/Y": cord, "metadata": metadata}

            elif line.startswith("connection"):
                data = line.split(":", 1)[1].strip()
                data, metadata = self.split_metadata(data, True)
                hub_from, hub_to = (hub.strip() for hub in data.split("-", 1))
                if hub_from == hub_to:
                    raise ParsingError("The connection must to be made with differents hubs")
                if hub_from not in self.hub_names or hub_to not in self.hub_names:
                    raise ParsingError("The connections need to be made with existing hubs")
                return {"from": hub_from, "to": hub_to, "metadata": metadata}

        except ValueError:
            print(f"Error: The nb_drones, max_drones and limits_capacity value must be positive integers and X/Y coordinades integers!")
            exit(1)
        except ParsingError as e:
            print(f"Error: {e}")
            exit(1)


    def split_parse_line(self, line: str):
        line = line.strip()
        if not ":" in line:
            raise ValueError("Invalid configuration format!!\n"
                             "To nb_drones:\n"
                             "nb_drones: int\n"
                             "\nTo Any hub:\n"
                             "hub_key: hub_name X Y [metaconfig]\n"
                             "\nTo connections:\n"
                             "connection: hub_name-hub_name [metaconfig]"
                             "(optional)")

        if line.startswith("nb_drones"):
            if "nb_drones" in self.parse_key:
                raise ValueError("There can only be one nb_drones key in the file!")
            if self.config:
                raise ValueError("The nb_drones must to be the first line if config in the file!")
            key = line.split(":", 1)[0]
            self.parse_key.add(key.strip())
            self.config[key] = self.parse_line(line)

        elif line.startswith("start_hub") or line.startswith("end_hub"):
            key = line.split(":", 1)[0]
            if key.strip() in self.parse_key:
                raise ValueError(f"There can only be one {key.strip()} key in the file!")
            
            self.parse_key.add(key.strip())
            self.config[key] = self.parse_line(line)

        elif line.startswith("hub"):
            self.parse_key.add("hub")

            if not self.config.get("hub"):
                self.config["hub"] = []
            self.config["hub"].append(self.parse_line(line))

        elif line.startswith("connection"):
            if line.split(":", 1)[0].strip() != "connection":
                raise ParsingError("The key connection is wrong!")
            self.parse_key.add("connection")
            if not "-" in line:
                raise ParsingError("To make a connection you must put '-' between hub names")
            if not self.config.get("connection"):
                self.config["connection"] = []
            self.config["connection"].append(self.parse_line(line))

        else:
            raise ValueError(f"The file has a invalid key/value: '{line}'")
            

    def load_file(self):
        try:
            with open(self.file) as f:

                for line in f:
                    cleaned_line = self.clean_line(line)
                    if not cleaned_line:
                        continue
                    self.split_parse_line(line)
            if self.required != self.parse_key:
                raise ValueError(f"Insufficient keys, The program needs"
                                 f" the following keys: "
                                 f"{self.required - self.parse_key}")
            return self.config

        except PermissionError:
            print("Error: The file hasn't permission!")
            print(f"For executes the program enter: chmod +rx {self.file}")
            exit(1)
        except FileNotFoundError:
            print("Configuration file not found.")
            exit(1)
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
        except Exception as e:
            print(f"Error reading config: {e}")
            exit(1)
