from datetime import datetime, timedelta

import pytz


def parse_period(period):
    """
    Parse a 'period' out to it's two parts

    >>> parse_period('minute-15')
    ('minute', 15)
    >>> parse_period('day')
    ('day', 1)
    """
    unit = period.split('-')[0]
    quantity = int((period.split('-') + ['1'])[1])
    return (unit, quantity)


def period_to_timedelta(period):
    """
    Valid periods are:
        minute, minute-15, hour, day, week
    'month' is not supported - months are varrying lengths of time
    """
    unit, quantity = parse_period(period)
    return timedelta(**{unit+'s': quantity})


def get_isoweek_monday(dt):
    # if it's a week we want to find the iso-week's monday
    return dt - timedelta(days=dt.weekday())


def round_datetime(dt, period, tzinfo=pytz.UTC, force=False):
    """
    Rounds a datetime to the nearest period.
    Valid periods are:
    minute, minute-15, hour, day, week

    :type dt: datetime
    :param dt: A naive or aware datetime object.

    :type period: str
    :param period: Options are minute, minute-15, hour, day, week

    :type tzinfo: pytz timezone
    :param tzinfo: A pytz timezone object. If given, the round will
        be performed with respect to the timezone.

    :type force: bool
    :param force: A boolean value. If force=True,
        it causes pre-rounded values to jump another step anyway.

    :rtype: datetime
    :returns: A datetime object that results from rounding datetime to the period.
        The timezone of the returned datetime will be equivalent to the
        original timezone of dt (or its DST equivalent if a DST border was
        crossed). If the input time was naive, it returns a naive datetime
        object.

    :raises: Exception if the period is not supported

    .. code-block:: python

        >>> import datetime
        >>> import pytz
        >>> import datetime_utils
        >>> # Weeks start on Monday, so the ceil will be for the next Monday
        >>> print datetime_utils.round_datetime(datetime.datetime(2013, 3, 3, 5), period='week')
        2013-03-04 00:00:00
        >>> print datetime_utils.round_datetime(datetime.datetime(2013, 3, 3, 5), period='day')
        2013-03-03 00:00:00
        >>> # Pass an aware datetime and return an aware datetime
        >>> print datetime_utils.round_datetime(datetime.datetime(2013, 3, 3, 5, tzinfo=pytz.utc), period='day')
        2013-03-03 00:00:00+00:00
        >>> print datetime_utils.round_datetime(datetime.datetime(2013, 3, 4, 6), period='day',
        ... tzinfo=pytz.timezone('US/Eastern'))
        2013-03-04 05:00:00
        >>> # Start with a naive UTC time and floor it with respect to EST
        >>> dt = datetime.datetime(2013, 2, 1)
        >>> # Since it is January 31 in EST, the resulting floored value
        >>> # for a day will be the previous day. Also, the returned value is
        >>> # in the original naive timezone of UTC
        >>> print datetime_utils.round_datetime(dt, period='day', tzinfo=pytz.timezone('US/Eastern'))
        2013-01-31 05:00:00
        >>> # Since it is January 31 in CST, the resulting floored value
        >>> # for a day will be the previous day. Also, the returned value is
        >>> # in the original timezone of EST
        >>> print datetime_utils.round_datetime(datetime.datetime(2013, 2, 1, 5, tzinfo=pytz.timezone('US/Eastern')),
        ... period='day', tzinfo=pytz.timezone('US/Central'))
        2013-02-01 01:00:00-05:00
    """

    if period == 'week':
        if dt.weekday() <= 4:
            return round_datetime_down(dt, 'week', tzinfo, force)
        else:
            return round_datetime_up(dt, 'week', tzinfo, force)

    if period == 'day':
        if dt.hour <= 12:
            return round_datetime_down(dt, 'day', tzinfo, force)
        else:
            return round_datetime_up(dt, 'day', tzinfo, force)

    if period == 'hour':
        if dt.minute <= 30:
            return round_datetime_down(dt, 'hour', tzinfo, force)
        else:
            return round_datetime_up(dt, 'hour', tzinfo, force)

    if period == 'minute-15':
        if dt.minute % 15 <= 7:
            return round_datetime_down(dt, 'minute-15', tzinfo, force)
        else:
            return round_datetime_up(dt, 'minute-15', tzinfo, force)

    if period == 'minute':
        if dt.second <= 30:
            return round_datetime_down(dt, 'minute', tzinfo, force)
        else:
            return round_datetime_up(dt, 'minute', tzinfo, force)

    raise Exception('Unrecognized period')


