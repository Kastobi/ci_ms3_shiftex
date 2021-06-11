"""
shiftex main package - filters module
=====================================

The filters to use in multiple templates from different packages.

Functions:
    timestamp_to_readable(timestamp)
    duration_to_readable(shift)
    shift_id_list(swap_list)
"""

import datetime

from shiftex.main.routes import main


@main.app_template_filter()
def timestamp_to_readable(timestamp: int) -> datetime:
    """
    Take a 13-digit timestamp int (given dataset)
    and parse the datetime
    :param timestamp: 13-digit int
    :return: datetime object
    """
    timestamp = timestamp // 1000
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt


@main.app_template_filter()
def duration_to_readable(shift: dict) -> float:
    """
    Take dict with .from and .to timestamps,
    convert them to datetime, calculate the
    timedelta and return hours.

    :param shift: dict with keys from and to, values 13-digit ints
    :return: float (hours)
    """
    shift_start = timestamp_to_readable(shift["from"])
    shift_end = timestamp_to_readable(shift["to"])
    duration = shift_end - shift_start
    return duration.total_seconds() // 3600


@main.app_template_filter()
def shift_id_list(swap_list: list) -> list:
    """
    Take list of dicts and extract the shiftId values.

    :param swap_list: list of dicts with "shiftId" key
    :return: list of "shiftId" values
    """
    output = []
    for shift in swap_list:
        output.append(shift["shiftId"])
    return output


@main.app_template_filter()
def accept_id_from_list(shift_id: str, accept_list: list) -> list:
    """
    Take a shift_id and a list of ids
    :param shift_id: id of the corresponding shift
    :param accept_list: list of dicts, [{"shiftId": id, "accept": id}]
    :return: list of accepted ids corresponding to input shift_id
    """
    output_list = []
    for item in accept_list:
        if item["shiftId"] == shift_id:
            output_list.append(item["accept"])
    return output_list
