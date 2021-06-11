import pandas as pd
from scan import ScoringDailyScan
from run import run

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scoring = ScoringDailyScan()
    pd.set_option('display.max_columns', None, 'display.max_rows', None, 'display.width', 200)

    run(scoring, pd)

