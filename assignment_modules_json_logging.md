# Practical Assignment: Modules, Packages, JSON and Logging

Covers only today's session: `calculator.py` / `main.py` (modules and imports), the `labtools` package, JSON config files and the `logging` module.

Use `DATA/readings.csv` (timestamp, instrument, channel, power_mw, temp_c) as sample data.

## Part A: Modules and imports

1. **Unit converter module:** Create `converter.py` with `c_to_f(c)` and `km_to_miles(km)`. In a separate `app.py`, import both with `from converter import ...` and print one example of each.
2. **Extend calculator:** Add `subtraction(a, b)` and `calcArea(radius)` to `calculator.py`, then call them from `main.py`.
3. **Import styles:** In one file use `import calculator` (call as `calculator.addition(...)`), and in another use `from calculator import addition as add`. Print the same result both ways.

## Part B: Packages

4. **Build a package:** Create `bench_tool/labtools/` with an empty `__init__.py`. Add `instruments.py` containing a `PowerMeter` class with `connect()` and `disconnect()`.
5. **Use the package:** In `bench_tool/main.py` import `PowerMeter` with `from labtools.instruments import PowerMeter`, create one on port `"COM3"`, then connect and disconnect.
6. **Second instrument:** Add a `TempSensor` class to `instruments.py` with a `read()` method that returns a fixed value. Use both classes in `main.py`.

## Part C: JSON configuration

7. **Write a config:** Build a dict with `station`, `instrument` (model, port, timeout_s), `channels`, `limits` (power_mw_min, power_mw_max) and `save_raw`. Save it to `config.json` with `json.dump` and `indent=2`.
8. **Read a config:** Load `config.json` with `json.load` and print the port and both limits using chained keys.
9. **Pass / Fail report:** Using the limits from the config, print `time channel power Pass/Fail` for every good row of `readings.csv`.
10. **Type check:** Dump a dict containing `True`, `None` and a tuple, then read the file as text and write a comment listing how each became JSON.

## Part D: Logging

11. **Levels:** Configure `logging.basicConfig` with level `INFO` and the format `%(asctime)s %(levelname)-8s %(message)s`. Log one message at each of DEBUG, INFO, WARNING and ERROR, and note which one does not appear.
12. **Log to file and screen:** Add a `FileHandler("run.log")` and a `StreamHandler()` so every message goes to both. Check that `run.log` has the lines.
13. **Log an exception:** Wrap `float("ERR")` in try/except and use `logging.exception`. Explain in a comment what extra information it adds compared to `logging.error`.

## Part E: Putting it together

14. **Analysis module:** Create `labtools/analysis.py` with `load_reading(path)`. Use `log = logging.getLogger(__name__)` and `log.warning("line %d skipped : %s", line_no, e)` for every row that fails conversion; return the good rows.
15. **Final run:** In `bench_tool/main.py` call `basicConfig` once, load the config and `readings.csv` through `load_reading`, and log how many rows passed and failed against the config limits.
