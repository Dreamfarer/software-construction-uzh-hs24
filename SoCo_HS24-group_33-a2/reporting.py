import sys
from datetime import datetime

def parse_log(log_file):
    data = {}
    with open(log_file, "r") as file:
        for line in file:
            if line.startswith("id"):
                continue
            id, timestamp,function_name,event = line.strip().split(",")
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            if id not in data:
                data[id] = {"function_name": None, "calls": 0, "start_time": None, "total_time": 0}
            if event == "start":
                data[id]["function_name"] = function_name
                data[id]["start_time"] = timestamp
                data[id]["calls"] += 1
            if event == "stop" and data[id]["start_time"] is not None:
                total_time = round((timestamp - data[id]["start_time"]).total_seconds() * 1000,3)
                data[id]["total_time"] = total_time
                data[id]["calls"] += 1
    return data

def print_logs(logs):
    pass

def main():
    assert len(sys.argv) == 2
    log_file = sys.argv[1]
    print(parse_log(log_file))
    print_logs(parse_log(log_file))


if __name__ == "__main__":
    main()
