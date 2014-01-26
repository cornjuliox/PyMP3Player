import eyed3
import os.path
import os

class Song():
	def __init__(self, filepath):
		self.filepath = self.Validate(filepath)
		# the dictionary seems redundant at this point
		# but i'll keep it in anyways to see where
		# it leads me.
		self.metadata = self.Analyze(self.filepath)
		self.title = u"".join(self.metadata["title"])
		self.artist = u"".join(self.metadata["artist"])
		self.album = u"".join(self.metadata["album"])
		self.length = u"".join(self.metadata["length"])

	def Validate(self, filepath):
		if os.path.exists(filepath):
			return filepath
		else:
			return ""

	def Analyze(self, filepath):
		metadict = {}
		try:
			audio_data = eyed3.load(filepath)
		except IOError:
			print "Not a valid file!"

		if audio_data == None:
			# if eyed3 fails to load the file
			# return a dict with empty values
			metadict["title"] = "(none)"
			metadict["artist"] = "(none)"
			metadict["album"] = "(none)"
			metadict["length"] = "(none)"
			return metadict
		else:
			metadict["title"] = audio_data.tag.title
			metadict["artist"] = audio_data.tag.artist
			metadict["album"] = audio_data.tag.album

			length_min = audio_data.info.time_secs / 60
			length_secs = audio_data.info.time_secs % 60
			if length_secs < 10:
				# I want a LEADING ZERO on this thing, STAT!
				metadict["length"] = "%d:%02d" % (length_min, length_secs)
			else:
				metadict["length"] = "%d:%d" % (length_min, length_secs)

			return metadict


class SubjectInterface():
	def __init__(self, *args, **kwargs):
		self.subscribers = []

	def RegisterObserver(self, observer):
		print "New subcriber registered!"
		self.subscribers.append(observer)

	def RemoveObserver(self, observer):
		# Now that I think about it I don't
		# actually know how to implement this.
		# delete() maybe?
		pass

	def NotifyObservers(self, value):
		print "Updated! Notifying all observers of the change."
		for index, observer in enumerate(self.subscribers):
			print "Observer %d has been notified." % index
			observer.UpdateStateControl(value)

class ObserverInterface():
	def __init__(self, *args, **kwargs):
		# data should be an iterable, a list of Song() objects.
		self.data = None

	# this name doesn't make sense but apparently
	# there's a function within wx named "Update".
	def UpdateStateControl(self, data):
		self.data = data

class Feed(SubjectInterface):
	def __init__(self, *args, **kwargs):
		super(Feed, self).__init__(*args, **kwargs)
		self._alreadyplayed = []
		self._songlist = []

	@property
	def songlist(self):
		# it occurs to me that I should just use pop() but...
		# maybe there's another way.
		song = _songlist[0]
		self._alreadyplayed.append(song)
		self._songlist[0].delete()
		return song

	@songlist.setter
	def songlist(self, value):
		# this might bite me later on. 
		self._songlist.extend(value)
		self.NotifyObservers(value)













