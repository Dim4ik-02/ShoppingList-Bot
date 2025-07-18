# ShoppingList-Bot
Telegram Bot which can help you with your products

# 🛒 Telegram Shopping List Bot

Простой Telegram-бот для создания и управления персональным списком покупок.

## 🔧 Возможности

- 📥 Добавление товаров в список
- 📋 Просмотр текущего списка с отметками "куплено / не куплено"
- ✅ Отметка товаров как купленных
- ❌ Удаление одного товара или всей корзины
- 📤 Экспорт списка в JSON-файл
- 📲 Удобное управление с помощью команд или кнопок

---

## 🚀 Как запустить бота

### 1. Склонируй или скачай проект
```bash
git clone https://github.com/Dim4ik-02/shoppingList-Bot.git
cd shoppingList-Bot

2. Установи зависимости
bash
pip install -r requirements.txt

3. Вставь свой API-токен
Создай файл api_token.py и добавь туда:
API_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"

4. Запусти бота
bash
python shopping_list_bot.py


💬 Команды бота
Команда	Описание
/start	Запуск бота и показ кнопок
/add_item	Добавить товар в список
/show_list	Показать список покупок
/mark_as_bought	Отметить товар как купленный
/delete_item	Удалить товар из списка
/clear_list	Очистить список полностью
/export_json	Отправить весь список в формате JSON
