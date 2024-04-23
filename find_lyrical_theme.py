import json

def search_word_in_songs(word):
    result = []
    with open('song_summaries.json', 'r') as f:
        data = json.load(f)
        for entry in data:
            if any(word in summary.lower() for summary in entry["generated_summary"]):
                result.append((entry["track_artist"], entry["track_name"]))
    return result if result else None

def main():
    word = input("Enter a word to search in song summaries: ").strip().lower()
    search_result = search_word_in_songs(word)
    if search_result:
        print("The word '{}' is found in the following songs:".format(word))
        for artist, song in search_result:
            print("Artist: {}, Song: {}".format(artist, song))
    else:
        print("No song available with the word '{}' in its summary.".format(word))

if __name__ == "__main__":
    main()
