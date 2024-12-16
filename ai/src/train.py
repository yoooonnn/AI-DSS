# src/train.py
import os
import sys
from config.model_config import ModelConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from trainer.sql_trainer import SQLTrainer

def main():
    """
    Main function to run the training pipeline.
    Handles model configuration, data loading, and training execution.
    """

    # Load configuration
    config = ModelConfig()

    # Initialize trainer
    trainer = SQLTrainer(config)

    # Create output directories if they don't exist
    os.makedirs(config.output_dir, exist_ok=True)
    os.makedirs(config.logging_dir, exist_ok=True)
    os.makedirs(config.checkpoint_dir, exist_ok=True)

    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'query_data.json')
    print(file_path)
    try:

        # Load training data
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        
        # Prepare datasets
        train_dataset, val_dataset = trainer.prepare_data(json_data)
        
        # Train model
        trainer.train(train_dataset, val_dataset)
        
        # Test generation with sample input
        test_input = "Find all response to b2e6c6bdfa7c51ba3ada031b4a740baf509d72b3ab8e2272eac0919cd0af68d614766940eb8f60491c77ff762fa0bea5eb5fc87d8dacff0c413774e53a13c59441"
        generated_sql = trainer.generate_sql(test_input)
        print(f"Sample generation test:")
        print(f"Input: {test_input}")
        print(f"Generated SQL: {generated_sql}")
        
    except FileNotFoundError:
        print("Error: Training data file not found at data/train.json")
    except Exception as e:
        print(f"Error during training: {str(e)}")

if __name__ == "__main__":
    main()