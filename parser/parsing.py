from enum import Enum
import re
#pygame

class ParsingError(Exception):
    pass


class Types(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

class ConfigParser:
    def __init__(self, file: str) -> None:
        self.file = file
        self.required = {"nb_drones", "start_hub", "end_hub", "hub", "connection"}
        self.parse_key = set()
        self.config = {}
        self.hub_names = []

    @staticmethod
    def clean_line(line: str) -> str | None:
        line = line.strip()
        if line == "":
            return None
        if line.startswith("#"):
            return None
        return line

    @staticmethod
    def split_metadata(line):
        
        match = re.search(r"\[(.*)\]", line)
        if not match:
            return line.strip(), {}
        content  = match.group(1)
        if "[" in content or "]" in content:
            raise ParsingError("The metadata is invalid, must be for example: '[color= Red]'")
        rest = line.replace(match.group(0), "").strip()
        metadata = {}
        div_data = content.split()
        for d in div_data:
            key, value = d.split("=")
            if value.isdigit():
                value = int(value)
            metadata[key] = value
        return rest, metadata
            



    def parse_line(self, line: str) -> None:
        try:
            hub = False
            if line.startswith("nb_drones"):
                _, value = line.split(":", 1)
                value = int(value)
                if value <= 0:
                    raise ValueError
                return value

            elif line.startswith("start_hub") or line.startswith("end_hub") or line.startswith("hub"):
                if line.startswith("hub"):
                    hub = True
                line = line.split(":", 1)[1]
                line, metadata = self.split_metadata(line.strip())
                line = line.split()
                if len(line) != 3:
                    raise ParsingError("The hub must follow the format of the example below\n"
                    "'hub: roof1 3 4 [zone=restricted color=red]'!")
                if hub:
                    return {line[0]: {"X": int(line[1]), "Y": int(line[2]), "metadata": metadata}}
                return {"name": line[0], "X": int(line[1]), "Y": int(line[2]), "metadata": metadata}

        except ValueError:
            print(f"Error: The nb_drones, X/Y coordinades value must be a positive integer!")
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
            self.parse_key.add("nb_drones")
            key, value = line.split(":")
            self.config[key] = self.parse_line(line)

        elif line.startswith("start_hub") or line.startswith("end_hub"):
            key, value = line.split(":", 1)
            if key.strip() in self.parse_key:
                raise ValueError(f"There can only be one {key.strip()} key in the file!")
            
            self.parse_key.add(key.strip())
            self.config[key] = self.parse_line(line)

        elif line.startswith("hub"):
            self.parse_key.add("hub")
            data = line[5:].split()

            if not self.config.get("hub"):
                self.config["hub"] = []
            self.config["hub"].append(self.parse_line(line))

        elif line.startswith("connection"):
            self.parse_key.add("connection")
            data = line.split(":")[1].strip()
            data = data.split("-")
            atrb = None
            self.parse_line(line)
            if len(data[1].split()) > 1:
                atrb = data[1].split()[1]
                data[1] = data[1].split()[0]
            if not self.config.get("connection"):
                self.config["connection"] = []
            self.config["connection"].append({"from": data[0], "to": data[1], "atrb": atrb})

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
            print(f"For executes the program enter: chmod +r {self.file}")
            exit(1)
        except FileNotFoundError:
            print("Configuration file not found.")
            exit(1)
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
        #except Exception as e:
        #    print(f"Error reading config: {e}")
        #    exit(1)




    def parse(self) -> dict:
       info = self.load_file()
       return info



