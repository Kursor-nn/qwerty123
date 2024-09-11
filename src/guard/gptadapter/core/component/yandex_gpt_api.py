from yandex_gpt import YandexGPT, YandexGPTConfigManagerForIAMToken, YandexGPTConfigManagerForAPIKey
from decouple import config

model_type = config("YANDEX_GPT_MODEL_TYPE")
catalog_type_id = config("YANDEX_GPT_CATALOG_ID")
api_key = config("YANDEX_GPT_API_KEY")
config = YandexGPTConfigManagerForAPIKey(model_type=model_type, catalog_id=catalog_type_id, api_key=api_key)

yandex_gpt = YandexGPT(config_manager=config)


def get_yandex_gpt_completion(text: str):
    messages = [{"role": "user", "text": text}]
    completion = yandex_gpt.get_async_completion(messages=messages, timeout=60)
    return completion
