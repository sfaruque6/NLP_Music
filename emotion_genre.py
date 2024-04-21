import pandas as pd

df = pd.read_csv('spotify_top_200_charts.csv')

def generate_playlist(emotion, genre):
    if emotion.lower() == 'happy':
        target_bpm = 150
    elif emotion.lower() == 'sad':
        target_bpm = 60
    elif emotion.lower() == 'mad':
        target_bpm = 130
    elif emotion.lower() == 'normal':
        target_bpm = 140
    else:
        print("Invalid emotion. Please enter 'happy', 'sad', 'mad', or 'regular'.")
        return

    filtered_df = df[df['Top Genre'].str.lower() == genre.lower()]

    if filtered_df.empty:
        print(f"No songs found in the '{genre}' genre.")
        return

    closest_songs = filtered_df.iloc[(filtered_df['Beats Per Minute (BPM)'] - target_bpm).abs().argsort()[:5]]
    closest_songs = closest_songs.sort_values(by='Popularity', ascending=False)

    print(f"Playlist for {emotion} emotion with closest BPM to {target_bpm} in the '{genre}' genre:")
    for index, row in closest_songs.iterrows():
        print(f"{row['Title']} by {row['Artist']} (BPM: {row['Beats Per Minute (BPM)']})")

emotion = input("Enter the emotion you are feeling (happy, sad, mad, regular): ")
genre = input("Enter the genre of music you want: ")
generate_playlist(emotion, genre)
