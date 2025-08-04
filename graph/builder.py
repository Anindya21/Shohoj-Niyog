##graph/builder.py

from langgraph.graph import StateGraph, END
from agents.ques_ans_gen import generate_question_and_answer_node 
from agents.transcribe_answer import transcribe_answer_node
from agents.validate_answer import validate_answer_node
from graph.schema import GraphState


def route_workflow(state:GraphState) -> str:
    """ Determine next step based on current state."""

    if state.get("video_file") and not state.get("question_answer_pairs"):
        return "transcribe_answer_node"
    
    else: 
        return "generate_question_and_answer_node"

def build_graph():

    builder= StateGraph(GraphState)
    builder.add_node("generate_question_and_answer_node", generate_question_and_answer_node)
    builder.add_node("transcribe_answer_node", transcribe_answer_node)
    # builder.add_node("validate_answer_node", validate_answer_node)  
    
    builder.set_conditional_entry_point(route_workflow)

    builder.add_conditional_edges(
        "generate_question_and_answer_node", 
        lambda state: "transcribe_answer_node" if state.get("video_file") else END

    )

    # builder.add_conditional_edges(
    #     "transcribe_answer_node",
    #     lambda state: "validate_answer_node" if state.get("question_answer_pairs") else END
    # )

    # builder.set_entry_point("generate_question_and_answer_node")
    # builder.add_edge("generate_question_and_answer_node", "transcribe_answer_node")
    # # builder.add_edge("transcribe_answer_node", "validate_answer_node")
    # # builder.add_edge("validate_answer_node",END)

    # builder.add_edge("transcribe_answer_node", END) # For testing only this node, REMOVE LATER
    graph= builder.compile()

    return graph