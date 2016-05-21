"""
Tests for datetime helpers.
"""
from datetime import datetime
from unittest import TestCase, main

import pytz

from datetime_utils import datetime_utils


class TestIsSnappedTo(TestCase):

    # UTC/GMT -2:30 hours
    tz = pytz.timezone('Canada/Newfoundland')

    # UTC/GMT -3 hours
    # Transition from 2015-02-22 24:00:00 -> 23:00:00
    # Transition from 2015-10-18 00:00:00 -> 01:00:00 (midnight doesn't exist)
    tz_AmericaSaoPaulo = pytz.timezone('America/Sao_Paulo')

    # UTC/GMT +2 hours
    # Transition from 2015-03-27 00:00:00 -> 01:00:00 (midnight doesn't exist)
    # Transition from 2015-10-30 01:00:00 -> 00:00:00 (midnight exists twice)
    tz_AsiaAmman = pytz.timezone('Asia/Amman')

    def test_unrecognized_period(self):
        dt = datetime(2015, 3, 1, 4, 1)
        with self.assertRaises(Exception):
            datetime_utils.is_snapped_to(dt, None)

    def test_naive_dt(self):
        period = 'minute'

        # success
        dt_success = datetime(2015, 3, 1, 4, 1)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 1, 35)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        period = 'minute-15'

        # success
        dt_success = datetime(2015, 3, 1, 4, 15)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 25)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        period = 'hour'

        # success
        dt_success = datetime(2015, 3, 1, 4)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 1)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        period = 'day'

        # success
        dt_success = datetime(2015, 3, 1)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 1)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

    def test_min(self):
        period = 'minute'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1, 4, 1))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 1, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

    def test_15_min(self):
        period = 'minute-15'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1, 4, 45))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

    def test_hour(self):
        period = 'hour'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1, 4))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

        # different TZ, would be success if TZ parameter not respected
        # depends on tz being a half-hour tz
        dt_should_fail = pytz.UTC.localize(datetime(2015, 3, 1))
        self.assertFalse(datetime_utils.is_snapped_to(dt_should_fail, period, self.tz))

    def test_day(self):
        period = 'day'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

        # different TZ, would be success if TZ parameter not respected
        # depends on tz being a half-hour tz
        dt_should_fail = pytz.UTC.localize(datetime(2015, 3, 1))
        self.assertFalse(datetime_utils.is_snapped_to(dt_should_fail, period, self.tz))

    def test_day_dst_transition_at_midnight_midnight_doesnt_exist(self):
        period = 'day'

        # America/Sao_Paulo Timezone
        # Transition from 2015-02-22 24:00:00 -> 23:00:00
        # same TZ, success
        dt_success = self.tz_AmericaSaoPaulo.localize(datetime(2015, 2, 22))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AmericaSaoPaulo))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AmericaSaoPaulo))

        # America/Sao_Paulo Timezone
        # Transition from 2015-10-18 00:00:00 -> 01:00:00 (midnight doesn't exist)
        # same TZ, success
        dt_success = self.tz_AmericaSaoPaulo.localize(datetime(2015, 10, 18))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AmericaSaoPaulo))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AmericaSaoPaulo))

        # same TZ, failure
        dt_fail = self.tz_AmericaSaoPaulo.localize(datetime(2015, 10, 18, 0, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AmericaSaoPaulo))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AmericaSaoPaulo))

    def test_day_dst_transition_at_midnight_midnight_exists_twice(self):
        period = 'day'

        # Asia/Amman Timezone
        # Transition from 2015-03-27 00:00:00 -> 01:00:00 (midnight doesn't exist)
        # same TZ, success
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 3, 27))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # Transition from 2015-10-30 01:00:00 -> 00:00:00 (midnight exists twice)
        # same TZ, success
        # this midnight should succeed - it's the first one
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=True)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, same success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # this midnight should fail - it's the second one
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=False)
        self.assertFalse(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, same failure
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # same TZ, failure
        dt_fail = self.tz_AsiaAmman.localize(datetime(2015, 10, 30, 0, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AsiaAmman))

    def test_hour_dst_transition_time_exists_twice(self):
        period = 'hour'

        # Transition from 2015-10-30 01:00:00 -> 00:00:00 (midnight exists twice)
        # first midnight
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=True)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, same success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # second midnight
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=False)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, same success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # make sure we're not passing other times that happen twice
        dt_fail = self.tz_AsiaAmman.localize(datetime(2015, 10, 30, 0, 5), is_dst=True)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AsiaAmman))

        dt_fail = self.tz_AsiaAmman.localize(datetime(2015, 10, 30, 0, 5), is_dst=False)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AsiaAmman))


