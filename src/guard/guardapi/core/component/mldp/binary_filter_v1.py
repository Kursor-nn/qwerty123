import os

import joblib
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

os.environ['TOKENIZERS_PARALLELISM'] = "false"
os.environ['clean_up_tokenization_spaces'] = "false"

PATH_2_MODEL = "/models/2_correct_check_text.pkl"
RANDOM_STATE = 42

GLOBAL_MODEL = None
GLOBAL_BERT_MODEL = None


def load_model():
    global GLOBAL_MODEL
    if GLOBAL_MODEL is None:
        GLOBAL_MODEL = joblib.load(PATH_2_MODEL)

    return GLOBAL_MODEL


model = AutoModelForSequenceClassification.from_pretrained("apanc/russian-inappropriate-messages")
tokenizer = AutoTokenizer.from_pretrained("apanc/russian-inappropriate-messages")


def check_toxic_2(message, model, tokenizer, device="cpu"):
    mapper = {0: False, 1: True}

    model.to(device)
    model.eval()

    with torch.no_grad():
        tokens = tokenizer(message, max_length=512, truncation=True, return_tensors="pt")
        return mapper[int(torch.argmax(model(**tokens).logits, dim=1))]


def check_toxic(text):
    return check_toxic_2(message=text, model=load_model(), tokenizer=tokenizer), text


if __name__ == "__main__":
    best_model = load_model()

    for i in [
        "да вы че?",
        "дурки?",
        "тупые",
        "молодцы",
        "Вы молодцы"]:
        print(check_toxic(i))
