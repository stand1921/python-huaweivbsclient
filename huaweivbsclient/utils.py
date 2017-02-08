"""Utils for the HuaWeiVBSClient"""


import re
import datetime
import pytz
import tzlocal
import exceptions


def format_job_status(job):
    """
    Convert job status dictionary into the format that cliff need for display.
    :param job: type dic
    :return: formatted result used for display
    """
    start = job['begin_time']
    end = job['end_time']
    success, start = utc_to_local_time(start)
    success, end = utc_to_local_time(end)
    cols = ['status', 'job_id', 'job_type', 'begin_time',
            'end_time', 'error_code', 'fail_reason']
    rows = [job['status'], job['job_id'], job['job_type'], start,
            end, job['error_code'], job['fail_reason']]
    for i in job['entities']:
        cols.append(i)
        rows.append(job['entities'][i])
    return cols, rows


def utc_to_local_time(utc_time_string):
    """Convert a utc datetime string to local datetime string."""
    try:
        utc_time = datetime.datetime.strptime(
            utc_time_string, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc)
        local_tz = tzlocal.get_localzone()
        local_time = utc_time.astimezone(local_tz)
        local_time_string = local_time.strftime('%Y-%m-%d %H:%M:%S')
        return True, local_time_string
    except:
        return False, utc_time_string


def check_id(string):
    """Check if an id string is valid"""
    if '/' in string or '\\' in string:
        raise exceptions.InvalidFormat(
            'Invalid symbols "/" or "\\" in ' + string)
    if len(string) != 32 and len(string) != 36:
        raise exceptions.InvalidFormat('ID length must be 32 or 36')
    return string


def check_name(string):
    """Check if an name string is valid"""
    if len(string) > 64:
        raise exceptions.InvalidFormat(
            'Argument "--name" length must be less than 64.')
    if re.search(u'[^A-Za-z0-9\u4e00-\u9fa5_-]', string):
        raise exceptions.InvalidFormat(
            'Argument "--name" symbol only can be one of those, '
            'english symbol, chinese symbol, number symbol, '
            'underscode(_) and Median line symbol.')
    return string


def check_description(string):
    """Check if an description string is valid"""
    if len(string) > 64:
        raise exceptions.InvalidFormat(
            'Argument "--description" length must be less than 64.')
    if re.search(u'[<>]', string):
        raise exceptions.InvalidFormat(
            'Argument "--description" symbol only can\'t be "<" and ">".')
    return string
