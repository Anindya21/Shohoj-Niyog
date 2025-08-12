import os
from dotenv import load_dotenv
from graph.builder import build_candidate_graph, build_recruiter_graph
from IPython.display import Image, display

   
def main():
    print("Welcome to the Question Generator!")

    load_dotenv()
    
    hf_token = os.getenv("HF_TOKEN")

    if hf_token is None:
        raise ValueError("HF_TOKEN environment variable is not set. Please set it to your Hugging Face token.")

    # position = input("Position: ").strip()
    # stacks = input("Stacks: ").strip()
    # level = input("Level: ").strip()
    # num_questions= str(input("Number of Questions: ")).strip()

    # inputs = {
    #     "position": position,
    #     "stacks": [s.strip() for s in stacks.split(",")],
    #     "level": level,
    #     "num_questions":num_questions
    # }

    cand_graph= build_candidate_graph()
    recruiter_graph = build_recruiter_graph()
    # Get the graph object
    rec_graph_prnt = recruiter_graph.get_graph()
    cand_graph_prnt = cand_graph.get_graph()

   # Option 1: Get a PNG image
    # can_png = cand_graph_prnt.draw_mermaid_png()
    # rec_png = rec_graph_prnt.draw_mermaid_png()
    # display(Image(can_png))
    # display(Image(rec_png))

   # Option 2: Get an ASCII representation
    ascii_graph_can = cand_graph_prnt.draw_ascii()
    ascii_graph_rec = rec_graph_prnt.draw_ascii()
    print(ascii_graph_can)
    print(ascii_graph_rec)


    # result = graph.invoke(inputs)
    print("===For Debuggig===")
    # print(result)
    print("====================")
    # print("\nGenerated Questions:\n") 
    # for i, qa in enumerate(result["question_answer_pairs"], start=1):
    #     print(f"{i}. {qa['question']}")


if __name__ == "__main__":
    main()
