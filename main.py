from datetime import datetime

import RecordAnalyze

now = datetime.now()

RecordAnalyze.Monthly(now.day-1, now.month, now.year).maxTemp_to_csv()
