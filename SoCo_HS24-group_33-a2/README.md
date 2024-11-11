# GROUP33 – Software Construction HS24 Task II
**Extend the Little German Language (LGL) interpreter by adding support for infix and boolean expressions, lexical scoping, and tracing**\
*By Ceyhun, Gianluca and Mischa*

## Table of Contents
- [Overview](#overview): Explanation and design decisions
- [Disclaimer](#disclaimer): Use of AI tools, Python requirements and commit distribution explanation
- [Code Documentation](#code-documentation): Detailed overview of each method

## Overview
This section outlines our general approach and the rationale behind key design decisions. For method-specific details, please refer to the [Code Documentation](#code-documentation).

#### LGL as A Tree Structure
We quickly realized that the Little German Language (LGL) can essentially be represented as a tree, with atomic expressions acting as leaves. Operations like `do_set`, `do_get`, `do_add`, and others serve as tree nodes, each with a specific (fixed for most, except `seq`) number of branches. Our `do` method manages this tree, determining which branches to append. `do` receives the entire LGL code and processes it in a depth-first manner, dividing and conquering the structure as it goes.

#### Infix Arithmetic and Boolean Operations
Since infix notation simply means that the operation identifier appears between operands, unlike prefix notation where the operation identifier appears first, we decided to convert infix instructions to prefix form before processing. The Boolean operations are structurally similar to the arithmetic operations already implemented, so adding them was trivial. For a detailed description of each operation, please refer to the [Code Documentation](#code-documentation).

#### Functions
To improve readability and understanding, we implemented a `Function` class to represent functions. Each `Function` object holds parameters, a body, and the current frame. The `do_function` method creates new functions, while `do_call` invokes the `call` method of the `Function` object. This, in turn, adds parameters as variables to the current frame and calls `do` on the current frame with the function body.

#### Lexical Scoping with Frames
Our implementation mimics Python's lexical scoping through a custom `Frame` class. The `do_set` method adds variables and functions to the current frame, while `do_get` retrieves them, checking the current frame first and then recursively searching parent frames if needed. Each time a new function is defined, a new frame is created with the current frame as its parent, allowing for **nested function definitions**. This modular approach also enables easy switching to dynamic scoping: simply open a new frame when calling functions instead of when defining them.

#### Tracing
We implemented tracing with a `Trace` class, utilizing a mix of object and class variables and methods. Each function that includes `@Trace.decorate` as a decorator logs its name, unique ID (a hash of the function name and definition timestamp), and precise start and end times to the class variable `call_stack`. Timing is measured using a combination of `datetime` and `perf_counter` to ensure maximum precision. Users can call `write` to generate a `.csv` file of the current call stack as needed.

#### Reporting
Reporting is divided into three parts. First, `parse_log` parses the `.csv` output from `Trace.write` into a dictionary. Next, `generate_function_stats` compiles statistics for each function (e.g., number of calls) and returns a new dictionary. Finally, `print_results` formats and displays the generated dictionary in the desired output format.

## Disclaimer
We aimed to distribute the workload as evenly as possible, and overall, this was successful. However, the commit count varies due to different committing habits. Additionally, [Dreamfarer](https://gitlab.uzh.ch/Dreamfarer) handled most of the merge requests, resulting in a higher number of commits on his part.

Please note that since our implementation uses `match` (the switch case of Python), Python >= 3.10 is **required** to run this code error-free.

ChatGPT was used as a tool to understand and learn concepts. However, all the code in this repository that extends the Little German Language (LGL) interpreter was authored exclusively by the three group members. ChatGPT contributed to writing docstrings and documentation, primarily for grammar correction and providing an outline.

## Code Documentation

...