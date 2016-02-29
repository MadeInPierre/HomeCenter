'''
This module gets the news from LeMonde.fr and Pierre Laclau's facebook notifications.
it returns a list of lists, each one being a post/notification with the title, date, time and link.
'''

import feedparser
import unicodedata

class NewsCollector():

	def __init__(self):
		self.lemonde_url = "http://rss.lemonde.fr/c/205/f/3050/index.rss"
		self.PLFBNotifs_url = 'https://www.facebook.com/feeds/notifications.php?id=100000386870459&viewer=100000386870459&key=AWi1AKzYtLMWGIkO&format=rss20'
		self.pythonReddit_url = "http://www.reddit.com/r/python/.rss"

	def get_lemonde_posts(self):
		pased_news = feedparser.parse(self.lemonde_url)
		return self.parse(pased_news)

	def get_python_reddit(self):
		pased_news = feedparser.parse(self.pythonReddit_url)
		return self.parse(pased_news)

	def get_fb_notifications(self):
		pased_news = feedparser.parse(self.PLFBNotifs_url)
		return self.parse(pased_news)

	def parse(self, d):
		posts = []
		print d.entries[0]
		for post in d.entries:
			'''
			Certains sites ne donnent pas l'heure de publication des articles, ce qui fait crasher notre systeme si on
			essaye directement de la recuperer.
			Pour contourner le probleme, on met un try sur la partie qui recupere l'heure, et si cette partie echoue,
			le code execute le except qui met une simple heure fictive a la place.
			'''
			try:
				fulldate = post.published_parsed

				'''
				On transforme les infos de feedparser en date lisible, de la forme "15/10/2015"
				'''
				day = str(fulldate[2])
				if fulldate < 10: day = "0" + fulldate[2]
				month = str(fulldate[1])
				if month < 10: month = '0' + fulldate[1]


				date = day+"/"+month+"/"+str(fulldate[0])

				'''
				Meme chose pour recuperer une heure de la forme "17:35"
				'''
				hour = str(fulldate[3])
				if int(hour) < 10: hour = '0' + str(fulldate[3])
				minute = str(fulldate[4])
				if int(minute) < 10: minute = '0' + str(fulldate[4])

				post_time = hour + ':' + minute
			except:
				date = "99/99/99"
				post_time = "99:99"

			'''
			On ajoute l'article avec nos modifications d'heure et de date dans la liste principale.
			'''
			posts.append([post.title, date, post_time, post.link])

		return posts

	def format(self, input_str):
		print input_str
		encoding = "iso-8859-15" # or iso-8859-15, or cp1252, or whatever encoding you use
		unicode_string = input_str.decode(encoding)

		nfkd_form = unicodedata.normalize('NFKD', unicode_string)
		return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

'''
In Order to use this News module, create an instance of NewsCollector, and use one of the functions :
	- get_le_monde_posts()
	- get_fb_notifications()
'''
# collector = NewsCollector()
# news = collector.get_lemonde_posts()
# notifs = collector.get_fb_notifications()
