from langchain_huggingface import HuggingFacePipeline
# from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from logics.llm.prompts import SYSTEM_PROMPTS
# import torch
import requests
import json
from dotenv import load_dotenv
import os



def load_llm():
  
  load_dotenv()
    
  openapi_key = os.getenv("openapi_key")

  url="https://openrouter.ai/api/v1/chat/completions"

  model= "meta-llama/llama-3.3-70b-instruct:free"
  
  
  def invoke(prompt: str):
    
    payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPTS},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 1024,
            "temperature": 0.7,
        }
    
    headers={
                "Authorization": f"Bearer {openapi_key}",
                "Content-Type": "shohoj_niyog/json",
                }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]
  
  return type("LLMWrapper", (), {"invoke": staticmethod(invoke)})()


# For offline usage (local model)

# def load_llm():
#     device = 0 if torch.cuda.is_available() else -1

#     tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-3B-Instruct-bnb-4bit")
#     model = AutoModelForCausalLM.from_pretrained(
#             "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
#             torch_dtype=torch.float16,
#             device_map="auto" if device == 0 else "cpu",
#             offload_folder="offload",
#             )

#     pipe = pipeline(
#                 task="text-generation", 
#                 model=model,
#                 tokenizer=tokenizer, 
#                 model_kwargs={"torch_dtype": torch.float16},
#                 max_new_tokens=1024,
#                 truncation=True
#                 )
    
#     return HuggingFacePipeline(pipeline=pipe)
