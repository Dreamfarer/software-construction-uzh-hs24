["seq",
    ["set", "get_logical_and", ["function", ["x","y"], [["get","x"], "AND", ["get","y"]]]],
    ["set", "get_logical_xor", ["function", ["a","b"], [["get","a"], "XOR", ["get","b"]]]],
    ["set", "add_two", ["function", ["num1", "num2"], [["call", "get_logical_xor", ["get","num1"], 13], "+", ["call", "get_logical_and", 7, ["get","num2"]]]]],

    ["call", "add_two", 4, 1]
]