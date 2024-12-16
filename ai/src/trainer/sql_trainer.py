# ai/src/train/sql_trainer.py

from transformers import (
   T5ForConditionalGeneration, 
   T5Tokenizer,
   Trainer,
   TrainingArguments
)
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.sql_dataset import SQLDataset

class SQLTrainer:
   """
   Trainer class for SQL translation model that handles the complete training pipeline
   including data preparation, model training, and inference.
   """
   def __init__(self, config):
       """
       Initialize trainer with configuration.
       
       Args:
           config: Configuration object containing model parameters
       """
       self.config = config
       self.tokenizer = T5Tokenizer.from_pretrained(config.model_name, legacy=True)
       self.model = T5ForConditionalGeneration.from_pretrained(config.model_name)
       
   def prepare_data(self, json_data):
       """
       Prepare training and validation datasets from JSON data.
       
       Args:
           json_data: Input JSON data containing training examples
           
       Returns:
           tuple: Training and validation datasets
       """
       data = json.loads(json_data)
       df = pd.DataFrame(data["dataset"])
       
       # Split data into train and validation sets
       train_texts, val_texts, train_labels, val_labels = train_test_split(
           df["input"].tolist(),
           df["output"].tolist(),
           test_size=0.2,
           random_state=42
       )
       
       # Create dataset objects
       train_dataset = SQLDataset(
           train_texts, 
           train_labels, 
           self.tokenizer, 
           self.config.max_length
       )
       val_dataset = SQLDataset(
           val_texts, 
           val_labels, 
           self.tokenizer, 
           self.config.max_length
       )
       
       return train_dataset, val_dataset

   def get_training_args(self):
       """
       Get training arguments for the Trainer.
       
       Returns:
           TrainingArguments: Configured training arguments
       """
       return TrainingArguments(
           output_dir=self.config.output_dir,
           num_train_epochs=self.config.num_train_epochs,
           per_device_train_batch_size=self.config.train_batch_size,
           per_device_eval_batch_size=self.config.eval_batch_size,
           warmup_steps=self.config.warmup_steps,
           weight_decay=self.config.weight_decay,
           logging_dir=self.config.logging_dir,
           logging_steps=self.config.logging_steps,
           eval_strategy=self.config.eval_strategy,
           save_strategy=self.config.save_strategy,
           load_best_model_at_end=True,
           learning_rate=self.config.learning_rate
       )

   def train(self, train_dataset, val_dataset):
       """
       Train the model using the provided datasets.
       
       Args:
           train_dataset: Training dataset
           val_dataset: Validation dataset
           
       Returns:
           Trainer: Trained model trainer
       """
       training_args = self.get_training_args()
       
       trainer = Trainer(
           model=self.model,
           args=training_args,
           train_dataset=train_dataset,
           eval_dataset=val_dataset
       )
       
       trainer.train()
       
       return trainer

   def generate_sql(self, input_text):
       """
       Generate SQL query from input text using the trained model.
       
       Args:
           input_text: Input text query
           
       Returns:
           str: Generated SQL query
       """
       input_text = "translate English to SQL: " + input_text
       
       inputs = self.tokenizer(
           input_text,
           max_length=self.config.max_length,
           padding="max_length",
           truncation=True,
           return_tensors="pt"
       )
       
       outputs = self.model.generate(
           input_ids=inputs["input_ids"],
           attention_mask=inputs["attention_mask"],
           max_length=self.config.max_length,
           num_beams=4,
           early_stopping=True
       )
       
       return self.tokenizer.decode(outputs[0], skip_special_tokens=True)