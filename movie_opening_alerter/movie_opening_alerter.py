# __author__ = "phoenikx"
import codecs
import datetime
import os
import sys

import requests
from bs4 import BeautifulSoup
from sendgrid import Email, sendgrid
from sendgrid.helpers.mail import Content, Mail, Personalization


class CinemaHallOpeningAlerter:
    def __init__(self, movie_name, movie_id, location, emails):
        self.email_sender = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        self.from_email = Email(os.environ.get('FROM_EMAIL'))
        self.base_url = "https://in.bookmyshow.com"
        self.subject = "BMS Alert: Booking opened for a movie"
        self.movie_name = movie_name
        self.movie_id = movie_id
        self.location = self.location
        self.emails = emails
        self.email_content = Content(type_='text/html',
                                     value=str(codecs.open("movie_opening_alerter/movie_opening_alerter.html", 'r')
                                               .read())
                                     .replace('{movie}', self.movie_name)
                                     .replace('{location}', self.location))

    def build_email(self):
        mail = Mail(from_email=self.from_email, subject=self.subject, to_email=self.from_email,
                    content=self.email_content)
        personalization = Personalization()
        for email in self.emails:
            personalization.add_to(Email(email))
        mail.add_personalization(personalization)
        return mail.get()

    def has_movie_opened(self):
        r = requests.get(self.base_url + "/" + self.movie_name + "/" + self.movie_id)
        soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
        theatre_list = soup.findAll("a", {"class": "__venue-name"})
        print("Theatres found: %s" % str(theatre_list))
        for theatre in theatre_list:
            # this is the part which may have to be changed
            formatted_theatre_name = str(theatre).lower()
            flag = True
            for keyword in self.keywords:
                if keyword not in formatted_theatre_name:
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
        print("Movie:%s has opened: %s in theatre: %s" % (self.movie_name, has_opened, theatre))
        if has_opened:
            self.send_email()


if __name__ == '__main__':
    _name = sys.argv[1]
    _id = sys.argv[2]
    _keywords = [x.lower() for x in sys.argv[3].split(",")]
    _emails = sys.argv[4].split(",")
    print('Running hall opening alerter script at %s' % datetime.datetime.now())
    hall_opening_alerter = CinemaHallOpeningAlerter(_name, _id, _keywords, _emails)
    hall_opening_alerter.run()
