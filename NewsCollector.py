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
		for post in d.entries:
			'''
			Parse the date in the form of 09/03/2015
			'''
			fulldate = post.published_parsed

			day = str(fulldate[2])
			if fulldate < 10: day = "0" + fulldate[2]
			month = str(fulldate[1])
			if month < 10: month = '0' + fulldate[1]

			date = day+"/"+month+"/"+str(fulldate[0])

			'''
			Parse the hour in the form of 09:45
			'''
			hour = str(fulldate[3])
			if hour < 10: hour = '0' + str(fulldate[3])
			minute = str(fulldate[3])
			if minute < 10: minute = '0' + str(fulldate[3])

			post_time = hour + ':' + minute

			'''
			Add the post to the main list with a list
			Order : title, 
			'''
			# posts.append([self.format(post.title), self.format(date), self.format(post_time), self.format(post.link)])
			posts.append([post.title, date, post_time, post.link])
		# for post in posts:
		# 	print post[0] + post[1] + post[2] + post[3]

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
