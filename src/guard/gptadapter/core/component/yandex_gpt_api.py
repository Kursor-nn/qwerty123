from dotenv import load_dotenv
from yandex_gpt import YandexGPT, YandexGPTConfigManagerForIAMToken

# Load environment variables
load_dotenv('/Users/alexanderkozachuk/work/learning/itmo/1_hacktone/qwerty123/src/guard/gptadapter/.env')

# Setup configuration (input fields are empty, because iam_token will be generated from environment variables)
config = YandexGPTConfigManagerForIAMToken()

yandex_gpt = YandexGPT(config_manager=config)


async def get_yandex_gpt_completion(text: str):
    messages = [{"role": "user", "text": text}]
    completion = await yandex_gpt.get_async_completion(messages=messages)
    return completion
