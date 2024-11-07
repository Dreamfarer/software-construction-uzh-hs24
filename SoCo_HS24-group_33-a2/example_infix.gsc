["seq",
    ["set", "add_two", ["function", ["a","b"], [["get","a"],"add",["get","b"]]]],
    ["set", "substract_two", ["function", ["a","b"], [["get","a"], "substract", ["get","b"]]]],
    ["set", "multiply_two", ["function", ["a","b"], [["get","a"], "multiply", ["get","b"]]]],
    ["set", "divide_two", ["function", ["a","b"], [["get","a"], "divide", ["get","b"]]]],
    ["set", "power_two", ["function", ["a","b"], [["get","a"], "power", ["get","b"]]]],
    ["set", "logical_and", ["function", ["a","b"], [["get","a"], "AND", ["get","b"]]]],
    ["set", "logical_or", ["function", ["a","b"], [["get","a"], "OR", ["get","b"]]]],
    ["set", "logical_xor", ["function", ["a","b"], [["get","a"], "XOR", ["get","b"]]]],

    ["call", "add_two",3,2],
    ["call", "substract_two",4,1],
    ["call", "multiply_two",5,8],
    ["call", "divide_two",9,3],
    ["call", "logical_and",12,0],
    ["call", "logical_or",4,7],
    ["call", "logical_xor",0,0]
]