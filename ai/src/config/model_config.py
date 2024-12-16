# ai/src/config/model_config

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

class ModelConfig:

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

    model_name: str = "t5-small"
    max_length: int = 128
    train_batch_size: int = 8
    eval_batch_size: int = 8
    learning_rate: float = 3e-4
    num_train_epochs: int = 3
    warmup_steps: int = 500
    weight_decay: float = 0.01
    output_dir: str = os.path.join(base_dir, "outputs", "models")
    logging_dir: str = os.path.join(base_dir, "outputs", "logs")
    checkpoint_dir: str = os.path.join(base_dir, "outputs", "checkpoints")
    logging_steps: int = 10
    save_strategy: str = "epoch"
    eval_strategy: str = "epoch"