from logics.graph.schema import CandidateGraphState
import datetime
import whisper
from functools import lru_cache
##agents/transcribe_answer.py

model = None

@lru_cache
def load_transcription_model():
    global model

    if model is None:
        model= whisper.load_model("tiny")
        options= whisper.DecodingOptions(language="en", fp16=True)
        print("Whisper model loaded successfully")

def transcribe_answer_node(state: CandidateGraphState) -> CandidateGraphState:
    
    load_transcription_model()

    video_files = state.get("video_files", None)

    if not video_files:
        print("No video files provided")
        return {
            **state,  # Keep all existing state
            "transcribed_text": [],
        }
    
    transcriptions = []
    
    for i, video in enumerate(video_files):
        try:
            print(f"Transciribing video {i+1}")
            result= model.transcribe(video) # Replace with actual captured video
            
            transcriptions.append(result["text"].strip())

            # existing_transcriptions = state.get("transcribed_text", [])
            # answers.append(result["text"])

            print(f"Transcription successful for video {i+1}")

        except:
            print(f"Transcription failed for video {i+1}")
            transcriptions.append("")
            
    return {
        **state,
        "transcribed_text": transcriptions,
    }