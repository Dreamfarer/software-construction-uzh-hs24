import sys
import csv
from datetime import datetime, timedelta

BLUE = "\033[36m"
RESET = "\033[0m"


def parse_log(log_file: str) -> dict:
    """
    Parses a log file generated by the 'Trace.write' from 'lgl_interpreter' to extract function call data.

    Args:
        log_file (str): Path to the log file containing function call events.

    Returns:
        dict: A dictionary with the function name as key and another dictionary a the value containing the number of calls and the total time as keys.
    """
    with open(log_file, 'r') as file:
        rows = sorted(list(csv.reader(file))[1:], key=lambda x: x[0])
        functions = {}
        for i in range(0, len(rows), 2):
            name = rows[i][2]
            if name not in functions:
                functions[name] = {"calls": 0, "total_time": timedelta(0)}
            start = datetime.strptime(rows[i][1], "%Y-%m-%d %H:%M:%S.%f")
            stop = datetime.strptime(rows[i+1][1], "%Y-%m-%d %H:%M:%S.%f")
            functions[name]["calls"] += 1
            functions[name]["total_time"] += abs(stop - start)
    return functions


def print_results(data: dict) -> None:
    """
    Prints formatted function call statistics, including the name, the number of calls, total time,
    and average time per function.

    Args:
        data (dict): A dictionary with function call data parsed from the log file by 'parse_log'.
    """
    print("\n")
    print(f"| {BLUE} Function Name  {RESET} |{BLUE} Num. of calls{RESET} | {BLUE} Total Time (ms) {RESET}| {BLUE}Average Time (ms) {RESET}|")
    print("|-------------------------------------------------------------------------|")
    for function_name, stats in data.items():
        calls = stats["calls"]
        total_time = stats["total_time"].total_seconds() * 1000
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


def main() -> None:
    """
    Main entry point for reporting. Expects a log file as a command-line argument
    and outputs formatted function statistics to the console.
    """
    assert len(sys.argv) == 2
    log_file = sys.argv[1]
    print_results(parse_log(log_file))


if __name__ == "__main__":
    main()
