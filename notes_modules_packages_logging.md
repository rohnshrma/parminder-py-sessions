# Modules, Packages and Logging - Notes

Everything here is based on what we covered: `calculator.py` + `main.py` (modules) and the `bench_tool` project (package + logging).

---

## 1. Modules

A **module** is simply a `.py` file. Whatever you define in it (functions, classes, variables) can be reused in another file.

```python
# calculator.py
def addition(a, b):
    return a + b
```

```python
# main.py
from calculator import addition, calcBmi

print(addition(23, 34))      # 57
```

Points to remember:

- Import using the file name **without** `.py` (`calculator`, not `calculator.py`).
- Both files should be in the same folder, so Python can find the module.
- Two ways to import:
  - `import calculator` -> use as `calculator.addition(1, 2)`
  - `from calculator import addition` -> use directly as `addition(1, 2)`
- Importing a module runs its top-level code once. Python also creates a `__pycache__` folder with compiled `.pyc` files. That is normal, no need to touch it.

### `if __name__ == "__main__":`

Python sets `__name__` for every file.

- Run the file directly -> `__name__` is `"__main__"`, so the block runs.
- Import the file from somewhere else -> `__name__` is the module name, so the block is skipped.

```python
if __name__ == "__main__":
    print(load_reading("readings.csv")[:2])   # quick self-test, runs only when file is run directly
```

---

## 2. Packages

A **package** is a **folder of modules** that contains an `__init__.py` file. The file can be empty; its presence tells Python "this folder is importable".

Our structure:

```
bench_tool/
├── main.py              # entry point
├── config.json          # settings
├── readings.csv         # data
└── labtools/            # the package
    ├── __init__.py      # empty, marks the folder as a package
    ├── instruments.py   # PowerMeter class
    └── analysis.py      # load_reading, check_limit
```

Importing from a package uses dots: `package.module`.

```python
from labtools.instruments import PowerMeter
from labtools.analysis import load_reading, check_limit
```

Points to remember:

- Run `main.py` from inside `bench_tool`, so that `labtools` and `config.json` are found.
- Why split into modules? Each file has one job (instrument code, analysis code, wiring in `main.py`). It is easier to read, test and reuse.

### The class in `instruments.py`

```python
class PowerMeter:
    def __init__(self, port):     # constructor, runs when PowerMeter("COM3") is created
        self.port = port          # data stored on the object

    def connect(self):
        print(f"connected to {self.port}")
```

`self` is the object itself, so every method can reach its data like `self.port`.

---

## 3. JSON config (used by `main.py`)

Settings live in `config.json`, not inside the code. To change the port or limits, we only edit the JSON.

```python
import json
with open("config.json") as f:
    cfg = json.load(f)                  # JSON object -> python dict

cfg["instrument"]["port"]               # "COM3"
cfg["limits"]["power_mw_min"]           # 8.0
```

- `json.load(f)` reads from a file. `json.loads(text)` reads from a string.
- JSON `{}` becomes a dict, `[]` becomes a list. Nested objects become nested dicts.
- JSON does not allow comments.

---

## 4. Logging

`print()` is fine for quick checks, but real programs use the **logging** module. It gives severity levels, a format, and the freedom to send output to the console or a file, without changing the code that writes the messages.

### Levels (low to high)

| Level      | When to use                                  |
|------------|----------------------------------------------|
| `DEBUG`    | Detailed info for developers                 |
| `INFO`     | Normal progress ("5 passed, 1 failed")       |
| `WARNING`  | Something is off but the program continues   |
| `ERROR`    | A task failed                                |
| `CRITICAL` | Whole program may not continue               |

If you set `level=INFO`, then INFO and everything above it is shown. DEBUG is hidden.

### Two parts: configure once, log everywhere

**(a) Configure once, in the entry point (`main.py`):**

```python
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s %(name)s : %(message)s")
```

- `level` -> minimum severity to show.
- `format` -> shape of each line. `%(levelname)s` is the level, `%(name)s` is the logger name, `%(message)s` is your text.
- Call it **once**, at the top level, before anything is logged.

**(b) Log in each module, with its own logger (`analysis.py`):**

```python
import logging
log = logging.getLogger(__name__)      # name becomes "labtools.analysis"

log.warning("line %d skipped : %s", line_no, e)
```

- `__name__` inside `analysis.py` is `"labtools.analysis"`, so every log line tells you which module it came from.
- Modules do **not** configure logging. They only create a logger and use it. `main.py` decides where and how messages appear.

### Lazy `%` formatting

```python
log.warning("line %d skipped : %s", line_no, e)     # good
log.warning(f"line {line_no} skipped : {e}")        # works, but formats even if message is not shown
```

Arguments are given separately, and logging builds the string only if that level is actually going to be emitted.

### Example output

```
WARNING labtools.analysis : line 4 skipped : could not convert string to float: 'ERR'
INFO root : 5 passed, 1 failed
```

`root` appears because `main.py` called `logging.info(...)` directly, which uses the root logger.

### Logging to a file

Add `filename` to `basicConfig` and the messages go to that file instead of the console (this is how `run.log` gets created):

```python
logging.basicConfig(filename="run.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s : %(message)s")
```

`%(asctime)s` adds the time of each message.

---

## 5. Putting it together: flow of `bench_tool`

1. `main.py` sets up logging, then reads `config.json`.
2. It creates `PowerMeter("COM3")` and calls `connect()`.
3. `load_reading("readings.csv")` reads the CSV with `csv.DictReader`, converts `power_mw` to float and `channel` to int. A bad row (like `ERR`) raises `ValueError`, which is caught and logged as a **warning**; the row is skipped and the program carries on.
4. `finally` makes sure `disconnect()` runs even if loading crashes.
5. `check_limit(rows, lo, hi)` counts rows with `lo <= power_mw <= hi` and returns `(passed, failed)`.
6. `main.py` logs the result at **INFO** level.

### Handy patterns used here

- `try / except ValueError` -> handle a known problem and continue.
- `try / finally` -> cleanup code that must always run.
- `with open(...) as f` -> file closes automatically.
- `enumerate(..., start=2)` -> line numbers for the log (line 1 is the CSV header).
- `passed, failed = check_limit(...)` -> unpacking a returned tuple.
