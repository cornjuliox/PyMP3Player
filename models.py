import eyed3
import os.path
import os

# currently certain songs are not "validating" correctly.
# I need to figure out why.

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
		# TODO: replace this with a more ... robust ...
		# checking mechanism.
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











