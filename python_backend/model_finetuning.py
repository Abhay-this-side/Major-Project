import pandas as pd
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling

# Load the dataset
data = pd.read_csv("interview_questions.csv")

# Combine questions and topics if relevant, otherwise use questions only
data['combined'] = data['Question']  # Modify this line to add `Topic` if needed: data['Question'] + " " + data['Topic']

# Load the tokenizer and model
model_name = "decapoda-research/llama-7b-hf"  # Change this to the correct LLaMA model
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

# Tokenize the data
def tokenize_function(examples):
    return tokenizer(examples['combined'], padding="max_length", truncation=True, max_length=128)

# Create a Hugging Face Dataset from the data
from datasets import Dataset
dataset = Dataset.from_pandas(data)
tokenized_data = dataset.map(tokenize_function, batched=True)

# Define data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./llama-finetuned",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,  # Adjust based on GPU memory
    gradient_accumulation_steps=8,  # Increase if using larger batch sizes
    save_steps=500,
    save_total_limit=2,
    prediction_loss_only=True,
    logging_dir="./logs",
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data,
    data_collator=data_collator,
)

# Fine-tune the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained("./llama-finetuned")
tokenizer.save_pretrained("./llama-finetuned")

print("Fine-tuning complete. Model saved to './llama-finetuned'")
