import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet as wn
from collections import defaultdict
import operator
import json

# Ensure NLTK resources are downloaded
nltk.download('wordnet')
nltk.download('stopwords')

def generate_summary(text, num_keywords=10):
    if not isinstance(text, str):
        return ["No lyrics available"]

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the text into words
    words = word_tokenize(text)
    
    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    filtered_words = [word.lower() for word in tokenizer.tokenize(text) if word.lower() not in stop_words]
    
    # Construct a graph representation of the text
    graph = defaultdict(list)
    for i in range(len(filtered_words) - 1):
        graph[filtered_words[i]].append(filtered_words[i+1])
        graph[filtered_words[i+1]].append(filtered_words[i])
    
    # Implement the TextRank algorithm
    scores = defaultdict(int)
    damping_factor = 0.85
    num_iterations = 10
    for _ in range(num_iterations):
        new_scores = defaultdict(int)
        for word in graph:
            score = 1 - damping_factor
            for neighbor in graph[word]:
                score += damping_factor * (scores[neighbor] / len(graph[neighbor]))
            new_scores[word] = score
        scores = new_scores
    
    # Select top keywords based on scores
    sorted_keywords = sorted(scores, key=scores.get, reverse=True)[:5]
    
    # Generate additional inferred keywords
    inferred_keywords = []
    for keyword in sorted_keywords:
        synsets = wn.synsets(keyword)
        if synsets:
            hypernyms = synsets[0].hypernyms()
            if hypernyms:
                inferred_word = hypernyms[0].lemmas()[0].name()
                if inferred_word not in filtered_words:
                    inferred_keywords.append(inferred_word)
            if len(inferred_keywords) >= 5:
                break

    # Combine and ensure we only have 10 unique keywords
    all_keywords = list(set(sorted_keywords + inferred_keywords))
    return all_keywords[:10]

# Load CSV and process
df = pd.read_csv('spotify_songs.csv', nrows=1000)

# Generate summaries and prepare the data structure
result_data = []
for _, row in df.iterrows():
    summary_keywords = generate_summary(row['lyrics'])
    entry = {
        'track_name': row['track_name'],
        'track_artist': row['track_artist'],
        'playlist_genre': row['playlist_genre'],
        'generated_summary': summary_keywords
    }
    result_data.append(entry)

# Save to JSON
with open('song_summaries.json', 'w') as f:
    json.dump(result_data, f, indent=4)

print("JSON file with song summaries has been created successfully.")
