import re


def format_date_year_first(date): # 1
    """Takes in a date of the format MM/DD/YYYY and returns it in YYYY/MM/DD
    for things like sorting by date

    Args:
        date (str): date input, must be MM/DD/YYYY

    Returns:
        String: date output in YYYY/MM/DD
    """
    if not re.search(r'^\d\d\/\d\d\/\d\d\d\d$', date):
        return ' [Err] - format_date_year_first() -> date isn\'t in the MM/DD/YYYY format'

    year = date[6:]
    month = date[:2]
    day = date[3:5]
    
    return year+'/'+month+'/'+day
    
    
def format_date_month_first(date): # 2
    """Takes in a date of the format YYYY/MM/DD and returns it in MM/DD/YYYY

    Args:
        date (str): date input, must be YYYY/MM/DD

    Returns:
        String: date output in MM/DD/YYYY
    """
    if not re.search(r'^\d\d\d\d\/\d\d\/\d\d$', date):
        return ' [Err] - format_date_month_first() -> date isn\'t in the YYYY/MM/DD format'
    
    year = date[:4]
    month = date[5:7]
    day = date[8:]
    
    return month+'/'+day+'/'+year
    

if __name__ == '__main__':
    func = int(input('Which function would you like to run? 1 = format_date_year_first and 2 = format_date_month_first: '))
    
    match func:
        case 1:
            date = input('Enter date to format (MM/DD/YYYY): ')
            print(format_date_year_first(date))
        case 2:
            date = input('Enter date to format (YYYY/MM/DD): ')
            print(format_date_month_first(date))