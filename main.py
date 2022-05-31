import os
import math

NOT_SPAM_DIRECTORY = 'not_spam_text/'
SPAM_DIRECTORY = 'spam_text/'
TEST_DIRECTORY = 'test_text/'
not_spam_files = os.listdir(NOT_SPAM_DIRECTORY)
spam_files = os.listdir(SPAM_DIRECTORY)
test_files = os.listdir(TEST_DIRECTORY)

punctuation_marks = [',', '.', "", "", "", "", '!', '?', '"', "'", '-', ':', ';', '(', ')', '«', '»', '\n']
stop_words = []  # стоп слова используются слишком часто (местоимения, союзы, частицы и т.п.) и делают предсказания менее точными
words = {}

with open('stop_words.txt', 'r', encoding='utf-8') as file:
    for i in file.readlines():
        stop_words.append(i.replace('\n', ''))

for f in not_spam_files:
    with open(NOT_SPAM_DIRECTORY + f, 'r', encoding='utf-8') as file:
        lyric = file.readlines()  # массив строчек каждого отдельного файла
        lyric = list(map(str.lower, lyric))  # перевод текста в нижний регистр
        for i in punctuation_marks:
            for j in range(len(lyric)):
                lyric[j] = lyric[j].replace(i, '')  # удаление знаков препинания
        for j in lyric:  # j - строка файла
            k = j.split()  # k - лист слов в каждой строке
            for word in k:
                if word in words.keys():
                    words[word][0] += 1  # увеличение счетчика (рока) в словаре

                else:
                    words[word] = [1, 0, 0]  # добавление слова в словарь

for f in spam_files:
    with open(SPAM_DIRECTORY + f, 'r', encoding='utf-8') as file:
        lyric = file.readlines()  # массив строчек каждого отдельного файла
        lyric = list(map(str.lower, lyric))  # перевод текста в нижний регистр
        for i in punctuation_marks:
            for j in range(len(lyric)):
                lyric[j] = lyric[j].replace(i, '')  # удаление знаков препинания
        for j in lyric:  # j - строка файла
            k = j.split()  # k - лист слов в каждой строке
            for word in k:
                if word in words.keys():
                    words[word][1] += 1  # увеличение счетчика (рока) в словаре
                else:
                    words[word] = [0, 1, 0]  # добавление слова в словарь

words = dict(sorted(words.items(), key=lambda x: x[1], reverse=True))  # таблица частот

for stop in stop_words:
    if stop in words.keys():
        del words[stop]  # чистка от стоп-слов

count_of_not_spam_words = 0
count_of_spam_words = 0
total_count_of_words = 0

for key in words.keys():
    total_count_of_words = len(words.keys())
    count_of_not_spam_words += words[key][0]
    count_of_spam_words += words[key][1]

for f in test_files:
    copy_words = words.copy()
    with open(TEST_DIRECTORY + f, 'r', encoding='utf-8') as file:
        lyric = file.readlines()  # массив строчек каждого отдельного файла
        lyric = list(map(str.lower, lyric))  # перевод текста в нижний регистр
        for i in punctuation_marks:
            for j in range(len(lyric)):
                lyric[j] = lyric[j].replace(i, '')  # удаление знаков препинания
        for j in lyric:  # j - строка файла
            k = j.split()  # k - лист слов в каждой строке
            for word in k:
                if word in copy_words.keys():
                    copy_words[word][2] += 1  # увеличение счетчика (рока) в словаре
                else:
                    copy_words[word] = [0, 0, 1]  # добавление слова в словарь

        alpha = 1  # коэффицент сглаживания (0<alpha<=1)
        not_spam_score = math.log(len(not_spam_files) / (len(not_spam_files) + len(spam_files)))
        spam_score = math.log(len(spam_files) / (len(not_spam_files) + len(spam_files)))
        for key in copy_words.keys():
            not_spam_score += copy_words[key][2] * \
                              math.log((alpha + copy_words[key][0]) / (
                                          alpha * total_count_of_words + count_of_not_spam_words))
            spam_score += copy_words[key][2] * \
                          math.log((alpha + copy_words[key][1]) / (alpha * total_count_of_words + count_of_spam_words))
        # так как произведение вероятностей крайне малое значение, то заменяем его суммой логарифмов
        print(f + " is ", end='')
        if spam_score > not_spam_score:
            print(f'spam')
        else:
            print(f'not-spam')
