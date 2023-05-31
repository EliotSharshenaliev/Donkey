def time_converter(hour, minute):
    suffix = "AM" if hour < 12 else "PM"
    hour = hour if hour <= 12 else hour - 12
    return f"{hour:02d}:{minute:02d} {suffix}"