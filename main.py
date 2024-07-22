import logging
from telegram import  ReplyKeyboardRemove, Update,Document
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler, ConversationHandler, MessageHandler,filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger =logging.Logger("telegram")

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if(update.effective_chat):
        await context.bot.send_message(chat_id=update.effective_chat.id,text="hello_world")

async def upload_PHOTO(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if(update.message):
        message = update.message.effective_attachment
        photo_file = await message.get_file()#type: ignore
        photo_bytes = await photo_file.download_as_bytearray()
        send_file(photo_bytes,message.mime_type,message.file_name)#type: ignore
    return ConversationHandler.END
        
async def upload_VIDEO(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if(update.message and isinstance(update.message.effective_attachment,Document)):
        message = update.message.effective_attachment
        if(message.mime_type):
            photo_file = await message.get_file()
            photo_bytes = await photo_file.download_as_bytearray()
            send_file(photo_bytes,message.mime_type,message.file_name)

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    if(update.message):
        user = update.message.from_user
        if(user):
            logger.info("User %s did not send a photo.", user.first_name)
            await update.message.reply_text(
                "I bet you look great! Now, send me your location please, or send /skip."
            )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    if(update.message):
        user = update.message.from_user
        if(user):
            logger.info("User %s canceled the conversation.", user.first_name )
            await update.message.reply_text(
                "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
            )

    return ConversationHandler.END




if __name__ == "__main__":
    proxy_url = "http://0.0.0.0:20171"
    applicaiton = ApplicationBuilder().token("7443345806:AAGmTpYkQ9rtUXruY13p-h9PxG_svtS-5Fw").proxy(proxy_url).get_updates_proxy(proxy_url).build()
    start_handler= CommandHandler("start",start)
    applicaiton.add_handler(start_handler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            "PHOTO": [MessageHandler(filters.PHOTO, upload_PHOTO), CommandHandler("skip", skip_photo)],
            "VIDEO": [MessageHandler(filters.PHOTO, upload_VIDEO), CommandHandler("skip",skip_photo)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    applicaiton.run_polling()
