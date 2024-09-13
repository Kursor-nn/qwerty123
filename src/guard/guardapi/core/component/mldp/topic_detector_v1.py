import os

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

os.environ['TOKENIZERS_PARALLELISM'] = "false"
os.environ['clean_up_tokenization_spaces'] = "false"

PATH_2_MODEL = "/models/output_topic_detector_service/"
RANDOM_STATE = 42

GLOBAL_MODEL = None
GLOBAL_BERT_MODEL = None


def load_model():
    global GLOBAL_MODEL
    if GLOBAL_MODEL is None:
        GLOBAL_MODEL = AutoModelForSequenceClassification.from_pretrained(PATH_2_MODEL, num_labels=7, ignore_mismatched_sizes=True)

    return GLOBAL_MODEL


tokenizer = AutoTokenizer.from_pretrained("apanc/russian-inappropriate-messages")


def tokenize_function(text: list[str]):
    return tokenizer(text, truncation=True, max_length=512)


def check_toxic_2(message, model, tokenizer, device="cpu"):
    mapper = {0: 'insult',
              1: 'politics',
              2: 'xenos',
              3: 'malware',
              4: 'neutral',
              5: 'violence',
              6: 'misinformation'}

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
        print(check_toxic(i)[0])
