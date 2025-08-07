from datetime import datetime, timedelta

def predict_next_period(last_date, cycle_length):
    date_obj = datetime.strptime(last_date, "%Y-%m-%d")
    next_date = date_obj + timedelta(days=cycle_length)
    return next_date.strftime("%Y-%m-%d")
