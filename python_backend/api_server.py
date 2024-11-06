from fastapi import FastAPI
from pydantic import BaseModel
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch

# Load the fine-tuned model and tokenizer
model_name = "llama_finetune.bin"  # Replace with the path to your fine-tuned model
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

# Initialize FastAPI
app = FastAPI()

# Define a Pydantic model to parse incoming data
class QuestionRequest(BaseModel):
    question: str

# Define an API endpoint for generating a response from the model
@app.post("/generate/")
async def generate_answer(request: QuestionRequest):
    # Encode the input question
    input_text = f"Q: {request.question} A:"
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate a response using the model
    with torch.no_grad():
        outputs = model.generate(inputs['input_ids'], max_length=200, num_return_sequences=1)

    # Decode the output
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract the answer part (after the "A:" part)
    question_answer = answer.split("A:")[1].strip() if "A:" in answer else answer.strip()

    # Return the question along with the generated answer as a JSON response
    return {"question": request.question, "answer": question_answer}

# Run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
