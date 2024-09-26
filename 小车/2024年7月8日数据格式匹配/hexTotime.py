from datetime import datetime, timedelta

def convert_dotnet_ticks(ticks):
    """
    Converts .NET DateTime ticks to a UTC datetime object and a 13-digit Unix timestamp.
    
    Parameters:
    ticks (int): .NET DateTime ticks (100-nanosecond intervals since 0001-01-01 00:00:00)

    Returns:
    tuple: UTC datetime object, 13-digit Unix timestamp
    """
    # .NET DateTime ticks are 100-nanosecond intervals since 0001-01-01 00:00:00
    # 1 tick = 100 nanoseconds
    # 1 second = 10,000,000 ticks
    seconds = ticks / 10**7
    # Create a datetime object for the .NET start date
    dotnet_start_date = datetime(1, 1, 1)
    # Add the seconds to the start date
    utc_date = dotnet_start_date + timedelta(seconds=seconds)
    
    # Convert UTC datetime to Unix timestamp and then to 13-digit timestamp
    unix_timestamp = int(utc_date.timestamp() * 1000)
    
    return utc_date, unix_timestamp
def little_to_big_endian(hex_str):
    """
    Converts a little-endian hex string to a big-endian hex string.
    
    Parameters:
    hex_str (str): Little-endian hex string
    
    Returns:
    str: Big-endian hex string
    """
    # Remove any spaces and ensure the hex string length is even
    hex_str = hex_str.replace(" ", "")
    if len(hex_str) % 2 != 0:
        raise ValueError("Hex string must have an even length")
    
    # Convert little-endian to big-endian by reversing byte order
    big_endian_hex = ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))
    return big_endian_hex


# Example usage
ticks = 638557922380000000 

utc_date, unix_timestamp = convert_dotnet_ticks(ticks)
print(f"UTC Date: {utc_date}")
print(f"13-digit Unix Timestamp: {unix_timestamp}")
