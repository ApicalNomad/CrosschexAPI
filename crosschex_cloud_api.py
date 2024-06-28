import requests
from datetime import datetime, timedelta


"""
1: 'IT and Inventory Manager',
2:	'Assistant Manager',
4:	'OBL Manager',
5:	'MA',
6:	'RN',
7:	'Office Assistant',
8:	'Patient Intake Specialist',
9:	'Sonographer',

"""
employee_postion_dict = {
    1: "IT and Inventory Manager",
    2: "Assistant Manager",
    4: "OBL Manager",
    5: "MA",
    6: "RN",
    7: "Office Assistant",
    8: "Patient Intake Specialist",
    9: "Sonographer",
    10: "MA",
    11: "Call Center Team",
    12: "MA",
}

empl_id_name_dict = {
    1: "Yousaf Chaudry",
    2: "Mohamad Majdalawi",
    4: "Margaret Kline",
    5: "Hannah Billings",
    6: "Alex Wells",
    7: "Victoria Ulrich",
    8: "Ahmed Chaudry",
    9: "Tamrat Hailemariam",
    10: "Justine Elgen",
    11: "Maya Wells",
    12: "Eliza Aamir",
}

# this gets the initial token used per session
def get_crosschex_token():
    url = "https://api.us.crosschexcloud.com"
    now = datetime.now()
    payload = {
        "header[nameSpace]": "authorize.token",
        "header[nameAction]": "token",
        "header[version]": "1.0",
        "header[requestId]": "f1becc28-ad01-b5b2-7cef-392eb1526f39",
        "header[timestamp]": f"{now}",
        "payload[api_key]": "_apikey_",
        "payload[api_secret]": "_secret_",
    }
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return response.json()["payload"]["token"]

# this is the primary function to get the API data, defaults to previous pay period for simplicity, can be adjusted myriad of ways
def get_previous_pp(employee_id=None):
    """
    Arg a = payload[begin_time]
    Arb b = payload[end_time]
    --- Both should be datetime objects, as of 03/18/2024: testing 2 week intervals. ---
    """
    url = "https://api.us.crosschexcloud.com"
    now = datetime.now()
    new_token = get_crosschex_token()
    from time_parse import calculate_pay_period

    current_pp_number, current_pp_start, current_pp_end = calculate_pay_period(now)
    delta = timedelta(days=1)
    prior_pp_boundary = current_pp_start - delta
    prior_pp_number, prior_pp_start, prior_pp_end = calculate_pay_period(
        prior_pp_boundary
    )
    payload = {
        "header[nameSpace]": "attendance.record",
        "header[nameAction]": "getrecord",
        "header[version]": "1.0",
        "header[requestId]": "f1becc28-ad01-b5b2-7cef-392eb1526f39",
        "header[timestamp]": f"{now}",
        "authorize[type]": "token",
        "authorize[token]": f"{new_token}",
        "payload[begin_time]": f"{prior_pp_start}",
        "payload[end_time]": f"{prior_pp_end}",
        # "payload[begin_time]": f"{datetime(2023, 2, 11)}",
        # "payload[end_time]": f"{datetime(2025, 2, 27)}",
        # "payload[workno]": f"{int(employee_id)}",
        "payload[order]": "asc",
    }
    if employee_id:
        payload["payload[workno]"] = f"{int(employee_id)}"

    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    if response.json()["payload"]["count"] >= 100:
        return get_all_previous_pp()

    # print(response.text)
    return response.json()

def get_all_records():
    url = "https://api.us.crosschexcloud.com"
    now = datetime.now()
    new_token = get_crosschex_token()
    payload = {
        "header[nameSpace]": "attendance.record",
        "header[nameAction]": "getrecord",
        "header[version]": "1.0",
        "header[requestId]": "f1becc28-ad01-b5b2-7cef-392eb1526f39",
        "header[timestamp]": f"{now}",
        "authorize[type]": "token",
        "authorize[token]": f"{new_token}",
        "payload[begin_time]": f"{datetime(2023, 2, 11)}",
        "payload[end_time]": f"{datetime(2025, 2, 27)}",
        # "payload[workno]": f"{num}",
        "payload[order]": "asc",
    }
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    return response.json()


