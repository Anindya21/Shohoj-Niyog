##graph/builder.py

from langgraph.graph import StateGraph, END
from logics.agents.recruiter.ques_ans_gen import generate_question_and_answer_node 
from logics.agents.recruiter.save_to_db import save_qa_pairs_node

from logics.agents.candidate.load_qa import load_qa_node
from logics.agents.candidate.transcribe_answer import transcribe_answer_node
from logics.agents.candidate.validate_answer import validate_answer_node
from logics.agents.candidate.save_response import save_response_node
from logics.graph.schema import RecruiterGraphState, CandidateGraphState


def build_recruiter_graph():

    builder= StateGraph(RecruiterGraphState)
    builder.add_node("generate_question_and_answer_node", generate_question_and_answer_node)
    builder.add_node("save_qa_pairs_node", save_qa_pairs_node)
    
    builder.set_entry_point("generate_question_and_answer_node")
    builder.add_edge("generate_question_and_answer_node", "save_qa_pairs_node")
    
    builder.add_edge("save_qa_pairs_node", END) 
    recruiter_graph= builder.compile()

    return recruiter_graph

def build_candidate_graph():

    builder= StateGraph(CandidateGraphState)

    builder.add_node("load_qa_node", load_qa_node)
    builder.add_node("transcribe_answer_node", transcribe_answer_node)
    builder.add_node("validate_answer_node", validate_answer_node)
    builder.add_node("save_candidate_response_node", save_response_node)

    builder.set_entry_point("load_qa_node")
    builder.add_edge("load_qa_node","transcribe_answer_node")
    builder.add_edge("transcribe_answer_node","validate_answer_node")
    builder.add_edge("validate_answer_node", "save_candidate_response_node")
    builder.add_edge("save_candidate_response_node",END)

    candidate_graph= builder.compile()
    return candidate_graph
