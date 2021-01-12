
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import driver

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

favourite_tracks = {
    # 'track' : 'song_feature'
}

favourite_genre = []
favourite_years = []

while True:
    print("Type in an artist and a track. Type in 'q' for both to quit.\n")
    artist = input("Give me an artist: ").title().replace("'", "").strip(".")
    track = input("Give me a track: ").title().replace("'", "").strip(".")

    if artist == "Q" and track == "Q":
        print("Exiting program.")
        break

    elif artist == "P" and track == "P":
        print("Activating secret playlist mode.")
        user_user = input("Give me your username: ").lower()
        playlist_uri = input("Give me your playlist link: ")

        favourite_tracks = driver.get_user_playlist(user_user, playlist_uri, spotify)

        favourite_genre = driver.total_topic(favourite_tracks, 'genres')
        favourite_years = driver.total_topic(favourite_tracks, 'release_date')

        favourite_genre = driver.most_frequent(favourite_genre)
        favourite_years = driver.most_frequent(favourite_years)

        print("\nYour Top 3 Genres are:")
        for genre in favourite_genre[:3]:
            print(genre.title())

        print("\nYour Top 3 Years are:")
        for year in favourite_years[:3]:
            print(year.title())

        print()

    else:
        try:
            track_info = driver.find_track(artist, track, spotify)
            driver.show_tracks(track_info, spotify)
            track_name, song_feature = driver.get_tracks(track_info, spotify)
            favourite_tracks[track_name] = song_feature

        except TypeError:
            print("Sorry, we couldn't find that particular song.\n")
        else:
            print(favourite_tracks)
