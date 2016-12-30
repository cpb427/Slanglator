import twitter
import gc
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Slanglator:

	consumer_key='YqNQtQdh6r1OaBFjPP5K0l8iY'
        consumer_secret='C6hoTHuAV9r3JMi8bf2ryHwvot5EjIcuEItSmDyOafItRBkxxl'
        access_token_key='809779950660292612-FyTyI2kWUGlz0EV0Z9fc6mkXqpSkevK'
        access_token_secret='iYlWPyxYzNjKBHceoLoKEsodLBnRY0tp5ZdfCQPg18Zce'
	#TODO: this doesn't need to be a dictionary anymore
	searchSlangWords = {'idgaf':"I don't give a fuck",'omg':'oh my gosh','omfg':'om my freaking gosh',
			    'wack':'bad','phat':'amazing','bae':'babe','aye':'yes','respek':'respect',
			    "murica":'The United States of America','lit':'intoxicated','tryna': 'trying to',
		  	    'gud':'good','dope': 'great','cake': 'butt','ayyyy': 'ahhhh!', 'lmao': "I'm laughing hard",
			    'cuh': 'Cousin', 'dawg' : 'friend', 'bruh':'friend','ratchet':'messy','mang': 'man',
			    'Throwing Shade' : 'Engaging in disrespectful activity', 'smh': 'shaking my head',
			    'wyd' : 'what are you doing?', 'yolo' : 'you only live once', 'fam': 'family', 'yeet' : 'yes!', 'af':'as fudge'}

	translateSlangWords = {'blast':'shame','L':'lose','ayyy':'ahhh!','idgaf':"I don't give a fudge",'omg':'oh my gosh',
			       'omfg':'om my freaking gosh','wack':'bad','phat':'amazing','bae':'babe','aye':'yes',
			       'respek':'respect',"murica":'The United States of America','lit':'crazy',
			       'tryna': 'trying to', 'gud':'good','dope': 'great','cake': 'butt','ayyyy': 'ahhhh!', 
			       'lmao': "I'm laughing hard",'cuh': 'Cousin', 'dawg' : 'friend', 'bruh':'friend','ratchet':'messy',
			       'mang': 'man','Throwing Shade' : 'Engaging in disrespectful activity', 'smh': 'shaking my head', 
			       'wyd' : 'what are you doing?', 'yolo' : 'you only live once', 'fam': 'family', 'r':'are',
			       'abt':'about','ppl':'people','pls':'please','u':'you','ur':'your','cuz':'because', 'gon' : 'gone', 
			       'tryna': 'trying to', 'yo' : 'your', 'cos' : 'because', 'dem': 'them', 'yeet' : 'yes!', 'dis':'this',
				'tho':'though', 'da':'the', 'rn':'right now', 'af' : 'as fudge', 'yall':'you all', 'idk':'I dont know', 'turnt':'hyper'}

	slangKeys = searchSlangWords.keys()
	translateSlangKeys = translateSlangWords.keys()

	tweetsThatHaveBeenSlanglated = [] 
	
	def __init__(self):
		self.searchSlangWords = Slanglator.searchSlangWords
		self.translateSlangWords = Slanglator.translateSlangWords	
		#configure api object to interact with Twitter
		self.api = twitter.Api(consumer_key = Slanglator.consumer_key,
				  consumer_secret = Slanglator.consumer_secret,
				  access_token_key = Slanglator.access_token_key,
				  access_token_secret = Slanglator.access_token_secret)
	
	def generateFullSlangTwitterString(self):
		"""
		OUTPUT: the search terms part of the twitter url we use to search for tweets
		"""
		returnString = ''
		returnString += ' {s} OR '.format(s=Slanglator.slangKeys[0])
		for slangWord in Slanglator.slangKeys:
			if slangWord != Slanglator.slangKeys[0]:
				returnString += '{x}'.format(x=slangWord)
				if slangWord != Slanglator.slangKeys[-1]:
					returnString += ' OR ' 
		return returnString


	def startTwitterSearch(self):
		sleepTimer = 5
		while True:
			try:
				#time in seconds that bot checks Twitter
				starttime = time.time()
				time.sleep(sleepTimer - ((time.time() - starttime) % 60.0))
				sleepTimer = 900
				print starttime
				#generate query string from table
				#search from query string
				twitterSpam = self.api.GetSearch(raw_query='q='+self.generateFullSlangTwitterString()+'&count=100')
				print "100 tweets pulled..."
				#parse each tweet, find one that works
				matches = []
				for tweet in twitterSpam:
					words = tweet.text.split()
					found = set(self.slangKeys) & set(words)
					#if 3 slang words are found
					if len(found) >= 3:
						print tweet.text
						#slanglate
						Slanglator.tweetsThatHaveBeenSlanglated
						if tweet.id not in Slanglator.tweetsThatHaveBeenSlanglated:
							slangTweet = self.slanglate(tweet)
							#post retweet
							self.retweet(tweet, slangTweet)
							sleepTimer = 14400 #sleep for 4 hours upon successful retweet
							print "\n\n"
			except:
				print 'Twitter Error - taking 3 hour break'
				sleepTimer = 10800
		#repeat

	def slanglate(self,tweet):
		"""
		INPUT : The Tweet
		OUTPUT : The Slanglated Text
		"""
		slanglated = ''
		for word in tweet.text.split():
			if word.lower() in Slanglator.translateSlangKeys:
				word = Slanglator.translateSlangWords[word]
			slanglated += '{x} '.format(x=word)
		return slanglated

	def retweet(self,tweet, newTweet):
		"""
		INPUT: api object, tweet to respond to, and  newTweet text
		OUTPUT: creates the new text values for the slanglated tweets , then calls the send tweet function 
		"""
		#add the tweet id, so we know to ignore it next time.
		Slanglator.tweetsThatHaveBeenSlanglated
		Slanglator.tweetsThatHaveBeenSlanglated += [tweet.id]
		numberOfNewTweets = len(newTweet)/135 
		remainder = len(newTweet) % 135
		if remainder != 0:
			numberOfNewTweets = numberOfNewTweets + 1
		introductionTweet = ' I have detected a large amount of slang in one of your tweets, and have Slang-Translated it : (0/{z})'.format(x = tweet.user.name , z = numberOfNewTweets)
		print introductionTweet
		self.sendTweet(introductionTweet, tweet)
		for i in range(numberOfNewTweets):
			tweetToSend = newTweet[(135 * i):(135 * (i + 1))] 
			tweetToSend += '({x}/{y})'.format(x = (i + 1), y = (numberOfNewTweets))
			print tweetToSend
			self.sendTweet(tweetToSend, tweet)
		print "\n\n ---------------- \n\n"

	def sendTweet(self,tweet, originalTweet):
		"""
		INPUT : tweet text to be sent as a tweet from Slangulator
			original tweet to respond to
			api object to send tweet with
		OUTPUT: tweet gets posted as a reply to original tweet
		"""
		self.api.PostUpdate(status = tweet,in_reply_to_status_id = originalTweet.id,auto_populate_reply_metadata = True)

	


#main
gc.enable()
slangBot = Slanglator()
slangBot.startTwitterSearch()


