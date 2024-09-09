import os

import joblib
import numpy as np
import pandas as pd
import torch
import transformers
from transformers import AutoTokenizer
import logging

os.environ['TOKENIZERS_PARALLELISM'] = "false"
os.environ['clean_up_tokenization_spaces'] = "false"

PATH_2_MODEL = "/models/1_catboost_toxic_embedings_rubert_2.pkl"
RANDOM_STATE = 42
BERT_MODEL = {"toxic": {"model-name": "sismetanin/rubert-toxic-pikabu-2ch"}}

GLOBAL_MODEL = None
GLOBAL_BERT_MODEL = None


def build_bert_model(bert_config):
    global GLOBAL_BERT_MODEL

    if GLOBAL_BERT_MODEL is None:
        GLOBAL_BERT_MODEL = transformers.BertModel.from_pretrained(bert_config["model-name"])

    return GLOBAL_BERT_MODEL


def train_embedings_for(model, attention_mask, padded, batch_size=256):
    embeddings = []
    for i in range(padded.shape[0] // batch_size + 1):
        batch = torch.LongTensor(padded[batch_size * i:batch_size * (i + 1)])
        attention_mask_batch = torch.LongTensor(attention_mask[batch_size * i:batch_size * (i + 1)])

        with torch.no_grad():
            batch_embeddings = model(batch, attention_mask=attention_mask_batch)

        batch = batch_embeddings[0][:, 0, :].cpu() if torch.cuda.is_available() else batch_embeddings[0][:, 0, :]
        embeddings.append(batch.numpy())

    return embeddings


def get_attention_mask_and_padded_from(dataset, bert_config):
    tokenizer = AutoTokenizer.from_pretrained(bert_config["model-name"])

    tokenized = dataset['text'].apply(
        lambda x: tokenizer.encode(x, add_special_tokens=True, truncation=True, max_length=512))

    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)

    padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])
    attention_mask = np.where(padded != 0, 1, 0)

    return attention_mask, padded


def build_embedings(dataset, config):
    attention_mask, padded = get_attention_mask_and_padded_from(dataset, config)
    model = build_bert_model(config)
    embedings = train_embedings_for(model, attention_mask, padded, batch_size=64)
    return embedings


def load_model():
    global GLOBAL_MODEL
    if GLOBAL_MODEL is None:
        GLOBAL_MODEL = joblib.load(PATH_2_MODEL)

    return GLOBAL_MODEL


def check_toxic(text):
    best_model = load_model()

    test = pd.DataFrame([text], columns=['text'])
    logging.error(test)

    test_toxic_embeddings = build_embedings(test, BERT_MODEL["toxic"])
    toxic_features_test = np.concatenate(test_toxic_embeddings)
    test_predict = best_model.predict(toxic_features_test)
    return bool(test_predict[0]), text


if __name__ == "__main__":
    best_model = load_model()

    for i in [
        "да вы че?",
        "дурки?",
        "тупые",
        "молодцы",
        "Вы молодцы"]:
        print(check_toxic(i))
