import datetime as dt
import pytz


def convert_est_to_gmt_str(est_string: str) -> str:
    """
    Convert a datetime string in Eastern Standard Time (EST) to Greenwich Mean Time (GMT).

    Args:
        est_string (str): A datetime string in the format '%Y-%m-%dT%H:%M:%SZ'.

    Returns:
        str: A datetime string in the format '%Y-%m-%dT%H:%M:%SZ' converted to GMT.
    """
    # Create a timezone object for Eastern Standard Time (EST)
    est_timezone = pytz.timezone("EST")

    try:
        # Parse the input EST string into a datetime object
        est_time = dt.datetime.strptime(est_string, "%Y-%m-%dT%H:%M:%SZ")

        # Set the timezone of the parsed time to EST
        est_time = est_timezone.localize(est_time)

        # Convert EST time to GMT
        gmt_timezone = pytz.timezone("GMT")
        gmt_time = est_time.astimezone(gmt_timezone)

        # Convert GMT time to string with the specified format
        gmt_str = gmt_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return gmt_str
    except ValueError:
        return "Invalid input format. Please use the format '%Y-%m-%dT%H:%M:%SZ'."


def convert_gmt_to_est(gmt_string: str) -> str:
    """
    Convert a datetime string in Greenwich Mean Time (GMT) to Eastern Standard Time (EST).

    Args:
        gmt_string (str): A datetime string in the format '%Y-%m-%dT%H:%M:%SZ'.

    Returns:
        str: A datetime string in the format '%Y-%m-%dT%H:%M:%SZ' converted to EST.
    """
    # Define the format for the input string
    fmt = "%Y-%m-%dT%H:%M:%SZ"

    # Create a datetime object from the GMT string
    gmt_datetime = dt.datetime.strptime(gmt_string, fmt)

    # Define GMT and EST timezones
    gmt_tz = pytz.timezone("GMT")
    est_tz = pytz.timezone("EST")

    # Localize the datetime to GMT
    localized_gmt = gmt_tz.localize(gmt_datetime)

    # Convert the time to EST
    est_datetime = localized_gmt.astimezone(est_tz)

    # Return the EST datetime as a string in the same format
    return est_datetime.strftime(fmt)
