from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

class ExerciseRequest(BaseModel):
    exercise_name: str

@app.post('/get_exercise_info')
async def get_exercise_info(request: ExerciseRequest):
    prompt = f"I want you to write a 50-words description of the exercise named '{request.exercise_name}' in the first paragraph of your response, followed by a clear list of 4 steps on how to perform this exercise. After the description paragraph, there should be a paragraph for step 1, then a paragraph for step 2, and a paragraph of every step till step 4. The paragraphs should be seperable by \n\n. Your answer should be in such a manner that i can programmatically get the description and the list of steps like this:  # Extract the text from the first choice and strip any excess whitespace text = response.choices[0].message.content.strip() # Split the text by double newlines to separate paragraphs parts = text.split('\n\n') description = parts[0]  # The first paragraph is the description steps = parts[1:]      # The remaining paragraphs are the steps. Be precise and intellectual in your answer and follow my instructions carefully."
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            max_tokens=250
        )
        
         # Extract the text from the first choice and strip any excess whitespace
        text = response.choices[0].message.content.strip()
        
        # Split the text by double newlines to separate paragraphs
        parts = text.split('\n\n')
        description = parts[0]  # The first paragraph is the description
        steps = parts[1:]     # The remaining paragraphs are the steps
        # Assuming 'steps' currently contains one string with all steps separated by '\n'
        steps_string = steps[0]  # This gets the single string that contains all steps.

        # Split this string on '\n' to create a list where each element is a step
        individual_steps = steps_string.split('\n')

        return {"description": description, "steps": individual_steps}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