class TestIsSnappedTo15Min(TestCase):

    # UTC/GMT -2:30 hours
    tz = pytz.timezone('Canada/Newfoundland')

    def test_naive_dt(self):
        # success
        dt_success = datetime(2015, 3, 1, 4, 15)
        self.assertTrue(datetime_utils.is_snapped_to_15min(dt_success))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 25)
        self.assertFalse(datetime_utils.is_snapped_to_15min(dt_fail))

    def test_non_naive_dt(self):
        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1, 4, 45))
        self.assertTrue(datetime_utils.is_snapped_to_15min(dt_success, self.tz))
        self.assertTrue(datetime_utils.is_snapped_to_15min(dt_success))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to_15min(dt_utc_success, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 35))
        self.assertFalse(datetime_utils.is_snapped_to_15min(dt_fail, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to_15min(dt_fail))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to_15min(dt_utc_fail, self.tz))


class RoundDatetime15Min(TestCase):
    def test_round_down(self):
        dt = datetime(2013, 4, 5, 2, 37)
        expected_result = datetime(2013, 4, 5, 2, 30)

        result = datetime_utils.round_datetime_to_15min(dt)
        self.assertEqual(result, expected_result)

    def test_round_up(self):
        dt = datetime(2013, 4, 5, 2, 38)
        expected_result = datetime(2013, 4, 5, 2, 45)

        result = datetime_utils.round_datetime_to_15min(dt)
        self.assertEqual(result, expected_result)


