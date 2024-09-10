from yandex_gpt import YandexGPT, YandexGPTConfigManagerForIAMToken

config = YandexGPTConfigManagerForIAMToken()

yandex_gpt = YandexGPT(config_manager=config)


async def get_yandex_gpt_completion(text: str):
    messages = [{"role": "user", "text": text}]
    completion = await yandex_gpt.get_async_completion(messages=messages, timeout=60)
    return completion
