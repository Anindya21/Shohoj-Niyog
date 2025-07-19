import os
from dotenv import load_dotenv
from graph.builder import build_graph
from IPython.display import Image, display

   
def main():
    print("Welcome to the Question Generator!")

    load_dotenv()
    
    hf_token = os.getenv("HF_TOKEN")

    if hf_token is None:
        raise ValueError("HF_TOKEN environment variable is not set. Please set it to your Hugging Face token.")

    role = input("Role: ").strip()
    stacks = input("Stacks: ").strip()
    level = input("Level: ").strip()

    inputs = {
        "role": role,
        "stacks": [s.strip() for s in stacks.split(",")],
        "level": level
    }

    graph= build_graph()
    # Get the graph object
    graph_prnt = graph.get_graph()

   # Option 1: Get a PNG image
    png = graph_prnt.draw_mermaid_png()
    display(Image(png))

   # Option 2: Get an ASCII representation
    ascii_graph = graph_prnt.draw_ascii()
    print(ascii_graph)


    result = graph.invoke(inputs)
    print("===For Debuggig===")
    print(result)
    print("====================")
    print("\nGenerated Questions:\n")
    for i, qa in enumerate(result["question_answer_pairs"], start=1):
        print(f"{i}. {qa['question']}")


if __name__ == "__main__":
    main()
