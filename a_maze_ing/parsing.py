import sys
import colors


class AnyError(Exception):
    pass


class NotPresentError(AnyError):
    pass


def get_dir(dir: str) -> tuple[int, int]:
    nbrs = dir.split(",")
    height = int(nbrs[0])
    width = int(nbrs[1])
    if height < 0 or width < 0:
        raise AnyError(f"{colors.RED}Negative coordinates")
    return (height, width)


def is_present(keys: list, mand: str) -> None:
    if mand not in keys:
        raise NotPresentError(f"{colors.RED}Need to add {mand} at config.txt")


def parse_bool(value: str) -> bool:
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"{colors.RED}Invalid bool at config.txt: {value}")


def config_parser(f_name: str) -> list:
    try:
        f = open(f_name, "r")
    except FileNotFoundError as e:
        print(f"{colors.RED}{e}")
        sys.exit(1)

    # turn config.txt into a dictionary
    msg = f.read().split("\n")
    f.close()
    dic = {}

    for var in msg:
        if var[0] == "#":
            continue
        try:
            temp = var.split("=")
            dic.update({temp[0]: temp[1]})
        except IndexError:
            print(f"{colors.RED}Invalid Configuration")
            sys.exit(1)

    # check for mandatory keys
    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    keys = list(dic.keys())
    for mand in mandatory:
        try:
            is_present(keys, mand)
        except NotPresentError as e:
            print(e)
            raise AnyError(f"{colors.RED}Mandatory key missing")
            return

    # check if valid values
    try:
        width = int(dic["WIDTH"])
        height = int(dic["HEIGHT"])
        entry = get_dir(dic["ENTRY"])
        exits = get_dir(dic["EXIT"])
        output_file = dic["OUTPUT_FILE"]
        perfect = parse_bool(dic["PERFECT"])
    except ValueError as e:
        print(e)
        raise AnyError(f"{colors.RED}Invalid Value")
        return

    if width < 2 or height < 2:
        raise AnyError(f"{colors.RED}Invalid Sizes")
    elif entry[0] >= width or entry[1] >= height:
        raise AnyError(f"{colors.RED}Invalid Entry")
    elif exits[0] >= width or exits[1] >= height:
        raise AnyError(f"{colors.RED}Invalid Exit")
    elif entry[0] == exits[0] and entry[1] == exits[1]:
        raise AnyError(f"{colors.RED}Invalid Entry/Exit")

    values = [width, height, entry, exits, output_file, perfect]
    ret = []
    for val in values:
        ret.append(val)
    return ret
