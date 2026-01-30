import discord
from discord.ext import commands
import re

# Настройка
TOKEN = "ВАШ ТОКЕН" #Read readme_blyat

bot = commands.Bot(command_prefix="", self_bot=True, help_command=None)

def replace_logic(text):
   
    rules = {
        'з': 'Z', 'З': 'Z',
        'в': 'V', 'В': 'V',
        'о': 'O', 'О': 'O',
        'с': 'Z', 'С': 'Z'  
    }
    
    url_pattern = r'(https?://[^\s]+)'
    parts = re.split(url_pattern, text)
    
    for i in range(len(parts)):
        if not re.match(url_pattern, parts[i]):
            for cyr, lat in rules.items():
                parts[i] = parts[i].replace(cyr, lat)
                
    return "".join(parts)
@bot.event
async def on_ready():
    print(f'Бот запущен под аккаунтом: {bot.user}')

is_active = True

@bot.event
async def on_message(message):
    global is_active
    
    # Бот реагирует только на твои сообщения
    if message.author != bot.user:
        return

    # Команда для включения/выключения
    if message.content.lower() == "!t":  # Пишешь !t чтобы переключить
        is_active = not is_active
        status = "ВКЛЮЧЕН" if is_active else "ВЫКЛЮЧЕН"
        print(f"Режим замены: {status}")
        
        # Редактируем сообщение, чтобы ты видел подтверждение, и через 2 сек удаляем его
        await message.edit(content=f"⚙️ Режим замены {status}")
        await message.delete(delay=2)
        return

    # Если режим выключен, ничего не делаем
    if not is_active:
        return

    # Логика замены
    original_content = message.content
    new_content = replace_logic(original_content)

    if new_content != original_content:
        await message.edit(content=new_content)

bot.run(TOKEN)