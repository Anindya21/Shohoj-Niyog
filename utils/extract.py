import json
import re
import time

def extract_json_array(text: str) -> list:
    
    # Extract the first JSON-like array from the model output
    match = re.search(r"\[\s*{.*?}\s*\]", text, re.DOTALL)
    if not match:
        print("DEBUG: No JSON array found in output.")
        print("DEBUG: Raw output was:\n", text)
        raise ValueError("No JSON array found.")

    json_block = match.group()

    try:
        parsed = json.loads(json_block)
    except json.JSONDecodeError as e:
        print("First parsing failed. Trying to clean the JSON string...")
        # Soft cleaning: remove trailing commas and try again
        cleaned = re.sub(r",\s*}", "}", json_block)
        cleaned = re.sub(r",\s*\]", "]", cleaned)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            print("JSONDecodeError after cleanup:", e)
            print("DEBUG: Raw output was:\n", text)
            raise ValueError("Failed to extract valid JSON after cleanup.")

    # Validate and filter the objects
    qa_pairs = [
        item for item in parsed
        if isinstance(item, dict) and "question" in item and "answer" in item
    ]

    if not qa_pairs:
        print("DEBUG: JSON parsed but no valid question-answer pairs found.")
        print("DEBUG: Parsed JSON:", parsed)
        raise ValueError("No valid question-answer pairs in JSON array.")

    return qa_pairs