import datetime

from shiftex.main.routes import main


@main.app_template_filter()
def timestamp_to_readable(timestamp):
    timestamp = timestamp // 1000
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt


@main.app_template_filter()
def duration_to_readable(shift):
    shift_start = timestamp_to_readable(shift["from"])
    shift_end = timestamp_to_readable(shift["to"])
    duration = shift_end - shift_start
    return duration.total_seconds() // 3600


@main.app_template_filter()
def shift_id_list(swap_list):
    output = []
    for shift in swap_list:
        output.append(shift["shiftId"])
    return output


@main.app_template_filter()
def accept_id_from_list(shift_id, accept_list):
    # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
    list_index = next((i for i, item in enumerate(accept_list) if item["shiftId"] == shift_id), None)
    return accept_list[list_index]["accept"]
