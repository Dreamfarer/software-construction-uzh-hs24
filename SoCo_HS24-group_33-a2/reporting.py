from datetime import datetime
import sys

def parse_log(log_file):

    logs = {}
    with open(log_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if not line.startswith("id"):
                id, timestamp, fuction_name, event = line.split(",")
                if id in logs and event == "stop":
                    logs[id] = [fuction_name,timestamp,event]
                else:
                    logs[id] = [fuction_name,timestamp,event]

    return logs

def print_logs(logs):
    pass

def main():
    assert len(sys.argv) == 2
    log_file = sys.argv[1]
    print(parse_log(log_file))
    print_logs(parse_log(log_file))


if __name__ == "__main__":
    main()
