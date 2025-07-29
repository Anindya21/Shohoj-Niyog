from graph.schema import GraphState
import datetime
import whisper

def transcribe_answer_node(state: GraphState) -> GraphState:
    
    model= whisper.load_model("small")

    options= whisper.DecodingOptions(language="en", fp16=False)
    result= model.transcribe("test.mp4")

    try:
        answers.append(result["text"])

        print("Transcription successful")

    except:
        answers = []
        answer= result["text"]
        answers.append(answer)
        
        print("Transcription Successful in except block")

    return {
        **state,
        "transcribed_text": answers,
    }