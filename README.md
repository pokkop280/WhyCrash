# 🚀 WhyCrash
**WhyCrash** is a fully automatic AI assistant for error handling in Python. When your code crashes, WhyCrash intercepts the error, analyzes it using neural networks (OpenRouter + Minimax), gathers context from your local project files, and provides the cause along with an **AUTOMATIC CODE FIX**.

Did your code crash? The AI will explain why and automatically replace the broken file with the fixed one (if you allow it).

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Versions](https://img.shields.io/badge/python-3.8%2B-blue)

## ✨ Main Features
- 🧠 **Smart Traceback Analysis**: Understands not just the line with the error but also gathers imported local project files.
- 🛠️ **Auto-Fixing**: Proposes a ready-made fix and can rewrite the target Python files itself.
- 🎯 **Precise Control**: You decide where to catch errors: in the entire project, in a single function, or in a specific block of code.
- 🎨 **Beautiful Interface**: Uses the `rich` library for nice windows and terminal formatting.

---

## 📦 Installation

```bash
pip install WhyCrash
```
> *(Requires `requests`, `rich`, and `questionary` — they will install automatically)*

---

## 🛠️ How to Use

You have 4 ways to control which errors WhyCrash should catch. Choose the one that fits best!

### 1. Global Intercept (Easiest)
If you want **any** unhandled error in your program to be analyzed by the AI:

```python
import WhyCrash

# Enable error catching for the whole script
WhyCrash.debug()

# If the code crashes below, WhyCrash comes to the rescue!
print(1 / 0)
```

### 2. Dynamic Toggle (start & end)
If you have a large block of code and want to turn on smart analysis right before it, and turn it off right after:

```python
import WhyCrash

# ... normal code without WhyCrash ...

WhyCrash.start_debug()  # Turn on the interceptor

a = "text"
b = int(a)  # <-- This error will go to the AI!

WhyCrash.end_debug()    # Turn off the interceptor (returns to standard behavior)
```

### 3. Decorator for Specific Functions `@catch_errors`
If you are only concerned about the reliability of a specific function, you can wrap it in a decorator. If the function crashes, WhyCrash will trigger, while system errors outside of it remain untouched.

```python
from WhyCrash import catch_errors

@catch_errors
def my_danger_function():
    # If it breaks here — WhyCrash will trigger
    file = open("no_exist.txt", "r")

def normal_function():
    # And if it breaks here — standard Python traceback
    pass

my_danger_function()
```

### 4. Context Manager `with catch_block()`
For the most precise control, if you expect a failure in literally 2 specific lines of code:

```python
from WhyCrash import catch_block

print("Starting work...")
text = "100"

with catch_block():
    # Only code inside this block is monitored
    number = int(text)
    result = number / 0  # This will trigger an error sent to WhyCrash!

print("This code will not execute if there was an error above.")
```

---

## 🛑 How to Ignore Error Catching?
WhyCrash only analyzes **unhandled** exceptions. If you want an error in your code **not** to reach WhyCrash and the script to keep running, simply use a standard `try...except` block:

```python
import WhyCrash
WhyCrash.debug()

try:
    int("letter")
except ValueError:
    print("Error caught, it won't reach WhyCrash. Moving on!")
```

## ⚙️ Under the Hood
- **OpenRouter & Minimax** — Responsible for code analysis, "Reasoning," and generating fix files.
- **Traceback Walking** — The script automatically follows the error chain, finds all your `.py` files involved, reads them, and sends them to the AI as context.
- **Rich** — Beautiful console UI (colors, panels, Markdown formatting).

---

Made with ❤️ to save developers' nerves!

---
🌍 **Languages:** [Русский](docs/README_ru.md) | [Deutsch](docs/README_de.md)
