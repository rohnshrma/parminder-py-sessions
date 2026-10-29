# labtools/analysis.py - CSV loading helpers that log problems instead of printing
import csv
import logging

# one logger per module; __name__ is "labtools.analysis", so log lines show where they came from
# it has no handlers of its own: main.py calls basicConfig once and decides where messages go
log = logging.getLogger(__name__)


def load_reading(path):            # path = CSV file to read; returns only the valid rows

    good = []                      # rows that converted cleanly
    with open(path , newline="") as f:     # newline="" is required for csv; 'with' auto-closes
        # DictReader makes each row a dict; start=2 because line 1 is the header
        for line_no , row in enumerate(csv.DictReader(f) , start=2):
            try :
                row["power_mw"] = float(row["power_mw"])   # text -> float (ValueError on 'ERR')
                row['channel'] = int(row['channel'])       # text -> int
                good.append(row)                           # reached only if both conversions worked
            except ValueError as e:
                # lazy %-style args: formatted only if the message is actually emitted
                log.warning("line %d skipped : %s", line_no , e)

    return good                    # caller gets the clean rows; bad ones are in the log
