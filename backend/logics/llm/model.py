from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
 
def load_llm():
    device = 0 if torch.cuda.is_available() else -1

    tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct-bnb-4bit")
    model = AutoModelForCausalLM.from_pretrained(
            "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
            torch_dtype=torch.float16,
            device_map="auto" if device == 0 else "cpu",
            offload_folder="offload",
            )

    pipe = pipeline(
                task="text-generation", 
                model=model,
                tokenizer=tokenizer, 
                model_kwargs={"torch_dtype": torch.float16},
                max_new_tokens=1024,
                truncation=True
                )
    
    return HuggingFacePipeline(pipeline=pipe)
