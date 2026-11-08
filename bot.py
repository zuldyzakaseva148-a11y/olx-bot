import asyncio
import sqlite3
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher

# ================= НАСТРОЙКИ =================
TOKEN = "9281348613:AAGIf_CvqbFmablkeXgkAcyHn5UFu-ClRG4"
CHAT_ID = 7525212274
OLX_URL = "https://www.olx.kz/d/elektronika/karaganda/?search[order]=created_at:desc"
# =============================================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройка базы данных
conn = sqlite3.connect('ads.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS seen_ads (id TEXT PRIMARY KEY)')
conn.commit()

def is_new(ad_id):
    cursor.execute('SELECT id FROM seen_ads WHERE id = ?', (ad_id,))
    return cursor.fetchone() is None

def save_ad(ad_id):
    cursor.execute('INSERT INTO seen_ads (id) VALUES (?)', (ad_id,))
    conn.commit()

async def check_olx():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(OLX_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    cards = soup.find_all('div', {'data-testid': 'ad-card'})

    for card in cards:
        link_elem = card.find('a')
        if not link_elem:
            continue

        link = "https://www.olx.kz" + link_elem['href'] if link_elem['href'].startswith('/') else link_elem['href']
        ad_id = link.split('#')[0]

        if is_new(ad_id):
            title = card.find('h6').text if card.find('h6') else "Новое объявление"
            price = card.find('p', {'data-testid': 'ad-price'}).text if card.find('p', {'data-testid': 'ad-price'}) else "Цена не указана"

            save_ad(ad_id)

            text = f"🔥 **НОВОЕ ОБЪЯВЛЕНИЕ!**\n\n📌 **{title}**\n💰 **Цена:** {price}\n\n🔗 [Открыть объявление]({link})"
            await bot.send_message(CHAT_ID, text, parse_mode="Markdown")

async def loop():
    print("Бот-радар запущен и ищет объявления...")
    while True:
        try:
            await check_olx()
        except Exception as e:
            print(f"Ошибка при проверке: {e}")
        await asyncio.sleep(40)

async def main():
    asyncio.create_task(loop())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