class RoundDatetime(TestCase):
    tz = pytz.timezone('America/Los_Angeles')
    tz_30 = pytz.timezone('Asia/Kolkata')

    def test_unrecognized_period(self):
        dt = datetime(2015, 3, 1, 4, 1)
        with self.assertRaises(Exception):
            datetime_utils.round_datetime(dt, None)

    def test_week1(self):
        dt = datetime(2015, 3, 12, 2, 33)
        period = 'week'
        expected_result = datetime(2015, 3, 9, 0, 0)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    def test_week2(self):
        dt = datetime(2013, 4, 6, 2, 33)
        period = 'week'
        expected_result = datetime(2013, 4, 8, 0, 0)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    def test_day(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 0, 0)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    def test_hour(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 3, 0)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    def test_15_minute_1(self):
        dt = datetime(2013, 4, 5, 2, 42)
        period = 'minute-15'
        expected_result = datetime(2013, 4, 5, 2, 45)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    def test_15_minute_2(self):
        dt = datetime(2013, 4, 5, 2, 15)
        period = 'minute-15'
        expected_result = datetime(2013, 4, 5, 2, 15)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    def test_minute1(self):
        dt = datetime(2013, 4, 5, 2, 33, 45)
        period = 'minute'
        expected_result = datetime(2013, 4, 5, 2, 34)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    def test_minute2(self):
        dt = datetime(2013, 4, 5, 2, 33, 25)
        period = 'minute'
        expected_result = datetime(2013, 4, 5, 2, 33)

        result = datetime_utils.round_datetime(dt, period)
        self.assertEqual(result, expected_result)

    # timezones

    def test_day_tz_1(self):
        dt = datetime(2013, 4, 5, 12, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 7, 0)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_2(self):
        dt = datetime(2013, 4, 5, 7, 0)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 7, 0)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_3(self):
        dt = datetime(2013, 4, 5, 19, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 6, 7, 0)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_30(self):
        dt = datetime(2013, 4, 5)
        period = 'day'
        expected_result = datetime(2013, 4, 4, 18, 30)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz_30)
        self.assertEqual(result, expected_result)

    def test_hour_tz_30(self):
        dt = datetime(2013, 4, 5, 18, 30)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 18, 30)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz_30)
        self.assertEqual(result, expected_result)

    def test_day_tz_before_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 8, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = dt

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_during_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 22, 30, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = self.tz.normalize(datetime(2015, 3, 9, 7, tzinfo=pytz.UTC))

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_after_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 23, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = self.tz.normalize(datetime(2015, 3, 9, 7, tzinfo=pytz.UTC))

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_week_tz_1(self):
        dt = datetime(2013, 3, 31, 2, 33)
        period = 'week'
        expected_result = datetime(2013, 4, 1, 7, 0)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    # note that April 2013 in LA is in DST while March is not

    def test_day_tz_11(self):
        dt = datetime(2013, 3, 5, 12, 33, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_12(self):
        dt = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_13(self):
        dt = datetime(2013, 3, 5, 19, 33, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 6, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    # test the force kwarg

    def test_force_day(self):
        dt = datetime(2013, 4, 5, 20)
        period = 'day'
        expected_result = datetime(2013, 4, 6, 0, 0)

        result = datetime_utils.round_datetime(dt, period, force=True)
        self.assertEqual(result, expected_result)

    def test_force_day_tz(self):
        dt = datetime(2013, 4, 5, 20, 0)
        period = 'day'
        expected_result = datetime(2013, 4, 6, 7, 0)

        result = datetime_utils.round_datetime(dt, period, tzinfo=self.tz, force=True)
        self.assertEqual(result, expected_result)

    def test_force_hour(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 3, 0)

        result = datetime_utils.round_datetime(dt, period, force=True)
        self.assertEqual(result, expected_result)


class RoundDatetimeUp(TestCase):
    tz = pytz.timezone('America/Los_Angeles')
    tz_30 = pytz.timezone('Asia/Kolkata')

    def test_week(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'week'
        expected_result = datetime(2013, 4, 8, 0, 0)

        result = datetime_utils.round_datetime_up(dt, period)
        self.assertEqual(result, expected_result)

    def test_day(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 6, 0, 0)

        result = datetime_utils.round_datetime_up(dt, period)
        self.assertEqual(result, expected_result)

    def test_hour(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 3, 0)

        result = datetime_utils.round_datetime_up(dt, period)
        self.assertEqual(result, expected_result)

    def test_15_minute_1(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'minute-15'
        expected_result = datetime(2013, 4, 5, 2, 45)

        result = datetime_utils.round_datetime_up(dt, period)
        self.assertEqual(result, expected_result)

    def test_15_minute_2(self):
        dt = datetime(2013, 4, 5, 2, 15)
        period = 'minute-15'
        expected_result = datetime(2013, 4, 5, 2, 15)

        result = datetime_utils.round_datetime_up(dt, period)
        self.assertEqual(result, expected_result)

    def test_minute(self):
        dt = datetime(2013, 4, 5, 2, 33, 45)
        period = 'minute'
        expected_result = datetime(2013, 4, 5, 2, 34)

        result = datetime_utils.round_datetime_up(dt, period)
        self.assertEqual(result, expected_result)

    def test_second(self):
        dt = datetime(2013, 4, 5, 2, 33, 44, 3412)
        period = 'second'
        expected_result = datetime(2013, 4, 5, 2, 33, 45)

        result = datetime_utils.round_datetime_up(dt, period)
        self.assertEqual(result, expected_result)

    # timezones

    def test_day_tz_1(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 7, 0)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_2(self):
        dt = datetime(2013, 4, 5, 7, 0)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 7, 0)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_3(self):
        dt = datetime(2013, 4, 5, 9, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 6, 7, 0)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_30(self):
        dt = datetime(2013, 4, 5)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 18, 30)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz_30)
        self.assertEqual(result, expected_result)

    def test_hour_tz_30(self):
        dt = datetime(2013, 4, 5, 18, 30)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 18, 30)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz_30)
        self.assertEqual(result, expected_result)

    def test_day_tz_before_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 8, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = dt

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_during_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 10, 30, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = self.tz.normalize(datetime(2015, 3, 9, 7, tzinfo=pytz.UTC))

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_after_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 13, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = self.tz.normalize(datetime(2015, 3, 9, 7, tzinfo=pytz.UTC))

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_week_tz_1(self):
        dt = datetime(2013, 3, 31, 2, 33)
        period = 'week'
        expected_result = datetime(2013, 4, 1, 7, 0)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    # note that April 2013 in LA is in DST while March is not

    def test_day_tz_11(self):
        dt = datetime(2013, 3, 5, 2, 33, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_12(self):
        dt = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_13(self):
        dt = datetime(2013, 3, 5, 9, 33, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 6, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    # test the force kwarg

    def test_force_day(self):
        dt = datetime(2013, 4, 5)
        period = 'day'
        expected_result = datetime(2013, 4, 6, 0, 0)

        result = datetime_utils.round_datetime_up(dt, period, force=True)
        self.assertEqual(result, expected_result)

    def test_force_day_tz(self):
        dt = datetime(2013, 4, 5, 7, 0)
        period = 'day'
        expected_result = datetime(2013, 4, 6, 7, 0)

        result = datetime_utils.round_datetime_up(dt, period, tzinfo=self.tz, force=True)
        self.assertEqual(result, expected_result)

    def test_force_hour(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 3, 0)

        result = datetime_utils.round_datetime_up(dt, period, force=True)
        self.assertEqual(result, expected_result)


class RoundDatetimeDown(TestCase):
    tz = pytz.timezone('America/Los_Angeles')
    tz_30 = pytz.timezone('Asia/Kolkata')

    def test_unrecognized_period(self):
        dt = datetime(2015, 3, 1, 4, 1)
        with self.assertRaises(Exception):
            datetime_utils.round_datetime_down(dt, None)

    def test_week(self):
        dt = datetime(2015, 3, 12, 2, 33)
        period = 'week'
        expected_result = datetime(2015, 3, 9, 0, 0)

        result = datetime_utils.round_datetime_down(dt, period)
        self.assertEqual(result, expected_result)

    def test_day(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 0, 0)

        result = datetime_utils.round_datetime_down(dt, period)
        self.assertEqual(result, expected_result)

    def test_hour(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 2, 0)

        result = datetime_utils.round_datetime_down(dt, period)
        self.assertEqual(result, expected_result)

    def test_15_minute_1(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'minute-15'
        expected_result = datetime(2013, 4, 5, 2, 30)

        result = datetime_utils.round_datetime_down(dt, period)
        self.assertEqual(result, expected_result)

    def test_15_minute_2(self):
        dt = datetime(2013, 4, 5, 2, 15)
        period = 'minute-15'
        expected_result = datetime(2013, 4, 5, 2, 15)

        result = datetime_utils.round_datetime_down(dt, period)
        self.assertEqual(result, expected_result)

    def test_minute(self):
        dt = datetime(2013, 4, 5, 2, 33, 45)
        period = 'minute'
        expected_result = datetime(2013, 4, 5, 2, 33)

        result = datetime_utils.round_datetime_down(dt, period)
        self.assertEqual(result, expected_result)

    def test_second(self):
        dt = datetime(2013, 4, 5, 2, 33, 45, 23948)
        period = 'second'
        expected_result = datetime(2013, 4, 5, 2, 33, 45)

        result = datetime_utils.round_datetime_down(dt, period)
        self.assertEqual(result, expected_result)

    # rounding with timezones is tricky.

    def test_day_tz_1(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 4, 7, 0)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_2(self):
        dt = datetime(2013, 4, 5, 7, 0)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 7, 0)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_3(self):
        dt = datetime(2013, 4, 5, 7, 33)
        period = 'day'
        expected_result = datetime(2013, 4, 5, 7, 0)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_30(self):
        dt = datetime(2013, 4, 5)
        period = 'day'
        expected_result = datetime(2013, 4, 4, 18, 30)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz_30)
        self.assertEqual(result, expected_result)

    def test_hour_tz_30(self):
        dt = datetime(2013, 4, 5, 8)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 7, 30)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz_30)
        self.assertEqual(result, expected_result)

    # note that April 2013 in LA is in DST while March is not

    def test_day_tz_4(self):
        dt = datetime(2013, 3, 5, 2, 33, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 4, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_5(self):
        dt = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_6(self):
        dt = datetime(2013, 3, 5, 9, 33, tzinfo=pytz.UTC)
        period = 'day'
        expected_result = datetime(2013, 3, 5, 8, 0, tzinfo=pytz.UTC)

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_before_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 8, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = dt

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_during_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 10, 30, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = self.tz.normalize(datetime(2015, 3, 8, 8, tzinfo=pytz.UTC))

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    def test_day_tz_after_transition(self):
        dt = self.tz.normalize(datetime(2015, 3, 8, 13, tzinfo=pytz.UTC))
        period = 'day'
        expected_result = self.tz.normalize(datetime(2015, 3, 8, 8, tzinfo=pytz.UTC))

        result = datetime_utils.round_datetime_down(dt, period, tzinfo=self.tz)
        self.assertEqual(result, expected_result)

    # test the force kwarg

    def test_force_day(self):
        dt = datetime(2013, 4, 5)
        period = 'day'
        expected_result = datetime(2013, 4, 4, 0, 0)

        result = datetime_utils.round_datetime_down(dt, period, force=True)
        self.assertEqual(result, expected_result)

    def test_force_hour(self):
        dt = datetime(2013, 4, 5, 2, 33)
        period = 'hour'
        expected_result = datetime(2013, 4, 5, 2, 0)

        result = datetime_utils.round_datetime_down(dt, period, force=True)
        self.assertEqual(result, expected_result)

    def test_force_day_tz(self):
        dt = datetime(2013, 4, 5, 7, 0)
        period = 'day'
        expected_result = datetime(2013, 4, 4, 7, 0)

        result = datetime_utils.round_datetime_down(dt, period, force=True, tzinfo=self.tz)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    main()
