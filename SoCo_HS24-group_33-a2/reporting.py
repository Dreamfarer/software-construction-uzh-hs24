import sys
from datetime import datetime

def parse_log(log_file):
    time = {}
    with open(log_file, "r") as file:
        for line in file:
            if line.startswith("id"):
                continue
            id, timestamp,function_name,event = line.split(",")
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            if event == "start":
                time[id] = [function_name,timestamp]
            if event == "stop" and id in time:
                total_time = (timestamp - time[id][1]).total_seconds() * 1000
                time[id][1] = total_time
             
    return time

def print_logs(logs):
    pass

def main():
    assert len(sys.argv) == 2
    log_file = sys.argv[1]
    print(parse_log(log_file))
    print_logs(parse_log(log_file))


if __name__ == "__main__":
    main()
