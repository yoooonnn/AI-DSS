# ai/src/config/model_config

class ModelConfig:
    model_name: str = "t5-small"
    max_length: int = 128
    train_batch_size: int = 8
    eval_batch_size: int = 8
    learning_rate: float = 3e-4
    num_train_epochs: int = 3
    warmup_steps: int = 500
    weight_decay: float = 0.01
    output_dir: str = "../outputs/results"     # 변경
    logging_dir: str = "../outputs/logs"       # 변경
    checkpoint_dir: str = "../outputs/checkpoints"  # 추가
    logging_steps: int = 10
    save_strategy: str = "epoch"
    eval_strategy: str = "epoch"