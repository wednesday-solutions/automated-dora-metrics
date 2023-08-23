import datetime

def get_current_date():
    utc_now = datetime.datetime.utcnow()
    # Calculate the time difference between UTC and IST (5 hours and 30 minutes)
    ist_offset = datetime.timedelta(hours=5, minutes=30)
    # Convert UTC time to IST by adding the offset
    ist_now = utc_now + ist_offset    
    formatted_date = ist_now.strftime("%d-%m-%Y %I:%M %p")
    return formatted_date
