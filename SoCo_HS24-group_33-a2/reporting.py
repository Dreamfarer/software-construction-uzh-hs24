import sys
from datetime import datetime

def parse_log(log_file):
    time = {}
    with open(log_file, "r") as file:
        for line in file:
            if line.startswith("id"):
                continue
            id, timestamp,function_name,event = line.strip().split(",")
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            if id not in time:
                time[id] = [0]
            if event == "start" and id in time:
                time[id].append(function_name)
                time[id].append(timestamp)
                time[id][0] += 1
            if event == "stop" and id in time:
                total_time = round((timestamp - time[id][2]).total_seconds() * 1000,3)
                time[id][2] = total_time
                time[id][0] += 1 
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
