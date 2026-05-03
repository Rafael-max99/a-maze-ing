
def get_info():
    with open("config.txt", "r") as f:
        lines = f.readlines()
        
    for line in lines:
        print(line.strip())

if __name__ == "__main__":
    get_info()