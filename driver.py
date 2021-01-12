

def find_track(artist, track, spotify):
    try:
        track_info = spotify.search(q=f"artist:{artist} track:{track}", type='track')
        print(track_info)
        track_info_f = track_info['tracks']['items'][0]
    except:
        print("There was an error")
    else:
        return track_info_f


def show_tracks(track_info_f, spotify):
    artist = spotify.artist(track_info_f['artists'][0]['external_urls']['spotify'])
    album = spotify.album(track_info_f["album"]["external_urls"]["spotify"])

    print(f"\nArtist: {artist['name']}\n"
          f"Track: {track_info_f['name']}\n"
          f"Cover Art: {track_info_f['album']['images'][0]['url']}\n"
          f"Artist Genre: {artist['genres']}\n"
          # f"Album Genre: {album['genres']}\n"
          f"Release date: {album['release_date']}\n"
          f"Audio: {track_info_f['preview_url']}\n")


def get_tracks(track_info_f, spotify):

    artist = spotify.artist(track_info_f['artists'][0]['external_urls']['spotify'])
    album = spotify.album(track_info_f["album"]["external_urls"]["spotify"])

    # Returns track name, song features
    track_id = track_info_f['id']
    song_features = spotify.audio_features(track_id)

    song_features[0]['release_date'] = album['release_date'][:4]
    song_features[0]['genres'] = artist['genres']

    return track_info_f['name'], song_features[0]


def most_frequent(lst):
    counter = {}
    for ele in lst:
        if ele in counter:
            counter[ele] += 1
        else:
            counter[ele] = 1
    popular_lst = sorted(counter, key=counter.get, reverse=True)
    return popular_lst


def total_topic(favourites, topic):
    topic_list = []
    for song, features in favourites.items():
        for key, value in features.items():
            if key == topic:
                if topic == "genres":
                    for element in value:
                        topic_list.append(element)
                else:
                    topic_list.append(value)
    return topic_list


def get_user_playlist(user, uri, spotify, fields=None, market=None):
    tracks_dict = {}

    response = spotify.user_playlist_tracks(user, uri, fields=fields, limit=100, market=market)

    results = response['items']

    while len(results) < response["total"]:
        response = spotify.user_playlist_tracks(
            user, uri, fields=fields, limit=100, offset=len(results), market=market
        )
        results.extend(response['items'])

    # for result in results
    for result in results:
        track, features = get_tracks(result['track'], spotify)
        tracks_dict[track] = features

    return tracks_dict
