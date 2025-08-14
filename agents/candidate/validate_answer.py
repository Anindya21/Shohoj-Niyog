from graph.schema import CandidateGraphState
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import nltk
import numpy as np
nltk.download('punkt')

def validate_answer_node(state: CandidateGraphState) -> CandidateGraphState:
    
    def angular_similarity(vec1, vec2):
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(vec1, vec2) / (norm1 * norm2)

    
    transcribed_text = state['transcribed_text']

    qa_pair= state['question_answer_pair']

    if not transcribed_text or not qa_pair:
        print("No transcribed text or question-answer pairs provided.")
        return {
            **state,
            "score": []
        }

    scores = []

    for expected, given in zip(qa_pair, transcribed_text):
        ideal_ans= expected.get("expected_answer", "")
        
        if given == "":
            print(f"No answer provided for {expected['question_id']}")
            scores.append(0.0)
            continue
        
        try:
            tokenized_ideal = word_tokenize(ideal_ans.lower())
            tokenized_given = word_tokenize(given.lower())
            
            tagged_data = [
                TaggedDocument(words=tokenized_ideal, tags=["ideal"]),
                TaggedDocument(words=tokenized_given, tags=["given"])
            ]
            model = Doc2Vec(vector_size=100, window=4, min_count=1, workers=4, epochs=500)

            model.build_vocab(tagged_data)
            model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)        
        
            vec_ideal =model.infer_vector(tokenized_ideal)
            vec_given =model.infer_vector(tokenized_given)

            similarity = angular_similarity(vec_ideal, vec_given)
            score= float(similarity*9+1,2)

            scores.append(score)

        except:
            print(f"Error scoring the answer for {expected['question_id']}")
            scores.append(0.0)
        
    return{
        **state,
        "scores": scores
    }

        
    # ideal_ans = []
    # for each in data:
    #     ideal_ans.append(each['answer'])

    # given_ans = state['transcribed_text']
    
    # # Now to tokenize the data
    
    # tokenized_ideal = [word_tokenize(document.lower()) for document in ideal_ans]
    # tokenized_given = [word_tokenize(document.lower()) for document in given_ans]
    
    # tagged_data = [TaggedDocument(words=words, tags=[str(idx)]) for idx, words in enumerate(tokenized_ideal)]

    
    
    

    # scores= []

    # for each in range(len(tokenized_given)):
    #     vec_ideal =model.infer_vector(tokenized_ideal[each])
    #     vec_given =model.infer_vector(tokenized_given[each])

    #     similarity = angular_similarity(vec_ideal, vec_given)
    #     scores.append(similarity)


    # return {
    #     **state,
    #     "score": scores,
    #     }