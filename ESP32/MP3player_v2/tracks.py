import json

class Tracks:
    """
    Class to encapsulate tracks on SDcard.
    It can be initialised with a filename to load a JSON file with a
    list of two-element lists:
      [ ["song", <length in seconds>], [...] ]

    Access the tracks and time in the class variable "tracks" or use the functions
    to get just name or time on a track.
    """
    tracks = None

    def __init__(self, filename):
        # Load file.  If it does not exist, handle it gracefully.
        try:
            f = open(filename)
            self.tracks = json.load(f)
            f.close()
        except:
            self.tracks = None
        print(self.tracks)
 
    def get_track_name(self, number):
        print(f"get: {number} - {self.tracks[number][0]}")
        return self.tracks[number][0]
    
    def get_track_length(self, number):
        return self.tracks[number][1]
    
    def __str__(self):
         print(self.tracks)
