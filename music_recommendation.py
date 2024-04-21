
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet as wn
from collections import defaultdict
import operator

# Ensure NLTK resources are downloaded
nltk.download('wordnet')
nltk.download('stopwords')


def generate_summary(text, num_keywords=10):
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
            # Add hypernyms of the first sense of the word
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

# Example usage
text = """
There's a pain within that I can't define
There's an empty space where your love used to shine
From the night we met 'til the day you died
Do you think I wished?
Do you still believe I tried?
All too soon we were divided
And life had just begun
Will you revive from the chaos in my mind
Where we still are bound together?
Will you be there waiting by the gates of dawn
When I close my eyes forever?
I belong to you, you belong to me
It's the way things are, always meant to be
Like the morning star and the rising sun
You convey my life and forgive me what I've done
All too soon we were divided
Into darkness and light
Will you revive from the chaos in my mind
Where we still are bound together?
Will you be there waiting by the gates of dawn
When I close my eyes forever?
Save me
Reverse how I'm thinking of you
Every breath I take brings me closer
Closer to forever, to you
I'm waiting for the day that I'm gone!
All too soon we were divided
And life had just begun
Will you revive from the chaos in my mind
Where we still are bound together?
Will you be there waiting by the gates of dawn
When I close my eyes forever?
Will you be there waiting by the gates of dawn
When I close my eyes forever?
"""

summary = generate_summary(text, 1)
print("Summary:")
print(summary)