def round_datetime_to_15min(dt, tzinfo=None, force=False):
    """
    Rounds a datetime to the nearest 15 minute interval.

    :type dt: datetime
    :param dt: A naive or aware datetime object.

    :type tzinfo: pytz timezone
    :param tzinfo: A pytz timezone object. If given, the round will
        be performed with respect to the timezone.

    :type force: bool
    :param force: A boolean value. If force=True,
        it causes pre-rounded values to jump another step anyway.

    :rtype: datetime
    :returns: A datetime object that results from rounding datetime to a 15
        minute interval.
        The timezone of the returned datetime will be equivalent to the
        original timezone of dt (or its DST equivalent if a DST border was
        crossed). If the input time was naive, it returns a naive datetime
        object.

    .. code-block:: python

        >>> import datetime
        >>> import pytz
        >>> import datetime_utils
        >>> # Weeks start on Monday, so the floor will be for the previous Monday
        >>> print datetime_utils.round_datetime_to_15min(datetime.datetime(2013, 3, 3, 5, 17))
        2013-03-03 05:15:00
        >>> print datetime_utils.round_datetime_to_15min(datetime.datetime(2013, 3, 3, 5, 40))
        2013-03-03 05:45:00
        >>> # Pass an aware datetime and return an aware datetime
        >>> print datetime_utils.round_datetime_to_15min(datetime.datetime(2013, 3, 3, 5, 34, tzinfo=pytz.utc))
        2013-03-03 05:30:00+00:00
        >>> print datetime_utils.round_datetime_to_15min(datetime.datetime(2013, 3, 4, 6, 10),
        ... tzinfo=pytz.timezone('US/Eastern'))
        2013-03-04 06:15:00
        >>> # Start with a naive UTC time and floor it with respect to EST
        >>> dt = datetime.datetime(2013, 2, 1, 2, 56)
        >>> # Since it is January 31 in EST, the resulting floored value
        >>> # for a day will be the previous day. Also, the returned value is
        >>> # in the original naive timezone of UTC
        >>> print datetime_utils.round_datetime_to_15min(dt, tzinfo=pytz.timezone('US/Eastern'))
        2013-02-01 03:00:00
        >>> # Since it is January 31 in CST, the resulting floored value
        >>> # for a day will be the previous day. Also, the returned value is
        >>> # in the original timezone of EST
        >>> print datetime_utils.round_datetime_to_15min(datetime.datetime(2013, 2, 1, 5, 2,
        ... tzinfo=pytz.timezone('US/Eastern')), tzinfo=pytz.timezone('US/Central'))
        2013-02-01 04:45:00-05:00
    """
    return round_datetime(dt, 'minute-15', tzinfo, force)


def round_datetime_down(dt, period, tzinfo=None, force=False):
    """
    Round the given datetime down by 'snapping' it to the period.

    Valid periods are:
        minute, minute-15, hour, day, week

    If a timezone is specified, the rounding is done in that timezone.
    Else it is done in the timezone of the datetime.

    Specify force=True to cause pre-rounded values to jump another step anyway.
    """
    if force:
        dt = dt - timedelta.resolution

    org_tz = dt.tzinfo
    if not org_tz:
        dt = pytz.UTC.localize(dt)

    if tzinfo:
        dt = tzinfo.normalize(dt)

    rounded = None

    if period == 'week':
        monday = get_isoweek_monday(dt)
        args = [monday.year, monday.month, monday.day]
        rounded = datetime(*args)

    args = [dt.year, dt.month, dt.day]
    if period == 'day':
        rounded = datetime(*args)

    args.append(dt.hour)
    if period == 'hour':
        rounded = datetime(*args)
    if period == 'minute-15':
        args.append(dt.minute/15*15)
        rounded = datetime(*args)

    args.append(dt.minute)
    if period == 'minute':
        rounded = datetime(*args)

    args.append(dt.second)
    if period == 'second':
        rounded = datetime(*args)

    if rounded is None:
        raise Exception('Unrecognized period')

    rounded = dt.tzinfo.localize(rounded)

    if org_tz:
        rounded = org_tz.normalize(rounded)
    else:
        rounded = pytz.UTC.normalize(rounded).replace(tzinfo=None)

    return rounded


