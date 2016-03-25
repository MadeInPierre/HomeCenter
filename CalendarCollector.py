'''
Classe prise du site de Google et modifiee qui donne les 50 prochains evenements de chaque
calendrier de Pierre.
'''
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class CalendarCollector():
    def get_events(self, start_year, start_month, start_day):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        try:
            controles_calendar_id   = "jh1vplv3t8tvg5uecguginu1i0@group.calendar.google.com"
            diverslycee_calendar_id = "iim4mi4h2p0sg4q2a63l6naaf0@group.calendar.google.com"
            travail_calendar_id     = "tj4oifktmlmuc2qbmko318nmk4@group.calendar.google.com"
            arendre_calendar_id     = "595q34j3kak6jb5nf97h90akko@group.calendar.google.com"
            main_calendar_id        = "pielaclau@gmail.com"



            credentials = self.get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)

            controles_events = self.get_events_from_calendar(service, controles_calendar_id   , start_year, start_month, start_day)
            divers_events    = self.get_events_from_calendar(service, diverslycee_calendar_id , start_year, start_month, start_day)
            travail_events   = self.get_events_from_calendar(service, travail_calendar_id     , start_year, start_month, start_day)
            arendre_events   = self.get_events_from_calendar(service, arendre_calendar_id     , start_year, start_month, start_day)
            main_events      = self.get_events_from_calendar(service, main_calendar_id        , start_year, start_month, start_day)

            return [("CONTROLES", controles_events),
                    ("ARENDRE",   arendre_events),
                    ("TRAVAIL",   travail_events),
                    ("DIVERS",    divers_events),
                    ("MAIN",      main_events)]
        except:
            
            return [("CONTROLES", [[u"PHY CT Em Epp Ec",   u"2016-03-25", u"test"], [u"MAT CT Integrales", u"2016-03-29", u""]]),
                    ("ARENDRE",   [[u"A rendre",           u"2016-04-05", ""],      [u"Autre",             u"2016-03-23", u""]]),
                    ("TRAVAIL",   [[u"Exercices de maths", u"2016-03-10", u""],     [u"Physiques exos cordialement",   u"2016-03-30", u""]]),
                    ("DIVERS",    [[u"Auto Ecole",         u"2016-03-08", u""],     [u"Journee portes ouvertes lycee", u"2016-03-25", u""]]),
                    ("MAIN",      [[u"AUTO ECOLE rdv",     u"2016-03-29", u""],     [u"Test",                          u"2016-03-25", u""]])]

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Google Calendar API Python Quickstart'


        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_events_from_calendar(self, service, ID, start_year, start_month, start_day):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        eventsAPI = service.events().list(calendarId = ID, timeMin = now, maxResults = 50, singleEvents = True, orderBy = 'startTime').execute()

        return self.parse_events(eventsAPI.get('items', []))

    def parse_events(self, events_source):
        parsed_events = []
        for event in events_source:
            start = event['start'].get('dateTime', event['start'].get('date'))

            try:
                description = event["description"]
            except:
                description = ""

            parsed_events.append([event["summary"], start, description])

        return parsed_events
