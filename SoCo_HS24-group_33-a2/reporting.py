import sys
from datetime import datetime

BLUE = "\033[36m"
RESET = "\033[0m"


def parse_log(log_file: str) -> dict:
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
            if event == "stop":
                elapsed_time = (timestamp - data[id]["start_time"]).total_seconds() * 1000
                data[id]["total_time"] = elapsed_time
    return data


def generate_function_stats(data: dict) -> dict:
    function_stats = {}
    for value in data.values():
        function_name = value["function_name"]
        calls = value["calls"]
        total_time = value["total_time"]
        if not function_name in function_stats:
            function_stats[function_name] = {"calls": calls, "total_time": total_time}
        else:
            function_stats[function_name]["calls"] += calls
            function_stats[function_name]["total_time"] += total_time
    return function_stats


def print_results(data: dict) -> None:
    print("\n")
    print(f"| {BLUE} Function Name  {RESET} |{BLUE} Num. of calls{RESET} | {BLUE} Total Time (ms) {RESET}| {BLUE}Average Time (ms) {RESET}|")
    print("|-------------------------------------------------------------------------|")

    function_stats = generate_function_stats(data)
    for function_name, stats in function_stats.items():
        calls = stats["calls"]
        total_time = stats["total_time"]
        average_time = total_time / calls
        total_time_formatted = f"{total_time:.3f}"
        average_time_formatted = f"{average_time:.3f}"
        print(f"|" + " " * 2 + function_name + " " * (16 - len(function_name)) +
               "|" + " " * 7 + str(calls) + " " * (8 - len(str(calls)))+
               "|" + " " * 7 + str(total_time_formatted) + " " * (11 - len(str(total_time_formatted)))+
               "|" + " " * 7  +  str(average_time_formatted) + " " * (12 - len(average_time_formatted)) +
               "|")
        
    print("|_________________________________________________________________________|")
    print("\n")


def main():
    assert len(sys.argv) == 2
    log_file = sys.argv[1]
    print_results(parse_log(log_file))


if __name__ == "__main__":
    main()
