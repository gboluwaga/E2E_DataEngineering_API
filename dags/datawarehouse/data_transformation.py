def parse_duration(duration_str):
    """Parse ISO 8601 duration string to total seconds."""
    import isodate
    duration_str = duration_str.replace("P","").replace("T","")
    
    isodate.parse_duration(duration_str)
    return int(duration.total_seconds())