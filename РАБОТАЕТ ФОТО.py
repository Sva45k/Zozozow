import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from googleapiclient.discovery import build

# Токен вашего бота
vk_token = 'vk1.a.2y1XF8D4Vok64y3b_qjg_nCr-SJNlFIlXoHrN0ByNtnkn1bRjfk887Ex4j7yQ5hPgHh7ofSzvsqcACrPIKLiLnf6N_IR56w-SV9PTGv1WO_EmLBNNjCpi7fDq4JPwU3yuO-wqxvbqevHdoheaR2liAI9auupTUtUDvDba_MfgaOgDwKwe42Y03Lae_7YYjVXXZoVSKEMF63OsOY7QLbXDw'

# API-ключ для Google Custom Search JSON API
google_api_key = 'AIzaSyAIaW8hREaCfrfnAixCxt7JByajqt9okhk'
google_cse_id = 'f3e36dc0a7e8e4d5a'  # Замените на ваш CSE ID

# ID группы, в которой находится бот
group_id = '221556829'

vk_session = vk_api.VkApi(token=vk_token)
longpoll = VkBotLongPoll(vk_session, group_id)

def send_photo(peer_id, photo_url):
    vk_session.method('messages.send', {
        'peer_id': peer_id,
        'attachment': photo_url,
        'random_id': random.randint(1, 999999999)
    })

def get_random_image(query):
    if not query:
        return None  # Возвращаем None, если запрос пуст
    service = build("customsearch", "v1", developerKey=google_api_key)
    res = service.cse().list(q=query, cx=google_cse_id, searchType="image").execute()
    if 'items' in res:
        items = res['items']
        if items:  # Проверяем, что список не пуст
            random_item = random.choice(items)
            return random_item['link']
    return None

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.message['text'].lower().startswith('покажи фото'):
            query = event.obj.message['text'][12:]  # Исправлен срез строки
            random_image_url = get_random_image(query)
            if random_image_url:
                send_photo(event.obj.message['peer_id'], random_image_url)
                print(f"Отправлено фото для запроса: {query}")
            else:
                vk_session.method('messages.send', {
                    'peer_id': event.obj.message['peer_id'],
                    'message': 'Извините, не удалось найти фото по вашему запросу.',
                    'random_id': random.randint(1, 999999999)
                })
                print(f"Не удалось найти фото для запроса: {query}")
