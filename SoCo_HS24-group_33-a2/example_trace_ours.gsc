[
    "seq",
    ["set", "get_cube_power", ["function", "x", ["power", ["get", "x"], 3]]],
    ["set", "add_cubes", ["function", ["a", "b"], ["add", ["call", "get_cube_power", ["get", "a"]],  ["call", "get_cube_power", ["get", "b"]] ]]],
    ["call", "add_cubes", 3, 2]
]