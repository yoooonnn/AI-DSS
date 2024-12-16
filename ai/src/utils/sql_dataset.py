# ai/src/utils/sql_dataset.py

from torch.utils.data import Dataset

class SQLDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.tokenizer = tokenizer
        self.texts = texts
        self.labels = labels
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = str(self.labels[idx])

        # Add task-specific prefix to input text
        text = "translate English to SQL: " + text

        # Tokenize input text
        input_encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        # Tokenize target SQL query
        target_encoding = self.tokenizer(
            label,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": input_encoding["input_ids"].flatten(),
            "attention_mask": input_encoding["attention_mask"].flatten(),
            "labels": target_encoding["input_ids"].flatten()
        }

