# -*- coding: utf-8 -*-
from unittest import TestCase
from datetime import timedelta, date, datetime
from datextractor import datetime_parsing, this_week_day, previous_week_day, next_week_day, dateFromDuration

"""
  Output of the parser is an array of tuples
  [match, value, (start, end)]
"""

class DateTimeParsingTestCases(TestCase):
  def test_captured_patterns(self):
    base_date = datetime.now()

    input_text = 'The event is on Monday 12 January 2012'
    parser = datetime_parsing(input_text)
    self.assertIn('Monday 12 January 2012'.lower(), parser[0])
    self.assertEqual(parser[0][1], datetime(2012, 1, 12))
    self.assertEqual(len(parser), 1)

    input_text = 'This monday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), this_week_day(base_date, 0).strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = 'Last monday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), previous_week_day(base_date, 0).strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = 'Next monday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), next_week_day(base_date, 0).strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)

    input_text = '25 minutes from now'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), dateFromDuration(base_date, 25, 'minutes', 'from now').strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)
    self.assertEqual(parser[0][3], 'minute')

    input_text = '10 days later'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%y'), dateFromDuration(base_date, 10, 'days', 'later').strftime('%d-%m-%y'))
    self.assertEqual(len(parser), 1)
    self.assertEqual(parser[0][3], 'day')

    # input_text = '2010'
    # parser = datetime_parsing(input_text)
    # self.assertIn(input_text.lower(), parser[0])
    # self.assertEqual(parser[0][1].strftime('%Y'), input_text)
    # self.assertEqual(len(parser), 1)

    input_text = 'today'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))
    self.assertEqual(len(parser), 1)
    self.assertEqual(parser[0][3], 'day')

    input_text = 'tomorrow'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text, parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() + timedelta(days=1)).strftime('%d'))
    self.assertEqual(len(parser), 1)
    self.assertEqual(parser[0][3], 'day')

    input_text = 'yesterday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=1)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'day before yesterday'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=2)).strftime('%d'))
    self.assertEqual(len(parser), 1)

    input_text = 'day before today'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=1)).strftime('%d'))
    self.assertEqual(len(parser), 1)
    self.assertEqual(parser[0][3], 'day')

    input_text = 'day before tomorrow'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=0)).strftime('%d'))
    self.assertEqual(len(parser), 1)
    self.assertEqual(parser[0][3], 'day')

    input_text = '2 days before'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d'), (datetime.today() - timedelta(days=2)).strftime('%d'))
    self.assertEqual(len(parser), 1)
    self.assertEqual(parser[0][3], 'day')

    input_text = 'Monday and Friday'
    parser = datetime_parsing(input_text)
    self.assertIn('Monday'.lower(), parser[0])
    self.assertIn('Friday'.lower(), parser[1])
    self.assertEqual(parser[0][1].strftime('%d'), this_week_day(base_date, 0).strftime('%d'))
    self.assertEqual(parser[1][1].strftime('%d'), this_week_day(base_date, 4).strftime('%d'))
    self.assertEqual(len(parser), 2)

    input_text = 'First quarter of 2016'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-01-2016')
    self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '31-03-2016')
    self.assertEqual(len(parser), 1)

    input_text = 'Last quarter of 2015'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-09-2015')
    self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '31-12-2015')
    self.assertEqual(len(parser), 1)

    input_text = 'My birthday is on January 1st.'
    parser = datetime_parsing(input_text)
    self.assertIn('January 1st'.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '01-01-2018')
    self.assertEqual(len(parser), 1)

    input_text = 'My birthday is on January 1st 2014.'
    parser = datetime_parsing(input_text)
    self.assertIn('January 1st 2014'.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '01-01-2014')
    self.assertEqual(len(parser), 1)

    input_text = 'My birthday is on 2nd January 2014.'
    parser = datetime_parsing(input_text)
    self.assertIn('2nd January 2014'.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '02-01-2014')
    self.assertEqual(len(parser), 1)

    input_text = 'My birthday is on 10th of January 2014.'
    parser = datetime_parsing(input_text)
    self.assertIn('10th of January 2014'.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '10-01-2014')
    self.assertEqual(len(parser), 1)

    input_text = '10 Feb'
    parser = datetime_parsing(input_text)
    self.assertIn(input_text.lower(), parser[0])
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '10-02-2018')
    self.assertEqual(len(parser), 1)

    input_text = 'fourteenth april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '14-04-2017')

    input_text = 'fourteen april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '14-04-2017')

    input_text = 'four april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '04-04-2017')

    input_text = 'twenty april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '20-04-2017')

    input_text = 'twenty one april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '21-04-2017')

    input_text = 'twenty first april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '21-04-2017')

    input_text = 'twenty three april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '23-04-2017')

    input_text = 'twenty third april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '23-04-2017')

    input_text = 'twenty third of april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '23-04-2017')

    input_text = '21st of april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '21-04-2017')

    input_text = '21st april twenty seventeen'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '21-04-2017')

    input_text = '21st of april 20 18'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '21-04-2018')

    input_text = '21st of april 2018'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '21-04-2018')

    input_text = 'twenty first of april 20 18'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '21-04-2018')
    self.assertEqual(parser[0][3], 'day')

    input_text = '2012-2014'
    parser = datetime_parsing(input_text)
    self.assertEqual(isinstance(parser[0][1], list), True)
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-01-2012')
    self.assertEqual(parser[0][3], 'year')

    input_text = '2014-2012'
    parser = datetime_parsing(input_text)
    self.assertEqual(isinstance(parser[0][1], list), True)
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-01-2012')
    self.assertEqual(parser[0][3], 'year')

    input_text = 'last 3 months'
    parser = datetime_parsing(input_text)
    self.assertEqual(isinstance(parser[0][1], list), True)
    self.assertEqual(parser[0][3], 'month')

    input_text = 'last 3 weeks'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][3], 'week')

    input_text = 'last 3 days'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][3], 'day')

    input_text = 'last december'
    parser = datetime_parsing(input_text)

    self.assertEqual(parser[0][3], 'month')

    input_text = 'monday 12 jan 2012 at 12:23pm'
    parser = datetime_parsing(input_text)
    self.assertEqual(parser[0][3], 'day')
    self.assertEqual(parser[0][1].strftime('%d-%m-%Y %H:%M'), '13-01-2012 00:23')

    input_text = 'may be now'
    parser = datetime_parsing(input_text)
    self.assertEqual(len(parser), 0)

    input_text = 'in may'
    parser = datetime_parsing(input_text)
    self.assertEqual(len(parser), 1)

    input_text = 'hello aug' # May always gets captured
    parser = datetime_parsing(input_text)
    self.assertEqual(len(parser), 0)

    input_text = 'hello may' # May always gets captured
    parser = datetime_parsing(input_text)
    self.assertEqual(len(parser), 1)

    input_text = 'this weekend' # May always gets captured
    parser = datetime_parsing(input_text, base_date=datetime.strptime('24052010', "%d%m%Y").date)
    self.assertEqual(parser[0][3], 'day')
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '29-05-2010')
    self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '30-05-2010')

    input_text = 'last weekend' # May always gets captured
    parser = datetime_parsing(input_text, base_date=datetime.strptime('24052010', "%d%m%Y").date)
    self.assertEqual(parser[0][3], 'day')
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '22-05-2010')
    self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '23-05-2010')

    input_text = 'next weekend' # May always gets captured
    parser = datetime_parsing(input_text, base_date=datetime.strptime('24052010', "%d%m%Y").date)
    self.assertEqual(parser[0][3], 'day')
    self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '05-06-2010')
    self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '06-06-2010')