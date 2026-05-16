class NotPresentError(Exception):
    pass


class AnyError(Exception):
    pass


def get_dir(dir: str) -> tuple[int, int]:
    nbrs = dir.split(",")
    height = int(nbrs[0])
    width = int(nbrs[1])
    return(height, width)


def is_present(keys: list, mand: str) -> None:
    if not mand in keys:
        raise NotPresentError(f"Need to add {mand} at config.txt")


def parse_bool(value:str) -> bool:
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"Invalid bool at config.txt: {value}")


def config_parser(f_name: str) -> list:
    try:
        f = open(f_name, "r")
    except FileNotFoundError as e:
        print(e)
        return

    #turn config.txt into a dictionary
    msg = f.read().split("\n")
    f.close()
    dic = {}

    for var in msg:
        if var[0] == "#":
            continue
        temp = var.split("=")
        dic.update({temp[0]: temp[1]})

    #check for mandatory keys
    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    keys = list(dic.keys())
    for mand in mandatory:
        try:
            is_present(keys, mand)
        except NotPresentError as e:
            print(e)
            raise AnyError("Error in parsing")
            return

    #check if valid values
    try:
        width = int(dic["WIDTH"])
        height = int(dic["HEIGHT"])
        entry = get_dir(dic["ENTRY"])
        exits = get_dir(dic["EXIT"])
        output_file = dic["OUTPUT_FILE"]
        perfect = parse_bool(dic["PERFECT"])
    except ValueError as e:
        print(e)
        raise AnyError("Error in parsing")
        return

    values = [width, height, entry, exits, output_file, perfect]
    ret = []
    for val in values:
        ret.append(val)
    return ret
