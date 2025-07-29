from graph.schema import GraphState
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import nltk
import numpy as np
nltk.download('punkt')


def validate_answer_node(state: GraphState) -> GraphState:
    
    def angular_similarity(vec1, vec2):
        cosine_sim = np.dot(vec1, vec2)/ (np.linalg.norm(vec1)* np.linalg.norm(vec2))
        angular_sim = 1- np.arccos(cosine_sim)/ np.pi

        return angular_sim

    data = state['question_answer_pairs']

    ideal_ans = []
    for each in data:
        ideal_ans.append(each['answer'])

    given_ans = state['transcribed_text']

    # Now to tokenize the data

    tokenized_ideal = [word_tokenize(document.lower()) for document in ideal_ans]

    tokenized_given = [word_tokenize(document.lower()) for document in given_ans]
    
    tagged_data = [TaggedDocument(words=words, tags=[str(idx)]) for idx, words in enumerate(tokenized_ideal)]

    model = Doc2Vec(vector_size=100, window=4, min_count=1, workers=4, epochs=500)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)

    scores= []

    for each in range(len(tokenized_given)):
        vec_ideal =model.infer_vector(tokenized_ideal[each])
        vec_given =model.infer_vector(tokenized_given[each])

        similarity = angular_similarity(vec_ideal, vec_given)
        scores.append(similarity)


    return {
        **state,
        "score": scores,
        }