def round_datetime_up(dt, period, tzinfo=None, force=False):
    """
    Round the given datetime up by 'snapping' it to the period.

    Valid periods are:
        minute, minute-15, hour, day, week

    If a timezone is specified, the rounding is done in that timezone.
    Else it is done in the timezone of the datetime.

    Specify force=True to cause pre-rounded values to jump another step anyway.
    """
    if force:
        dt = dt + timedelta.resolution

    # we're already 'snapped' to the period
    previous = round_datetime_down(dt, period, tzinfo=tzinfo, force=force)

    if previous == dt:
        return previous

    # add the period, then round down.
    ahead = dt + period_to_timedelta(period)
    return round_datetime_down(ahead, period, tzinfo=tzinfo, force=force)


def is_snapped_to_15min(dt, tzinfo=None):
    """
    Checks if the datetime is 'snapped' to a 15 minute interval.

    :type dt: datetime
    :param dt: A naive or aware datetime object.

    :type tzinfo: pytz timezone
    :param tzinfo: A pytz timezone object.
        If a timezone is specified, the check is done in that timezone.
        Else it is done in the timezone of the datetime.

    :rtype: bool
    :returns: A boolean value that results from checking if the given datetime
        is snapped to a 15 minute interval

    .. code-block:: python

        >>> import datetime
        >>> import pytz
        >>> import datetime_utils
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 3, 3, 4, 20,
        ... tzinfo=pytz.utc), period='minute-15')
        False
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 2, 1, 5, 45,
        ... tzinfo=pytz.utc), period='minute-15', tzinfo=pytz.timezone('US/Eastern'))
        True
    """
    return is_snapped_to(dt, 'minute-15', tzinfo)


def is_snapped_to(dt, period, tzinfo=None):
    """
    Checks if the datetime is 'snapped' to the period.

    :type dt: datetime
    :param dt: A naive or aware datetime object.

    :type period: str
    :param period: Options are minute, minute-15, hour, day

    :type tzinfo: pytz timezone
    :param tzinfo: A pytz timezone object.
        If a timezone is specified, the check is done in that timezone.
        Else it is done in the timezone of the datetime.

    :rtype: bool
    :returns: A boolean value that results from checking if the given datetime
        is snapped to the period specified

    .. code-block:: python

        >>> import datetime
        >>> import pytz
        >>> import datetime_utils
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 3, 3), period='day')
        True
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 3, 3, 5), period='day')
        False
        >>> # Pass an aware datetime and return an aware datetime
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 3, 3, tzinfo=pytz.utc), period='day')
        True
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 2, 1, 5, tzinfo=pytz.utc), period='day',
        ... tzinfo=pytz.timezone('US/Eastern'))
        True
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 3, 3, 4, tzinfo=pytz.utc), period='hour')
        True
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 2, 1, 5, tzinfo=pytz.utc), period='hour',
        ... tzinfo=pytz.timezone('US/Eastern'))
        True
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 3, 3, 4, 20, tzinfo=pytz.utc), period='minute')
        True
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 2, 1, 5, 20, tzinfo=pytz.utc), period='minute',
        ... tzinfo=pytz.timezone('US/Eastern'))
        True
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 3, 3, 4, 20,
        ... tzinfo=pytz.utc), period='minute-15')
        False
        >>> print datetime_utils.is_snapped_to(datetime.datetime(2013, 2, 1, 5, 45,
        ... tzinfo=pytz.utc), period='minute-15',
        ... tzinfo=pytz.timezone('US/Eastern'))
        True
    """
    tz = tzinfo or dt.tzinfo
    dt_local = tz.normalize(dt) if tz else dt

    dt_less = dt - timedelta.resolution
    dt_less = tz.normalize(dt_less) if tz else dt_less

    if period == 'minute':
        return dt_less.minute != dt_local.minute

    if period == 'minute-15':
        return dt_less.minute / 15 != dt_local.minute / 15

    if period == 'hour':
        if dt_less.hour != dt_local.hour:
            return True

        # handling the case where there's a 'double hour' DST transition
        if (dt_less.tzinfo != dt_local.tzinfo and
                dt_less.minute > dt_local.minute):
            return True

        return False

    if period == 'day':
        return dt_less.day != dt_local.day

    raise Exception('Unrecognized period: %s' % period)