def get_specified_records(a=None, b=None):
    """
    Arg a = payload[begin_time]
    Arb b = payload[end_time]
    --- Both should be datetime objects, as of 03/18/2024: testing 2 week intervals. ---
    """
    url = "https://api.us.crosschexcloud.com"
    now = datetime.now()
    new_token = get_crosschex_token()
    from time_parse import calculate_pay_period

    pp_number, pp_start, pp_end = calculate_pay_period(now)
    payload = {
        "header[nameSpace]": "attendance.record",
        "header[nameAction]": "getrecord",
        "header[version]": "1.0",
        "header[requestId]": "f1becc28-ad01-b5b2-7cef-392eb1526f39",
        "header[timestamp]": f"{now}",
        "authorize[type]": "token",
        "authorize[token]": f"{new_token}",
        "payload[begin_time]": f"{datetime(2024, 4, 29)}",
        "payload[end_time]": f"{datetime(2024, 5, 12)}",
        # "payload[begin_time]": f"{datetime(2023, 2, 11)}",
        # "payload[end_time]": f"{datetime(2025, 2, 27)}",
        # "payload[workno]": f"{num}",
        "payload[order]": "asc",
    }
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    return response.json()



def get_all_previous_pp():
    all_records = get_previous_pp(
        employee_id=list(empl_id_name_dict.keys())[0]
    )  # this is first population of response dict
    for emp_id in list(empl_id_name_dict.keys())[1:]:
        [
            all_records["payload"]["list"].append(x)
            for x in get_previous_pp(employee_id=emp_id)["payload"]["list"]
        ]
    return all_records


def get_specific_employee_times(employee_id=None):
    """
    Arg a = payload[begin_time]
    Arb b = payload[end_time]
    --- Both should be datetime objects, as of 03/18/2024: testing 2 week intervals. ---
    """
    url = "https://api.us.crosschexcloud.com"
    now = datetime.now()
    new_token = get_crosschex_token()
    # from time_parse import calculate_pay_period

    # current_pp_number, current_pp_start, current_pp_end = calculate_pay_period(now)
    # delta = timedelta(days=1)
    # prior_pp_boundary = current_pp_start - delta
    # prior_pp_number, prior_pp_start, prior_pp_end = calculate_pay_period(
    #     prior_pp_boundary
    # )
    start = datetime(2024, 4, 20)
    end = datetime(2024, 6, 20)
    payload = {
        "header[nameSpace]": "attendance.record",
        "header[nameAction]": "getrecord",
        "header[version]": "1.0",
        "header[requestId]": "f1becc28-ad01-b5b2-7cef-392eb1526f39",
        "header[timestamp]": f"{now}",
        "authorize[type]": "token",
        "authorize[token]": f"{new_token}",
        "payload[begin_time]": f"{start}",
        "payload[end_time]": f"{end}",
        # "payload[begin_time]": f"{datetime(2023, 2, 11)}",
        # "payload[end_time]": f"{datetime(2025, 2, 27)}",
        # "payload[workno]": f"{int(employee_id)}",
        "payload[order]": "asc",
    }
    if employee_id:
        payload["payload[workno]"] = f"{int(employee_id)}"

    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    return response.json()


def test_records(a=None, b=None):
    """
    Arg a = payload[begin_time]
    Arb b = payload[end_time]
    --- Both should be datetime objects, as of 03/18/2024: testing 2 week intervals. ---
    """
    url = "https://api.us.crosschexcloud.com"
    now = datetime.now()
    new_token = get_crosschex_token()
    from time_parse import calculate_pay_period

    pp_number, pp_start, pp_end = calculate_pay_period(now)
    payload = {
        "header[nameSpace]": "attendance.record",
        "header[nameAction]": "getrecord",
        "header[version]": "1.0",
        "header[requestId]": "f1becc28-ad01-b5b2-7cef-392eb1526f39",
        "header[timestamp]": f"{now}",
        "authorize[type]": "token",
        "authorize[token]": f"{new_token}",
        "payload[begin_time]": f"{datetime(2024, 3, 18)}",
        "payload[end_time]": f"{datetime(2024, 3, 31)}",
        # "payload[begin_time]": f"{datetime(2023, 2, 11)}",
        # "payload[end_time]": f"{datetime(2025, 2, 27)}",
        # "payload[workno]": f"{num}",
        "payload[order]": "asc",
    }
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    return response.json()


"""
02/19/2024: this is response.text = 

{"header":{"nameSpace":"authorize.token","nameAction":"token","version":"1.0","requestId":"f1becc28-ad01-b5b2-7cef-392eb1526f39","timestamp":"2024-02-19 13:37:25.463743"},"payload":{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2NvZGUiOiIxMTAwMTE5MzMiLCJob29rc19vbiI6MCwidXJsIjoiIiwic2VjcmV0IjoiIiwiY3JlYXRlX3RpbWUiOiIiLCJ1cGRhdGVfdGltZSI6IiIsImFwaV9rZXkiOiI4ZGJmZDYxNjgyYzFhN2E4YTVhZjliNjI5ZGZhOTNhNSIsImFwaV9zZWNyZXQiOiIyZWU1N2VhOGNlMTQ0OWYxYTBjOTY2ZDY2OTBiYTg4OCIsImV4cCI6MTcwODM3NTAzNn0.yhPNeGW2oBcisG-orWEkHMsKB7Dx2Su13-LI-3yGKps","expires":"2024-02-19T20:37:16+00:00"}}

"""


