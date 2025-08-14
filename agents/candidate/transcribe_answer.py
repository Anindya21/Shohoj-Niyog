from graph.schema import CandidateGraphState
import datetime
import whisper

##agents/transcribe_answer.py
def transcribe_answer_node(state: CandidateGraphState) -> CandidateGraphState:
    
    model= whisper.load_model("small")

    options= whisper.DecodingOptions(language="en", fp16=False)
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
            print(f"Transciribing {i} th video")
            result= model.transcribe(video) # Replace with actual captured video
            
            transcriptions.append(result["text"].strip())

            # existing_transcriptions = state.get("transcribed_text", [])
            # answers.append(result["text"])

            print(f"Transcription successful for video {i}")

        except:
            print(f"Transcription failed for video {i}")
            transcriptions.append("")
            
    return {
        **state,
        "transcribed_text": transcriptions,
    }