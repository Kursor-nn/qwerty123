# qwerty123

qwerty123 — это сервис для мониторинга токсичного контента в AI-продуктах.

## Содержание

- [Описание](#описание)
- [Функциональные требования](#функциональные-требования)
- [Установка и настройка](#установка-и-настройка)
  - [Предварительные требования](#предварительные-требования)
  - [Установка проекта](#установка-проекта)
- [Использование](#использование)

## Описание

qwerty123 решение для мониторинга токсичного контента в AI-продуктах предназначено для обеспечения безопасного и этичного взаимодействия с искусственным интеллектом. С помощью передовых технологий обработки естественного языка и машинного обучения мы помогаем вам выявлять и фильтровать вредоносные, оскорбительные или неприемлемые комментарии и сообщения в реальном времени.

- **Анализ в реальном времени**: Непрерывный мониторинг контента с немедленным выявлением токсичных элементов.
- **Многоуровневая фильтрация**: Использование различных моделей машинного обучения для точного определения и классификации токсичного контента.
- **Интеграция API**: Легкая интеграция с существующими системами и платформами через гибкий API.

## Функциональные требования

- **Регистрация пользователей:** Пользователи могут создавать учетные записи, входить в систему.
- **Чатиться с LLM через форму диалога:** Возможность проверки сообщения на токсичность с помощью чата.
- **Отображение истории сообщений на графиках по токсчичности:** Поддержка отображения единиц сообщений как токсичных так и нет
- **Интеграция с внешними сервисами:** Поддержка интеграции с такими сервисами, как yandexgpt.
- **Возможность работы с сервисом через API:** Поддержка взаимодействия с сервисом через API
- **Возможность выбора механизма фильтрации** Поддержка выбора как на входе так и на выходе работы с LLM

## Установка и настройка

### Предварительный требования

Удостовертесь, что с выполнены следующие условия:

1. **Docker и Docker Compose**
   - Установите последнюю стабильную версию Docker и Docker Compose. Рекомендуется использовать версии выше 20.10 для Docker и 1.29 для Docker Compose.

2. **Доступ к Docker Registry**
   - Убедитесь, что у вас есть доступ к Docker Registry для получения базовых образов. В случае необходимости вы можете заменить стандартные образы или использовать собственные, изменив конфигурацию Docker Compose.

3. **Доступ к репозиториям и зеркалам для `pip`**
   - Проверьте, что у вас есть доступ к репозиториям и зеркалам для библиотек пакетного менеджера `pip`. Это может быть как стандартные репозитории PyPI, так и частные или зеркальные источники.

4. **Виртуальная машина или сервер**
   - Для развертывания и запуска проекта вам потребуется виртуальная машина или сервер. На данный момент Kubernetes не используется, поэтому все компоненты будут развертываться непосредственно на сервере или VM.

### Установка проекта

Для установки проекта выполните следующие шаги:

1. **Клонирование репозитория**

   Сначала клонируйте репозиторий на свою локальную машину:
   ```bash
   git clone <например по гит протоколуgit@github.com:Kursor-nn/qwerty123.git>
   cd <напримерqwerty123>
   ```

2. **Загрузка и установка моделей**
    Поскольку модели являются крупными файлами и их нецелесообразно хранить в git-репозитории, вам необходимо загрузить их отдельно. Для этого:
    - модель раз
    - модель два

### Заполнение `.env` файлов

- Например заполните `src/guard/common/.env` и убедитесь, что ключ для взаимодействия с yandexgpt доступен как переменная `YANDEX_GPT_PRIVATE_KEY` в контейнере `llm-yandex-gpt-api-adapter`, пример можно увидеть, в `src/docker-compose.yml`

## Использование

Для запуска сервиса после вышеперечисленного достаточно следующих действий:

1. Выполнить запуск контейнеров с помощью:
    ```
    cd qwerty123/src
    docker compose up -d
    ```
Если образов контейнеров не будет, оно будут скачены и собраны.

2. После этого также необходимо инициализоровать базу данных, например с помощью src/guard/app/core/models/model.py или использовать liquibase, пример есть в .gitlab-ci.yml

3. При доступности ВМ или сервера с тестируемого устройства, можно пройти по адресу http://<ip> например, если не настроено доменное имя, и уведить WebUI.

    Кроме WebUI так же доступно взаимодействие по API, Swagger доступен по http://<ip/dns-name>/swagger/

*Пример использования*:
1. Авторизация, в результате которой получается Bearer токен
    ```
    curl --location 'http://<ip/dns-name>/api/user/signin' \
    --header 'Content-Type: application/json' \
    --data '{
    "login": "test",
    "password": "test"
    }'
    ```
2. Взаимодействие с API с использованием Bearer токен
    ```
    curl --location 'http://<api/dns-name>/api/guard/validate' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <token>' \
    --data '{
    "text": "какой-то запрос",
    "filter_type": "general_filter"
    }'
    ```