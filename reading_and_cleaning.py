# this file is to read the comments and get only the relevant words for sentiment analysis
# #1 bag of words approach : getting only the adjectives from each comment
import json
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag

import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(THIS_FOLDER, 'idea_items.json')
# reading file idea_items.json
# input_file = 'C:\\Users\\Kanakaraj\\Desktop\\GRIDS project\\idea_items.json'
# downloading stopwords as given by nltk
stop_words = list(set(stopwords.words('english')))
# to filter out adjectives (adjectives have J in them)
allowed_word_types = ["J"]
comments_dict = {}
modified_comments = []


def tokenize(string):
    # removing punctuations and '\n' from the comments
    cleaned = re.sub(r'[^a-zA-Z\s]', '', string).replace('\n', '')
    # tokenizing sentences
    tokenized = word_tokenize(cleaned)
    # removing stopwords
    stopped = [w for w in tokenized if not (w in stop_words)]
    # POS tagging
    pos = pos_tag(stopped)
    # allowed_words being adjectives alone (do we need verbs? adverbs maybe)
    for w in pos:
        # pos format = (word, pos_tag): we get the pos_tag and check only the first letter to see if it's 'J'
        if w[1][0] in allowed_word_types:
            modified_comments.append(w[0].lower())
    return set(modified_comments)


def read_file_and_analyze(input_f):
    with open(input_f, 'r', encoding='utf8') as f:
        for line in f:
            data = json.loads(line)
            comments = data['comments']
            if not isinstance(comments, dict):
                comments_dict['Idea Name'] = data['ideaName'].replace('\u00a0', '').strip()
                # Also add the number vote up and vote down
                # comments_dict['Vote up'] = data['voteUpNumber']
                # comments_dict['Vote down'] = data['voteDownNumber']
                comments_dict['Words in comments'] = []
                comments_dict['Total vote'] = data['voteTotalNumber']
                for sent in comments:  # I am adding all the words of all the comments of one idea into one list
                    modified_comment = tokenize(sent['comment'])
                    if not modified_comment:  # if the list is empty
                        comments_dict.pop('Words in comments')
                        # comments_dict.pop('Vote up')
                        # comments_dict.pop('Vote down')
                        comments_dict.pop('Total vote')
                        comments_dict.pop('Idea Name')
                    else:
                        comments_dict['Words in comments'] += list(modified_comment)
                    break
            if comments:
                with open('positive.txt', 'a') as pos_files, open('negative.txt', 'a') as neg_files, open('neutral.txt', 'a') as neutral_files:
                    if comments_dict:
                        if comments_dict['Total vote'] > 0:
                            pos_files.write(json.dumps(comments_dict))
                            pos_files.write("\n")
                        elif comments_dict['Total vote'] < 0:
                            neg_files.write(json.dumps(comments_dict))
                            neg_files.write("\n")
                        else:
                            neutral_files.write(json.dumps(comments_dict))
                            neutral_files.write("\n")


read_file_and_analyze(input_file)
