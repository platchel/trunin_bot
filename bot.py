import logging
import threading
from time import sleep
from tkinter import W
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime, pytz 
import apscheduler
import info
from info import Workers
import schedule_info


class BOT:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    logger = logging.getLogger(__name__)
    
    def __init__(self) -> None:
        self.updater = Updater("1482977152:AAG3EK9SCoCJGFB53WiKyIBMW5lAIbhqbUs")


        dispatcher = self.updater.dispatcher
    
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("job", self.job_info))
        dispatcher.add_handler(CommandHandler("end", self.end))
        thread = threading.Thread(target=self.schedule_checker)
        thread.start()
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, context):
        
        chat_id = update.message.chat_id
        
        match = False
        for key in schedule_info.worker_id:
            if str(chat_id) == schedule_info.worker_id[key]:
                update.message.reply_text(f"Привет, {update.message.from_user.first_name} \nУведомления включены")
                match = True

        if match == False:
            update.message.reply_text(f"Прости, а мы знакомы, {update.message.from_user.first_name}?")
        
        user = Workers(str(chat_id))        
        
        schedule = user.schedule()
        for lesson in user.schedule():
            s_day = schedule[lesson]['day']
            s_hour = schedule[lesson]['hour']
            s_minute = schedule[lesson]['minute']
            context.job_queue.run_daily(self.alarm, datetime.time(hour=s_hour, minute=s_minute,tzinfo=pytz.timezone('Europe/Moscow')), days=s_day, context=chat_id)
        




    def alarm(self, context: CallbackContext) -> None:
        """Send the alarm message."""
        job = context.job
        context.bot.send_message(job.context, text='У тебя урок через 5 минут')
        

    def info(self, context: CallbackContext):
        job = context.job
        context.bot.send_message(job.context, text='Кто был на уроке?')
    
    def job_info(self, update, context):
        job_names = [job.name for job in context.job_queue.jobs()]
        
    def end(self, update,context):
        current_jobs = context.job_queue.get_jobs_by_name('alarm')

        for job in current_jobs:
            job.schedule_removal()
        update.message.reply_text("Уведомления выключены")
    
    def schedule_checker(self):
        while(True):
            if (open('data.txt').read() != open('schedule_info.txt').read()):
                with open('schedule_info.txt', 'w') as file:
                    file.write(open('data.txt').read())
                sleep(1)
                print('123')
            else:    
                sleep(1)
                print('321')
    

bot = BOT()
bot.start()
