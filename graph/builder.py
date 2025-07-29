from langgraph.graph import StateGraph, END
from agents.ques_ans_gen import generate_question_and_answer_node 
from agents.transcribe_answer import transcribe_answer_node
from agents.validate_answer import validate_answer_node
from graph.schema import GraphState


def build_graph():

    builder= StateGraph(GraphState)

    builder.add_node("generate_question_and_answer_node", generate_question_and_answer_node)
    builder.add_node("transcribe_answer_node", transcribe_answer_node)
    builder.add_node("validate_answer_node", validate_answer_node)  
    
    # builder.add_node("return_questions_only", return_questions_only)

    builder.set_entry_point("generate_question_and_answer_node")
    builder.add_edge("generate_question_and_answer_node", "transcribe_answer_node")
    builder.add_edge("transcribe_answer_node", "validate_answer_node")
    builder.add_edge("validate_answer_node",END)

    graph= builder.compile()

    return graph