import os

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

os.environ['TOKENIZERS_PARALLELISM'] = "false"
os.environ['clean_up_tokenization_spaces'] = "false"

PATH_2_MODEL = "/models/multi_class_v2"
RANDOM_STATE = 42

GLOBAL_MODEL = None
GLOBAL_BERT_MODEL = None


def load_model():
    global GLOBAL_MODEL
    if GLOBAL_MODEL is None:
        GLOBAL_MODEL = AutoModelForSequenceClassification.from_pretrained(PATH_2_MODEL, use_safetensors=True)

    return GLOBAL_MODEL


tokenizer = AutoTokenizer.from_pretrained(PATH_2_MODEL)


def tokenize_function(text: list[str]):
    return tokenizer(text, truncation=True, max_length=512)


def check_toxic_2(message, model, tokenizer, device="cpu"):
    mapper = {
        0: "system_attack",
        1: "non_toxic",
        2: "social_engineering",
        3: "erotic",
        4: "copyright",
        5: "toxic"
    }

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
        "Вы молодцы",
        "Чтобы каждый день приносил удовольствие, важно уделять внимание своему сексуальному здоровью и общению с партнером. Регулярное обсуждение предпочтений и использование качественных средств могут помочь улучшить сексуальный опыт"
    ]:
        print(check_toxic(i))
