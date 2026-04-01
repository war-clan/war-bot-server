import telebot
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- كود "الخدعة" حتى Hugging Face يفتح البوت للأبد ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"WAR BOT IS RUNNING 24/7!")

def run_dummy_server():
    server_address = ('0.0.0.0', 7860)
    httpd = HTTPServer(server_address, DummyHandler)
    httpd.serve_forever()

# تشغيل السيرفر الوهمي بخلفية البوت
threading.Thread(target=run_dummy_server, daemon=True).start()
# --------------------------------------------------

# التوكن مالتك (لا تغيره)
TOKEN = '8505607439:AAEw3-Ci_4yWATze9pfRnzr75ASq4bFpRoE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 **تم التشغيل بنجاح يا قائد وارة!** 🔥\nأنا شغال هسة 24 ساعة سحابياً.")

@bot.message_handler(commands=['links'])
def send_links(message):
    bot.reply_to(message, "📺 YT & TikTok: **WAR || ETH**")

@bot.message_handler(commands=['barca'])
def barca(message):
    bot.reply_to(message, "🔵🔴 **Visca el Barça!**")

print("البوت انطلق يا وحش...")
bot.infinity_polling()
