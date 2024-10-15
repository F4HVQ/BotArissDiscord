# -*- coding: utf-8 -*-
""" TODO """

# Note : Built-in imports
import sys
import os

import html2text

from typing import List, Dict, Optional, Any
from pathlib import Path

from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from icalendar import Calendar
from pytz import UTC
import requests


class BotAriss:
    """ TODO """

    def __init__(self,
                 ) -> None:
        """ TODO """

        # Reading configuration from .env file
        load_dotenv()

        self.mode           = os.getenv('Mode')
        self.location       = os.getenv('Location')
        self.calendarURL    = os.getenv('CalendarURL')

#        print(f"DBG : {self.mode}")
#        print(f"DBG : {self.location}")
#        print(f"DBG : {self.calendarURL}")


    def _get_events_from_ics(self,
                            url):
        response = requests.get(url)
        response.raise_for_status()

        # ICS file analysis
        cal = Calendar.from_ical(response.content)

        # We keep track of the next 2 weeks (can be adapted)
        now            = datetime.utcnow().replace(tzinfo=UTC)
        two_week_later = now + timedelta(days=14)

        events = []

        for component in cal.walk():
            if component.name == "VEVENT":
                event_stamp   = component.get('dtstamp').dt
                event_start   = component.get('dtstart').dt
                event_end     = component.get('dtend')
                event_summary = component.get('summary')
                event_desc    = component.get('description')
                # If dtend is None, we use dstart as dtend (on day event)
                if event_end is None:
                    event_end = event_start
                else:
                    event_end = event_end.dt

                # We check objects are datetime so we can compare them
                if isinstance(event_start, datetime):
                    event_start = event_start
                elif isinstance(event_start, date):
                    event_start = datetime.combine(event_start, datetime.min.time(), tzinfo=UTC)

                if isinstance(event_end, datetime):
                    event_end = event_end
                elif isinstance(event_end, date):
                    event_end = datetime.combine(event_end, datetime.min.time(), tzinfo=UTC)

                if now <= event_start <= two_week_later:
                    #print(event_desc)
                    if self.location in event_desc:
                      events.append({
                          "start"      : event_start,
                          "end"        : event_end,
                          "stamp"      : event_stamp,
                          "summary"    : event_summary,
                          "description": event_desc
                      })
#        print(f"DBG : {events}")
        return events

    def _convert_html_to_markdown(self,
                                 html_content):
        """ TODO """

        h = html2text.HTML2Text()
        h.ignore_links    = True
        h.ignore_images   = True
        h.ignore_emphasis = False
        h.body_width      = 0

        markdown_content = h.handle(html_content)
        return markdown_content

#    def ret_upcoming_events(self,
#                            events):
#        """ TODO """
#
#        if not events:
#            print("Aucun événement à venir trouvé.")
#            return
#
#        print("Événements à venir:")
#        for event in events:
#            start   = event['start'].strftime('%d/%m/%Y')
#            end     = event['end'].strftime('%Y-%m-%d %H:%M:%S')
#            summary = event['summary']
#            content = self._convert_html_to_markdown(event['description'])
#
#            return(f"{start} - {end}: {summary}\n--\n {content}")

    def send_msg(self):
        """ TODO """


        ics_url          = self.calendarURL
        events           = self._get_events_from_ics(ics_url)
#        formatted_events = self.ret_upcoming_events(events)
#        print(f"DBG : {formatted_events}")

        if not events:
            print("No event found.")
            return

        print("Future events:")
        s = ""
        for event in events:
            start   = event['start'].strftime('%Y-%m-%d %H:%M:%S')
            end     = event['end'].strftime('%Y-%m-%d %H:%M:%S')
            summary = self._convert_html_to_markdown(event['summary'])
            content = self._convert_html_to_markdown(event['description'])

            event_info = f"**Date**    : {start}\n" \
                         f"**Summary** : {summary}"
                         f"---\n" \
#                        f"{content}" \

            s += event_info

        synthese = "-- **Planned ARISS contact** --\n" + s

#        print(f"DBG : \n{synthese}")
        return synthese


