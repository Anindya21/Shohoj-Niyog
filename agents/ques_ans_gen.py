from llm.model import load_llm
from llm.prompts import SYSTEM_PROMPTS
from utils.extract import extract_json_array
from graph.schema import GraphState

##agents/ques_ans_gen.py

llm= load_llm()


def generate_question_and_answer_node(state: GraphState) -> GraphState:
    prompts= (
        f"{SYSTEM_PROMPTS}\n\n"
        f"Position: {state['position']}\n"
        f"Stacks: {state['stacks']}\n"
        f"Level: {state['level']}\n"
        f"Number Of Questions: {state['num_questions']}"
    )

    for attempt in range(3):
        response = llm.invoke(prompts)
        raw_output = response[0]["generated_text"] if isinstance(response, list) else str(response)
        try:
            qa_pairs = extract_json_array(raw_output)
            break  # Success
        except ValueError as e:
            print(f"Attempt {attempt+1} failed, retrying...")
    else:
        raise ValueError("All attempts failed to produce valid JSON.")

    
    return {
        **state,
        "question_answer_pairs": qa_pairs
    }
