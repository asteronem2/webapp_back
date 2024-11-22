import traceback

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from src.tg_bot.tg_bot import bot

router = APIRouter(prefix='', tags=['Заявки'])

class ApplicationModel(BaseModel):
    value: int
    bank: str
    number: str

eng_to_rus_bank = {
    'sber': 'Сбер',
    'tbank': 'Тбанк (Тинькофф)',
    'alfa': 'Альфа',
    'vtb': 'ВТБ',
    'open': 'Открытие'
}

@router.post('/create_application/')
async def main_page(application: ApplicationModel):
    async with httpx.AsyncClient() as client:
        try:
            res1 = await client.get('https://api.coincap.io/v2/assets/?ids=tether')
            tether_rate = float(res1.json()['data'][0]['priceUsd'])
            res2 = await client.get('https://www.cbr-xml-daily.ru/daily_json.js')
            rubles_rate = float(res2.json()['Valute']['USD']['Value'])
        except:
            traceback.print_exc()
            tether_rate = 0
            rubles_rate = 0


    await bot.send_message(
        chat_id=892097042,
        text=f'Создана заявка:\n'
             f'Сумма в USDT: {application.value}\n'
             f'Сумма в долларах: {application.value * tether_rate}\n'
             f'Сумма в рублях: {application.value * rubles_rate}\n'
             f'Банк: {eng_to_rus_bank[application.bank]}\n'
             f'Номер (карта или телефон): {application.number}\n'

    )