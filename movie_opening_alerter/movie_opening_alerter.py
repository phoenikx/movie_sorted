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
    def __init__(self, movie_name, location, movie_id, emails, date_list):
        self.email_sender = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        self.from_email = Email(os.environ.get('FROM_EMAIL'))
        self.base_url = "https://in.bookmyshow.com/buytickets"
        self.location = location
        self.movie_name = movie_name
        self.movie_id = movie_id
        self.movie_name_with_location = self.movie_name + "-" + self.location
        self.subject = "BMS Alert: Booking for %s opened in location: %s" % (self.movie_name, self.location)
        self.emails = emails
        self.date_list = date_list
        self.email_content = Content(type_='text/html',
                                     value=str(codecs.open("movie_opening_alerter/movie_opening_alerter.html", 'r')
                                               .read())
                                     .replace('{movie_name}', self.movie_name)
                                     .replace('{location}', str(self.location))
                                     .replace('{status}', 'Booking started'))
        print(self.email_content.get())

    def build_email(self):
        mail = Mail(from_email=self.from_email, subject=self.subject, to_email=self.from_email,
                    content=self.email_content)
        personalization = Personalization()
        for email in self.emails:
            personalization.add_to(Email(email))
        mail.add_personalization(personalization)
        return mail.get()

    def has_booking_started(self):
        base_url = self.base_url + "/" + self.movie_name_with_location + "/" + self.movie_id
        for date in self.date_list:
            url = base_url + "/" + str(date)
            print("Checking url: ", url)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
            theatre_list = soup.findAll("a", {"class": "__venue-name"})
            if theatre_list:
                return True
        return False

    def send_email(self):
        response = self.email_sender.client.mail.send.post(request_body=self.build_email())
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def run(self):
        has_booking_started = self.has_booking_started()
        print("Booking for movie: %s has started: %s in location: %s" % (self.movie_name,
                                                                         has_booking_started, self.location))
        if has_booking_started:
            self.send_email()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_name', help='Movie name', type=str)
    parser.add_argument('location', help='Location', type=str)
    parser.add_argument('movie_id', help='Movie name', type=str)
    parser.add_argument('emails', help='Email ids to alert (separated by ,)', type=str)
    parser.add_argument("date_list", help="Date list")
    args = parser.parse_args()
    movie_name_to_query = args.movie_name
    location_to_query = args.location
    movie_id_to_query = args.movie_id
    emails_to_alert = args.emails.split(",")
    date_list_to_search = [] if not args.date_list else args.date_list.split(',')
    print('Running hall opening alerter script at %s' % datetime.datetime.now())
    hall_opening_alerter = CinemaHallOpeningAlerter(movie_name_to_query, location_to_query, movie_id_to_query,
                                                    emails_to_alert, date_list_to_search)
    hall_opening_alerter.run()
