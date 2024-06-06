import requests
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Trace.moe API endpoint
TRACE_MOE_API_URL = 'https://trace.moe/api/search'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me an image or video and I will try to identify the anime scene!')

def analyze_media(update: Update, context: CallbackContext) -> None:
    file_id = update.message.photo[-1].file_id
    file_path = context.bot.get_file(file_id).file_path
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    
    response = requests.post(TRACE_MOE_API_URL, files={'image': requests.get(file_url).content})
    
    if response.status_code == 200:
        data = json.loads(response.text)
        anime_title = data['docs'][0]['title_native']
        episode_number = data['docs'][0]['episode']
        similarity = data['docs'][0]['similarity']
        
        update.message.reply_text(f'Anime Title: {anime_title}\nEpisode: {episode_number}\nSimilarity: {similarity}')
    else:
        update.message.reply_text('Failed to analyze the media. Please try again.')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, analyze_media))
    
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