"""
import pandas as pd
from datetime import datetime, timedelta

# Constants
T0 = datetime.strptime("2024-02-19", "%Y-%m-%d")
PAY_PERIOD_LENGTH = 14

# Functions
def calculate_pay_period(date):
    delta = date - T0
    period_number = delta.days // PAY_PERIOD_LENGTH
    period_start = T0 + timedelta(days=period_number * PAY_PERIOD_LENGTH)
    period_end = period_start + timedelta(days=PAY_PERIOD_LENGTH - 1)
    return period_number, period_start, period_end

def assign_shift_to_period(clock_in, clock_out):
    _, period_start_in, period_end_in = calculate_pay_period(clock_in)
    _, period_start_out, period_end_out = calculate_pay_period(clock_out)
   
    if period_start_in == period_start_out or (clock_in < period_start_out and clock_out <= period_end_out):
        return period_start_out, period_end_out
    else:
        return period_start_out, period_end_out

def calculate_shift_hours(clock_in, clock_out):
    duration = clock_out - clock_in
    hours = duration.total_seconds() / 3600
    return hours

def process_shifts(df):
    # Sort and calculate shift durations
    df.sort_values(by=['employee.workno', 'checktime'], inplace=True)
   
    # Calculate pay period for each shift
    df['pay_period'] = df['checktime'].apply(lambda x: calculate_pay_period(x)[0])
   
    # Calculate hours worked for each shift assuming consecutive logins as in/out pairs
    df['shift_end'] = df.groupby('employee.workno')['checktime'].shift(-1)
    df['hours_worked'] = (df['shift_end'] - df['checktime']).dt.total_seconds() / 3600
   
    # Drop NaN values in 'shift_end' to filter out last entry or unmatched shifts
    df.dropna(subset=['shift_end'], inplace=True)
   
    # Group by pay period and sum hours worked
    pay_period_summary = df.groupby(['pay_period', 'employee.workno'])['hours_worked'].sum().reset_index()
   
    return pay_period_summary

# Assuming `data` is your JSON data loaded into a Python dictionary
def load_and_process_data(json_data):
    df = pd.DataFrame(json_data['payload']['list'])
   
    # Preprocess and convert 'checktime' to datetime
    df['checktime'] = pd.to_datetime(df['checktime'])
   
    # Process shifts to calculate hours worked and assign to pay periods
    summary_df = process_shifts(df)
   
    return summary_df

# Example usage
# Replace `json_data` with the actual JSON data variable
# summary_df = load_and_process_data(json_data)
# print(summary_df)

# def get_empl_record(num):
#     url = "https://api.us.crosschexcloud.com"
#     now = datetime.now()
#     payload = {
#         "header[nameSpace]": "attendance.record",
#         "header[nameAction]": "getrecord",
#         "header[version]": "1.0",
#         "header[requestId]": "f1becc28-ad01-b5b2-7cef-392eb1526f39",
#         "header[timestamp]": f"{now}",
#         "authorize[type]": "token",
#         "authorize[token]": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2NvZGUiOiIxMTAwMTE5MzMiLCJob29rc19vbiI6MCwidXJsIjoiIiwic2VjcmV0IjoiIiwiY3JlYXRlX3RpbWUiOiIiLCJ1cGRhdGVfdGltZSI6IiIsImFwaV9rZXkiOiI4ZGJmZDYxNjgyYzFhN2E4YTVhZjliNjI5ZGZhOTNhNSIsImFwaV9zZWNyZXQiOiIyZWU1N2VhOGNlMTQ0OWYxYTBjOTY2ZDY2OTBiYTg4OCIsImV4cCI6MTcwODM3NTE3NH0.exitShdCHVOI2IwZjh3ulLx9YJbXk0fgKMYVJFbSfFNAfVM",
#         "payload[begin_time]": f"{datetime(2024, 2, 18)}",
#         "payload[end_time]": f"{datetime(2024, 2, 21)}",
#         "payload[workno]": f"{num}",
#         "payload[order]": "asc",
#     }
#     files = []
#     headers = {}

#     response = requests.request("POST", url, headers=headers, data=payload, files=files)

#     print(response.text)
#     return response.json()



"""
