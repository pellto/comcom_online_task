import os
import csv

import torch
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from transformers import AdamW, get_linear_schedule_with_warmup


class ConversationDataset(Dataset):
    def __init__(self, data_path):
        self.conversation_data = []
        self.end_of_text_token = "</s>"

        header = 0
        with open(data_path, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                if header == 0:
                    header += 1
                    continue
                _type = ["일상", "부정", "긍정"][int(row[2])]
                temp_converation = [f"{_type}: {row[0]}{self.end_of_text_token}", f"{row[1]}{self.end_of_text_token}"]
                self.conversation_data.append(temp_converation)

    def __len__(self):
        return len(self.conversation_data)

    def __getitem__(self, idx):
        return self.conversation_data[idx]


device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'


if __name__=="__main__":
    BATCH_SIZE = 1
    EPOCHS = 5
    LEARNING_RATE = 3e-5
    WARMUP_STEPS = 100
    MAX_SEQ_LEN = 100
    DATA_PATH = r"C:\Users\loveg\Downloads\Chatbot_data-master\ChatbotData.csv"
    MODEL_TYPE = "taeminlee/kogpt2"
    OUTPUT_FOLDER = r"E:\online_task"

    print("="*15, "LOAD MODEL", "="*15)
    model = GPT2LMHeadModel.from_pretrained(MODEL_TYPE)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_TYPE)

    print("=" * 15, "GET DATASET", "=" * 15)
    dataset = ConversationDataset(data_path=DATA_PATH)
    data_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    print("=" * 15, "MODEL ATTACH", "=" * 15)
    model = model.to(device)

    model.train()
    optimizier = AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = get_linear_schedule_with_warmup(optimizier, WARMUP_STEPS, len(data_loader) - WARMUP_STEPS, -1)

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    print("=" * 15, "TRAIN MODEL", "=" * 15)
    start_token = torch.tensor(tokenizer.encode("<s>")).unsqueeze(0)
    unknown_token = tokenizer.unk_token_id
    for epoch in range(EPOCHS):
        print(f'EPOCH : {epoch}, started' + "=" * 30)
        proc_seq_count = 0
        total_loss = 0.0
        total_count =0
        with tqdm(data_loader, desc="Train Epoch #{}".format(epoch)) as t:
            for idx, data in enumerate(t):
                try:
                    Q, A = tokenizer.encode(data[0][0]), tokenizer.encode(data[1][0])
                    for i in range(len(Q)):
                        if Q[i] > tokenizer.vocab_size:
                            Q[i] = unknown_token
                    for i in range(len(A)):
                        if A[i] > tokenizer.vocab_size:
                            A[i] = unknown_token

                    Q = torch.tensor(Q).unsqueeze(0)
                    A = torch.tensor(A).unsqueeze(0)
                    temp_conversation = torch.cat([Q, start_token, A], dim=1).to(device)

                    outputs = model(temp_conversation, labels=temp_conversation)
                    loss, logits = outputs[:2]
                    loss.backward()
                    total_loss += loss.detach().data
                    total_count += 1
                    t.set_postfix(loss='{:.6f}'.format(total_loss / total_count))

                    proc_seq_count += 1
                    if proc_seq_count == BATCH_SIZE:
                        proc_seq_count = 0
                        optimizier.step()
                        scheduler.step()
                        optimizier.zero_grad()
                        scheduler.optimizer.zero_grad()

                    if idx % 2000 == 1:
                        torch.save(model.state_dict(), os.path.join(OUTPUT_FOLDER, f"KoGPT2_KoDialog_{epoch}_{idx}.pt"))
                except :
                    print(data)
                    torch.save(model.state_dict(), os.path.join(OUTPUT_FOLDER, f"ERROR_{epoch}_{idx}.pt"))
            torch.save(model.state_dict(), os.path.join(OUTPUT_FOLDER, f"KoGPT2_KoDialog_{epoch}.pt"))
