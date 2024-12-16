class SQLDataset:
    def __init__(self, texts, labels, tokenizer, max_length, device='cpu'):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.device = device

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        # Prepare input
        input_text = "translate English to SQL: " + text
        
        # Tokenize input and label
        inputs = self.tokenizer(
            input_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        labels = self.tokenizer(
            label,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        # Move tensors to specified device
        return {
            'input_ids': inputs['input_ids'].squeeze().to(self.device),
            'attention_mask': inputs['attention_mask'].squeeze().to(self.device),
            'labels': labels['input_ids'].squeeze().to(self.device)
        }