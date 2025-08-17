from graph.schema import CandidateGraphState
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance

# Load model once globally (so it doesn’t reload every function call)
model = SentenceTransformer('all-MiniLM-L6-v2')

def validate_answer_node(state: CandidateGraphState) -> CandidateGraphState:
    transcribed_text = state.get('transcribed_text', [])
    qa_pair = state.get('question_answer_pair', [])

    if not transcribed_text or not qa_pair:
        print("No transcribed text or question-answer pairs provided.")
        return {**state, "scores": []}

    scores = []

    for expected, given in zip(qa_pair, transcribed_text):
        ideal_ans = expected.get("expected_answer", "")

        if not given.strip():
            print(f"No answer provided for {expected['question_id']}")
            scores.append(0.0)
            continue

        try:
            # Encode both ideal and given answer
            vec_ideal = model.encode([ideal_ans])[0]
            vec_given = model.encode([given])[0]

            # Cosine similarity
            similarity = 1 - distance.cosine(vec_ideal, vec_given)

            # Scale similarity (0–1) to (1–10)
            score = round(similarity * 9 + 1, 2)

            scores.append(score)

        except Exception as e:
            print(f"Error scoring the answer for {expected['question_id']}: {e}")
            scores.append(0.0)

    return {**state, "scores": scores}
