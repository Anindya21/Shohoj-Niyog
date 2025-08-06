from graph.schema import CandidateGraphState
import datetime
import whisper

##agents/transcribe_answer.py
def transcribe_answer_node(state: CandidateGraphState) -> CandidateGraphState:
    
    model= whisper.load_model("small")

    options= whisper.DecodingOptions(language="en", fp16=False)
    video_file = state.get("video_file", None)
    
    if not video_file:
        print("No video file provided")
        return {
            **state,  # Keep all existing state
            "transcribed_text": state.get("transcribed_text", []),
        }
    
    try:
        result= model.transcribe(video_file) # Replace with actual captured video
        existing_transcriptions = state.get("transcribed_text", [])
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