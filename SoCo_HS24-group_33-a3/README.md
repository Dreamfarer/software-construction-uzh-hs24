# Challenges Translating Python to Java

Since our Python code was already quite object-oriented, translating it to Java wasn’t straightforward and we faced some key challenges.

- Imports and Libraries:
In our Python version we used built-in modules like difflib for our Tig.diff method. However, Java does not have an equivalent for difflib. To resolve this we had to use an external library but the implementation was quite challenging compared to Python were we basically write pip install module_name.

- Error Handling:
Java’s strict error handling required more work compared to Python, where you can often skip it until needed. Therefore, we faced some issues, when we did not handle errors.

- Json Handling:
Since Java lacks a built-in JSON handling library compared to Python, we had to put in extra effort when implementing JSON-related methods because we did not use a third-party library.

- AI Usage:
Regarding the AI usage, we used it to look at the translation from Python to Java. A big challenge we faced was that although the AI was mostly correct, it made mistakes that we had to fix because it did not know the rest of our code and the exact task description but it helped us getting a thorough understanding of Java and its built-in modules.


