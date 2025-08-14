import json

class TrackManager:
    """
    Class to encapsulate tracks on SDcard.
    It must be initialised with a filename to load a JSON file with this
    structure:
        {
          "tracks": [
                     [<folder_id>,<track_id>,"<title>", <length in seconds>],
                     ...
                    ],
          "playlists": {
            "<title>": [[<folder>,<track>],[...]],
            "<title>": <folder>,
            ...
          }
        }
    Access the tracks and time in the class variable "tracks" or use the functions
    to get just name or time on a track.
    Accesss the playlists in the class valiable "playlists"
    """
    def __init__(self, hal, filename):
        # Update internal instance variables
        self.hal = hal
        self.playlists = {}
        self.current_playlist = None
        self.current_playlist_length = 0
        self.current_track_folder = None
        self.current_track_number = None
        self.current_track_name = None
        self.current_track_length = None
        self.current_track_index = -1

        # Load file.  If it does not exist, handle it gracefully.
        try:
            f = open(filename)
            data = json.load(f)
            self.tracks = data['tracks']
            self.playlists = data['playlists']
            f.close()
        except:
            self.tracks = [["Error!", 0]]
            self.playlists['alle'] = []
            
        if self.tracks != None:
            # Expand folder playlists
            for playlist in self.playlists:
                if isinstance(self.playlists[playlist], int):
                    # Needs expansion
                    self.playlists[playlist] = self._find_tracks_in_folder(self.playlists[playlist])

            # Build playlist with all tracks in it
            self.playlists['alle'] = []
            for track in self.tracks:
                self.playlists['alle'].append((track[0], track[1]))
        # At this point all playlists are expanded and look the same.
        self.select_playlist('alle')
        print(self.tracks)
        print("\n",self.playlists)

    def _find_tracks_in_folder(self, folder_id):
        """ return a list of tracks in a folder as [(<folder_id>, <track_id>),...] """
        tmp = []
        for track in self.tracks:
            if track[0] == folder_id:
                tmp.append((track[0],track[1]))
        return tmp

    def _update_current_track(self, where):
        """ Find a track in the tracks data given a tuple (<folder_id>, <track_id>)
            Then update class state: current_track_name|length|folder|number
        """
        for track in self.tracks:
            if track[0] == where[0]:
                if track[1] == where[1]:
                    self.current_track_folder = track[0]
                    self.current_track_number = track[1]
                    self.current_track_name = track[2]
                    self.current_track_length = track[3]
        
    def get_track_folder(self, number=None):
        if number == None:
            return self.current_track_folder
        else:
            return self.tracks[number][0]

    def get_track_number(self, number=None):
        if number == None:
            return self.current_track_number
        else:
            return self.tracks[number][1]

    def get_track_name(self, number=None):
        if number == None:
            return self.current_track_name
        else:
            return self.tracks[number][2]
    
    def get_track_length(self, number=None):
        if number == None:
            return self.current_track_length
        else:
            return self.tracks[number][3]

    def get_number_of_tracks(self):
        """ Return length of the chosen playlist. """
        return len(self.playlists[self.current_playlist])
    
    def get_playlist_names(self):
        """ Return a list of the names of all playlists """
        return list(self.playlists.keys())

    def select_playlist(self, name):
        """ Update state with selected playlist. """
        self.current_playlist = name
        self.current_playlist_length = len(self.playlists[name])
        self.current_track_index = -1
        self.select_next_track()
        
    def select_next_track(self):
        """ Update current track with the next one from the selected playlist. """
        self.current_track_index = (self.current_track_index+1) % len(self.playlists[self.current_playlist])
        where = self.playlists[self.current_playlist][self.current_track_index]
        #print(f"idx: {self.current_track_index}, playlist: {self.current_playlist}")
        #print(f"folder:{where}")
        self._update_current_track(where)
        return (self.current_track_folder,
                self.current_track_number,
                self.current_track_name,
                self.current_track_length) 

    def select_track(self, folder_id, track_id):
        """ Update state with a specific track selection """
        self._update_current_track( (folder_id, track_id) )
        return (self.current_track_folder,
                self.current_track_number,
                self.current_track_name,
                self.current_track_length) 

    def play(self):
        """ Play the current track using the appropriate player function """
        if self.current_track_folder == 0:
            # root folder
            self.hal.play(self.current_track_number)
        elif self.current_track_folder == 100:
            # MP3 folder
            self.hal.play_mp3(self.current_track_number)
        elif self.current_track_folder == 200:
            # ADVERT folder
            self.hal.play_advert(self.current_track_number)
        else:
            # a numbered folder
            self.hal.play_folder(self.current_track_folder, self.current_track_number)

        self.print_track_info()

    def print_track_info(self):
        print(f"Playlist: {self.current_playlist}")
        print(f"Track info")
        print(f" Folder: {self.current_track_folder}/{self.current_track_number}")
        print(f" Name  : {self.current_track_name}")

    def __str__(self):
        print(self.tracks)
        print("\n",self.playlists)

# Run this file by itself...
if __name__ == '__main__':
    import HAL
    print("Running TrackManager as main.")
    hal = HAL.HAL()
    player = TrackManager(hal, "sdcard.json")
    hal.music.volume(1)
    player.select_playlist('mix')
    print(player.select_next_track())
    player.play()
