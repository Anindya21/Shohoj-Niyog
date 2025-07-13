import datetime
import whisper

model= whisper.load_model("small")

options= whisper.DecodingOptions(language="en", fp16=False)
result= model.transcribe("test.mp4")

answer= result["text"]

print(answer)