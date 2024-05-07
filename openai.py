from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()
openai.api_key = os.getenv('OPENAI_API_KEY')

class ExerciseRequest(BaseModel):
    exercise_name: str

@app.post('/get_exercise_info')
async def get_exercise_info(request: ExerciseRequest):
    prompt = f"Write a max 50-words description of the exercise named '{request.exercise_name}', followed by a clear list of 4 steps numbered sequentially on how to perform it.Your answer should be in such a manner that i can programmatically get the description and steps like this:parts = text.split('\n')description = parts[0]steps = parts[1:]"
    
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=200
        )
        text = response['choices'][0]['text'].strip()
        
        # Assuming the text format is a description followed by steps numbered 1 to 4
        parts = text.split('\n')
        description = parts[0]
        steps = parts[1:]

        return {"description": description, "steps": steps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
