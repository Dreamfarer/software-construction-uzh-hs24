["seq",
    ["set", "x", 200],
    ["set", "func1", ["function", [], ["set", "x", 10]]],
    ["set", "func2", ["function", [], ["seq", 
                                        ["set", "x", 20],
                                        ["set", "func3", ["function", [], ["seq",
                                                                            ["call", "func1"],
                                                                            ["get", "x"]
                                                                          ]]],
                                        ["call", "func3"]
                                      ]]],
    ["call", "func2"]
]