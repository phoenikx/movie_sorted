# __author__ = "phoenikx"
import argparse
import codecs
import datetime
import os

import requests
from bs4 import BeautifulSoup
from sendgrid import Email, sendgrid
from sendgrid.helpers.mail import Content, Mail, Personalization


class CinemaHallOpeningAlerter:
    def __init__(self, movie_name, location, movie_id, keywords, emails, date_list=None):
        self.email_sender = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        self.from_email = Email(os.environ.get('FROM_EMAIL'))
        self.base_url = "https://in.bookmyshow.com/buytickets"
        self.subject = "BMS Alert: Booking opened in a theatre"
        self.movie_name_with_location = movie_name + "-" + location
        self.movie_id = movie_id
        self.keywords = keywords
        self.emails = emails
        if not date_list:
            current_day = datetime.datetime.today()
            next_day = current_day + datetime.timedelta(days=1)
            date_list = [current_day.strftime("%Y%m%d"), next_day.strftime("%Y%m%d")]
        self.date_list = date_list
        self.email_content = Content(type_='text/html',
                                     value=str(
                                         codecs.open("hall_opening_alerter/hall_opening_alerter.html", 'r').read()) \
                                     .replace('{movie}', self.movie_name_with_location) \
                                     .replace('{keywords}', str(self.keywords))
                                     .replace('{status}', 'Booking started'))

    def build_email(self):
        mail = Mail(from_email=self.from_email, subject=self.subject, to_email=self.from_email,
                    content=self.email_content)
        personalization = Personalization()
        for email in self.emails:
            personalization.add_to(Email(email))
        mail.add_personalization(personalization)
        return mail.get()

    def has_movie_opened(self):
        base_url = self.base_url + "/" + self.movie_name_with_location + "/" + self.movie_id
        for date in self.date_list:
            url = base_url + "/" + str(date)
            print("Checking url: ", url)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
            theatre_list = soup.findAll("a", {"class": "__venue-name"})
            for theatre in theatre_list:
                # this is the part which may have to be changed
                formatted_theatre_name = str(theatre).lower()
                flag = True
                for keyword in self.keywords:
                    if str(keyword).lower() not in formatted_theatre_name:
                        flag = False
                        break
                if flag:
                    print("Theatre matched: %s" % theatre)
                    return True, theatre.contents[1]
        return False, None

    def send_email(self):
        response = self.email_sender.client.mail.send.post(request_body=self.build_email())
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def run(self):
        has_opened, theatre = self.has_movie_opened()
        print("Movie:%s has opened: %s in theatre: %s" % (self.movie_name_with_location, has_opened, theatre))
        if has_opened:
            self.send_email()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_name', help='Movie name', type=str)
    parser.add_argument('location', help='Location', type=str)
    parser.add_argument('movie_id', help='Movie name', type=str)
    parser.add_argument('keywords', help='Keywords to identify theatre (separated by ,)', type=str)
    parser.add_argument('emails', help='Email ids to alert (separated by ,)', type=str)
    parser.add_argument("--date_list", help="Date list(optional)")
    args = parser.parse_args()
    movie_name_to_query = args.movie_name
    location_to_query = args.location
    movie_id_to_query = args.movie_id
    keywords_to_search = [x.lower() for x in args.keywords.split(",")]
    emails_to_alert = args.emails.split(",")
    date_list_to_search = [] if not args.date_list else args.date_list.split(',')
    print('Running hall opening alerter script at %s' % datetime.datetime.now())
    hall_opening_alerter = CinemaHallOpeningAlerter(movie_name_to_query, location_to_query, movie_id_to_query,
                                                    keywords_to_search, emails_to_alert, date_list_to_search)
    hall_opening_alerter.run()
