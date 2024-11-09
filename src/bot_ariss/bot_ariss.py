""" TODO """

# Note : Built-in imports
import html2text
import os
import requests
import sys
import yaml

from datetime import datetime, timedelta, date
from icalendar import Calendar
from pathlib import Path
from pytz import UTC
from typing import List, Dict, Optional, Any

try:
    pass

except ImportError as err:
    print("[IMPORT ERROR]\t\t{} : {}".format(__file__, err))
    sys.exit()


class BotAriss:
    """ TODO """

    def __init__(self,
                 future_days) -> None:
        """ Constructor

        :param future_days: TODO        
        """

        self._future_days = future_days

        # Reading configuration from .env file
        with open("./env.yaml", "r") as config_file:
            self._config = yaml.safe_load(config_file)

#        print(f"DBG :\n{self._config}")


    def _get_events_from_ics(self,
                             url):
        """ TODO """

        response = requests.get(url)
        response.raise_for_status()

        # ICS file analysis
        cal = Calendar.from_ical(response.content)

        # We keep track of the next 2 weeks (can be adapted)
        now      = datetime.utcnow().replace(tzinfo=UTC)
        deadline = now + timedelta(days=self._future_days)

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

                if now <= event_start <= deadline:
#                    print(f"DBG :\nevent_desc : {event_desc}")
                    found = any(s in event_desc for s in self._config["keywords"])
                    if found:
                      events.append({
                          "stamp"      : event_stamp,
                          "start"      : event_start,
                          "end"        : event_end,
                          "summary"    : event_summary,
                          "description": event_desc
                      })
#        print(f"DBG :\nevents : {events}")
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

    def get_synthese(self):
        """ TODO """

        events           = self._get_events_from_ics(self._config["CalendarURL"])
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
                         f"**Summary** : {summary}" \
                         f"---\n" \
#                        f"{content}" \

            s += event_info

        synthese = "-- **Planned ARISS contact** --\n" + s

#        print(f"DBG : \n{synthese}")
        return synthese


