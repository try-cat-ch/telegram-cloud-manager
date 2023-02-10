DEV launch: main.py -d=True

backend (local) -> BOT_TOKEN -> Bot (dev)

backend (serverless) -> BOT_TOKEN -> API Gateway YC -> Bot (prod)


https://cloud.yandex.ru/docs/functions/tutorials/telegram-bot-serverless
1. create bot in Botfather
2. create api gateway
3. create cloud function (use BOT_TOKEN and API_GATEWAY_DOMAIN)
4. set id_cloud_function in api gateway
5. curl api.telegram.org --data "API_GATEWAY_DOMAIN/id_cloud_function"

TODO:
1. buttons
2. profiles
