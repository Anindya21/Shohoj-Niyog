from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
 
def load_llm():
    device = 0 if torch.cuda.is_available() else -1

    tokenizer = AutoTokenizer.from_pretrained("context-labs/meta-llama-Llama-3.2-3B-Instruct-FP16")
    model = AutoModelForCausalLM.from_pretrained(
            "context-labs/meta-llama-Llama-3.2-3B-Instruct-FP16",
            torch_dtype=torch.float16,
            device_map="auto" if device == 0 else "cpu"
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
