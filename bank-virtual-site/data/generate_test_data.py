import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

clients = []
statuses = ['Студент', 'Зарплатный клиент', 'Премиальный клиент', 'Стандартный клиент']
cities = ['Алматы', 'Астана', 'Шымкент', 'Караганда', 'Актау']
names = ['Айгерим', 'Данияр', 'Сабина', 'Тимур', 'Камилла', 'Аян', 'Руслан', 'Мадина', 'Арман', 'Карина',
         'Бауржан', 'Жанар', 'Алина', 'Диас', 'Нурия', 'Ерасыл', 'Жанель', 'Санжар', 'Азамат', 'Анель',
         'Павел', 'Аружан', 'Темирлан', 'Гульмира', 'Адиль', 'Маржан', 'Нурсултан', 'Алтынай', 'Сая', 'Ербол',
         'Дамир', 'Алия', 'Мерей', 'Инкар', 'Самат', 'Назым', 'Гульнар', 'Серик', 'Ляззат', 'Асхат',
         'Сандугаш', 'Рустем', 'Нуртас', 'Айнагуль', 'Диана', 'Арсен', 'Камшат', 'Ержан', 'Амина', 'Тимурлан',
         'Жанат', 'Милана', 'Расул', 'Виктория', 'Асель', 'Нуркен', 'Жания', 'Султан', 'Динара', 'Ермек']

for i in range(1, 61):
    client = {
        'client_code': i,
        'name': names[i-1],
        'status': random.choice(statuses),
        'age': random.randint(18, 65),
        'city': random.choice(cities),
        'avg_monthly_balance_KZT': random.uniform(100000, 10000000),
        'push_opt_in': random.choice([True, False])
    }
    clients.append(client)

pd.DataFrame(clients).to_csv("clients.csv", index=False)

categories = [
    'Одежда и обувь', 'Продукты питания', 'Кафе и рестораны', 'Медицина', 'Авто', 'Спорт', 
    'Развлечения', 'АЗС', 'Кино', 'Питомцы', 'Книги', 'Цветы', 'Едим дома', 'Смотрим дома', 
    'Играем дома', 'Косметика и Парфюмерия', 'Подарки', 'Ремонт дома', 'Мебель', 'Спа и массаж', 
    'Ювелирные украшения', 'Такси', 'Отели', 'Путешествия'
]
transfer_types = [
    'salary_in', 'stipend_in', 'family_in', 'cashback_in', 'refund_in', 'card_in', 'p2p_out', 
    'card_out', 'atm_withdrawal', 'utilities_out', 'loan_payment_out', 'cc_repayment_out', 
    'installment_payment_out', 'fx_buy', 'fx_sell', 'invest_out', 'invest_in', 'deposit_topup_out', 
    'deposit_fx_topup_out', 'deposit_fx_withdraw_in', 'gold_buy_out', 'gold_sell_in'
]
currencies = ['KZT', 'USD', 'RUB', 'EUR']

start_date = datetime(2025, 6, 1)
end_date = datetime(2025, 8, 31)

for client_code in range(1, 61):
    transactions = []
    num_tx = random.randint(30, 100)
    for _ in range(num_tx):
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        tx = {
            'client_code': client_code,
            'date': date,
            'category': random.choice(categories),
            'amount': random.uniform(1000, 100000),
            'currency': random.choice(currencies)
        }
        transactions.append(tx)
    pd.DataFrame(transactions).to_csv(f'client_{client_code}_transactions_3m.csv', index=False)
    
    transfers = []
    num_tf = random.randint(10, 50)
    for _ in range(num_tf):
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        tf_type = random.choice(transfer_types)
        direction = 'in' if tf_type in ['salary_in', 'stipend_in', 'family_in', 'cashback_in', 'refund_in', 'card_in', 'invest_in', 'deposit_fx_withdraw_in', 'gold_sell_in'] else 'out' if tf_type in ['p2p_out', 'card_out', 'atm_withdrawal', 'utilities_out', 'loan_payment_out', 'cc_repayment_out', 'installment_payment_out', 'invest_out', 'deposit_topup_out', 'deposit_fx_topup_out', 'gold_buy_out'] else random.choice(['in', 'out'])
        tf = {
            'client_code': client_code,
            'date': date,
            'type': tf_type,
            'direction': direction,
            'amount': random.uniform(5000, 500000),
            'currency': random.choice(currencies)
        }
        transfers.append(tf)
    pd.DataFrame(transfers).to_csv(f'client_{client_code}_transfers_3m.csv', index=False)