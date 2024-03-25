import os
import math
from typing import Optional
import pandas as pd


punctuation_marks: set[Optional[str]] = {',', '.', "", "", "", "", '!', '?', '"', "'", '-', ':', ';', '(', ')', '«', '»', '\n'}

# Read stop-words
with open('stop_words.txt', 'r', encoding='utf-8') as file:
    stop_words = set(map(lambda x: x.replace('\n', ''), file.readlines()))


# Clear the texts and string vectorization
def vectorization(file_path: str) -> pd.Series:
    words_vector = pd.Series(dtype="int")
    with open(file_path, 'r', encoding='utf-8') as file:
        text_lines = list(map(str.lower, file.readlines()))
        # Dropping a punctuation symbols
        for punctuation in punctuation_marks:
            text_lines = list(map(lambda x: x.replace(punctuation, ''), text_lines))
        # Vectorization
        for line in text_lines:
            for word in line.split():
                words_vector[word] = words_vector.get(word, 0) + 1
    return words_vector


words = pd.DataFrame()

# Data preprocessing
words["not spam"], words["spam"] = pd.Series(dtype=int), pd.Series(dtype=int)
for path in os.listdir('not_spam/'):
    vector = vectorization(file_path='not_spam/'+path)
    for word in vector.index:
        words.loc[word, "not spam"] = words.get((word, "not spam"), 0) + vector[word]
for path in os.listdir('spam/'):
    vector = vectorization(file_path='spam/'+path)
    for word in vector.index:
        words.loc[word, "spam"] = words.get((word, "spam"), 0) + vector[word]

# Deleting stop words
for stop_word in stop_words:
    if stop_word in words.index:
        words.drop(index=stop_word)


# The Bayes method with smoothing
def check(filename: str, not_spam_files_cnt: int, spam_files_cnt: int,
          words: pd.DataFrame = words, alpha: float = 0.8):
    words["target"] = vectorization(file_path='target/'+filename)
    words.fillna(value=0, inplace=True)

    spam_words_count = words["spam"].sum()
    not_spam_words_count = words["not spam"].sum()
    words_count = spam_words_count + not_spam_words_count

    spam_score = math.log(spam_files_cnt / (spam_files_cnt + not_spam_files_cnt))
    not_spam_score = math.log(not_spam_files_cnt / (spam_files_cnt + not_spam_files_cnt))

    for word in words[words["target"] > 0].index:
        spam_score += math.log((alpha + words.loc[word, "spam"])/(alpha*words_count + spam_words_count))
        not_spam_score += math.log((alpha + words.loc[word, "not spam"])/(alpha*words_count + not_spam_words_count))

    print(filename + " is " + ("spam" if spam_score > not_spam_score else "not spam"), end='')


if __name__ == "__main__":
    check(filename="file6.txt", spam_files_cnt=len(os.listdir("spam/")), not_spam_files_cnt=len(os.listdir("not_spam/")))
