import spacy
from spacy.lang.en import English
import numpy as np



spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

categories = ["urban","rural"]


text = """

Twenty students of a remote panchayat union school near Srivilliputtur had a rare opportunity of having a flight journey for the first time, thanks to their Headmaster, V. Jayachandran, who kept his promise.

“I had promised the students of class 5 that if they were regular to school without absenting themselves for frivolous reasons, I would take them for an air travel. When the students heeded to my advice, I had to keep my words,” says the Headmaster of Panchayat Union Primary School at Mangalam under Srivilliputtur Panchayat union.

The students of the small village often take leave for any functions at home or even for the temple festivals in any of the neighbouring villages.

“I thought the children were losing out on their studies. So, to motivate them, I told them that I will spend for their air travel. In the last four months, except for health reasons and other pressing needs, the children have not taken leave and their attendance has increased dramatically,” he said.

All the 5th class students — 9 boys and 11 girl — were taken to Chennai by train on Friday night. After two days of touring various places in Chennai, Mahabalipuram and zoo in Vandalur, the children were taken back on a flight journey from Chennai to Madurai,” he said.

“It was just fabulous,” said M. Swetha, a class 5 student, who for the first time had an air travel.

For all the children, for whom the nearest town Srivilliputtur itself is 13 km, a travel by Express train, the ride on Metro Train in Chennai and an air journey otherwise could have remained a dream for many of the students for several years.

The Headmaster, who has spent around ₹ 1.25 lakh for the travel, food and stay for the students and four teachers who accompanied them, says it was a pleasure giving something to the students.

“All my salary is only because of these children. I have spent only a portion of my salary to motivate them to come to school to become better citizens,” Mr. Jayachandran said.
"""

embeddings_index={}

def LoadEmbeddings():

    with open("glove.6B.100d.txt",encoding="utf8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            embed = np.array(values[1:], dtype=np.float32)
            embeddings_index[word] = embed
    print("Loaded %s word vectors." % len(embeddings_index))

def process(query,categories):
  
    scores = {}

    for category in categories:
        scores[category] = 0
  
    # import pdb; pdb.set_trace()
    for word in query:
        temp_score = {}
        for category in categories:
            try:
                query_embed = embeddings_index[word]
                embed = embeddings_index[category]
                dist = query_embed.dot(embed)
                temp_score[category]=dist
            #word does not exist
            except KeyError as e:
                print(str(e))
                temp_score[category] = 0
           
        # print(word,temp_score)

        max_category = categories[0]
        for category in temp_score:
            if temp_score[category]>temp_score[max_category]:
                max_category = category
        
        scores[max_category]+=(1/len(query))
    
    return scores


def classify(textinput):
    if embeddings_index == {}:
        LoadEmbeddings()
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = English()
    my_doc = nlp(textinput)
    # Create list of word tokens
    token_list = []
    for token in my_doc:

        if token.is_stop == False and token.text.isalpha():
            token_list.append(str.lower(token.text))
    return process(token_list,categories)
   

if __name__ == "__main__":
     
    print(classify(text))
    
