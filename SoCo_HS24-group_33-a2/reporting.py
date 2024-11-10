import sys
from datetime import datetime

BLUE = "\033[36m"
RESET = "\033[0m"


def parse_log(log_file) -> dict:
    data = {}
    with open(log_file, "r") as file:
        for line in file:
            if line.startswith("id"):
                continue
            id, timestamp, function_name, event = line.strip().split(",")
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            if id not in data:
                data[id] = {
                    "function_name": None,
                    "calls": 0,
                    "start_time": None,
                    "total_time": 0,
                }
            if event == "start":
                data[id]["function_name"] = function_name
                data[id]["start_time"] = timestamp
                data[id]["calls"] += 1
            if event == "stop" and data[id]["start_time"] is not None:
                elapsed_time = round((timestamp - data[id]["start_time"]).total_seconds() * 1000, 3)
                elapsed_time = "{:.3f}".format(elapsed_time)
                data[id]["total_time"] = elapsed_time
                data[id]["calls"] += 1
    return data


def print_results(data: dict) -> None:
    print("\n")
    print(f"| {BLUE} Function Name  {RESET} |{BLUE} Num. of calls{RESET} | {BLUE} Total Time (ms) {RESET}| {BLUE}Average Time (ms) {RESET}|")
    print("|-------------------------------------------------------------------------|")
    for value in data.values():
        name = value["function_name"]
        calls = value["calls"]
        total_time = value["total_time"]
        average_time = round(float(total_time) / calls, 3)
        average_time = "{:.3f}".format(average_time)

        print(f"|" + " " * 2 + name + " " * (16 - len(name)) +
               "|" + " " * 7 + str(calls) + " " * (8 - len(str(calls)))+
               "|" + " " * 7 + str(total_time) + " " * (11 - len(str(total_time)))+
               "|" + " " * 7  +  str(average_time) + " " * (12 - len(average_time)) +
               "|")
    print("|_________________________________________________________________________|")
    print("\n")


def main():
    assert len(sys.argv) == 2
    log_file = sys.argv[1]
    parse_log(log_file)
    print_results(parse_log(log_file))


if __name__ == "__main__":
    main()
