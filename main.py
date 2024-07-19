from datetime import datetime

import RecordAnalyze

now = datetime.now()

RecordAnalyze.Monthly(now.day, now.month, now.year).maxTemp_to_csv()
