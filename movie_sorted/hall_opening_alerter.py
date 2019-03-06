# __author__ = "phoenikx"
import datetime
import os

import requests
import yaml
from bs4 import BeautifulSoup
from sendgrid import sendgrid, Email
from sendgrid.helpers.mail import Content, Mail


class CinemaHallOpeningAlerter:
    def __init__(self):
        self.email_sender = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        self.from_email = Email(os.environ.get('FROM_EMAIL'))
        self.to_email = Email(os.environ.get('TO_EMAIL'))
        self.base_url = "https://in.movie_sorted.com/buytickets"

    def has_movie_opened(self, movie_name, movie_id, keywords):
        r = requests.get(self.base_url + "/" + movie_name + "/" + movie_id)
        print(r.status_code)
        print(r.encoding)
        soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
        theatre_list = soup.findAll("a", {"class": "__venue-name"})
        for theatre in theatre_list:
            # this is the part which may have to be changed
            formatted_theatre_name = str(theatre).lower()
            flag = True
            for keyword in keywords:
                if keyword not in formatted_theatre_name:
                    flag = False
                    break
            if flag:
                print("Theatre matched: %s" % theatre)
                return True, theatre.contents[1]
        return False, None

    def alert(self, movie, theatre, keywords):
        subject = "BMS Alert: Booking for %s has opened in one of the matched theatres" % (movie)
        content = Content("text/plain", "Theatre matched: %s . <br> keywords used for searching: %s" %(theatre, keywords))
        mail = Mail(self.from_email, subject, self.to_email, content)
        response = self.email_sender.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def run(self, movie_name, movie_id, keywords):
        has_opened, theatre = self.has_movie_opened(movie_name, movie_id, keywords)
        print("Movie:%s has opened: %s in theatre: %s" % (movie_name, has_opened, theatre))
        if has_opened:
            self.alert(movie_name, theatre, keywords)


if __name__ == '__main__':
    lukka_chupi_movie = 'luka-chuppi-bengaluru'
    lukka_chupi_id = 'movie-bang-ET00078940-MT/20190306'
    captain_marvel_movie = 'captain-marvel-bengaluru'
    captain_marvel_id = 'movie-bang-ET00097168-MT/20190308'
    print('Running hall opening alerter script at %s' % datetime.datetime.now())
    hall_opening_alerter = CinemaHallOpeningAlerter()
    hall_opening_alerter.run(captain_marvel_movie, captain_marvel_id, ['central', 'pvr', 'bellandur'])
