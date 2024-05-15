from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
#from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials='YzAxMDg4YWItNzQ3My00ZDdjLTg0MDUtYTdkMzVhMmNiYTc3OmIyMDliYzI2LWI4NTItNDU2Mi05NmU4LTBjNTI2NGFhMDhkNA==', verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]

while(True):
    # Ввод пользователя
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print("Bot: ", res.content)