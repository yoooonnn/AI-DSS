import torch
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
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        self.tokenizer = T5Tokenizer.from_pretrained(config.model_name, legacy=True)
        self.model = T5ForConditionalGeneration.from_pretrained(config.model_name)
        self.model.to(self.device)
        
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
            self.config.max_length,
            device=self.device
        )
        val_dataset = SQLDataset(
            val_texts, 
            val_labels, 
            self.tokenizer, 
            self.config.max_length,
            device=self.device
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
            learning_rate=self.config.learning_rate,
            no_cuda=False
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
        ).to(self.device)
        
        outputs = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=self.config.max_length,
            num_beams=4,
            early_stopping=True
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def save_model(self, save_dir=None):
        """
        Save the model and tokenizer to the specified directory.
        
        Args:
            save_dir: Directory path to save the model. If None, uses config.output_dir
        """
        if save_dir is None:
            save_dir = self.config.output_dir
            
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(save_dir, "model")
        self.model.save_pretrained(model_path)
        
        # Save tokenizer
        tokenizer_path = os.path.join(save_dir, "tokenizer")
        self.tokenizer.save_pretrained(tokenizer_path)
        
        # Save config as JSON
        config_path = os.path.join(save_dir, "config.json")
        config_dict = {k: v for k, v in vars(self.config).items() 
                      if not k.startswith('_')}
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=4)

        self.model.to(self.device)
            
    def load_model(self, load_dir):
        """
        Load a saved model, tokenizer, and configuration.
        
        Args:
            load_dir: Directory containing the saved model
        """
        # Load model
        model_path = os.path.join(load_dir, "model")
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        
        # Load tokenizer
        tokenizer_path = os.path.join(load_dir, "tokenizer")
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)
        
        # Load config
        config_path = os.path.join(load_dir, "config.json")
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
            for k, v in config_dict.items():
                setattr(self.config, k, v)

    def evaluate(self, val_dataset):
        """
        Evaluate the model on the validation dataset.
        
        Args:
            val_dataset: Validation dataset
            
        Returns:
            dict: Evaluation metrics
        """
        training_args = self.get_training_args()
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=None,  # Not needed for evaluation
            eval_dataset=val_dataset
        )
        
        # Evaluate model
        eval_results = trainer.evaluate()
        print(f"Evaluation results: {eval_results}")
        
        return eval_results