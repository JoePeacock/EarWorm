import gdata.youtube
import gdata.youtube.service

class YoutubeAPI():

	def __init__(self):
		self.data = []

	def search(self, search_terms):
		yt_service = gdata.youtube.service.YouTubeService()
		query = gdata.youtube.service.YouTubeVideoQuery()
		query.vq = search_terms
		query.orderby = 'relevance'
		query.racy = 'include'
		feed = yt_service.YouTubeQuery(query)
		return feed

	def PrintVideoFeed(self, feed):
		for entry in feed.entry:
			self.PrintEntryDetails(entry)

	def PrintEntryDetails(self, entry):
		print 'Video title: %s' % entry.media.title.text
		print 'Video published on: %s ' % entry.published.text
		print 'Video description: %s' % entry.media.description.text
		print 'Video category: %s' % entry.media.category[0].text
		print 'Video tags: %s' % entry.media.keywords.text
		print 'Video watch page: %s' % entry.media.player.url
		print 'Video flash player URL: %s' % entry.GetSwfUrl()
		print 'Video duration: %s' % entry.media.duration.seconds

		# show thumbnails
		for thumbnail in entry.media.thumbnail:
			print 'Thumbnail url: %s' % thumbnail.url