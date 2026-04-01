import telebot
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# ========== نظام الحماية من الإغلاق (Hugging Face Stay-Alive) ==========
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"WAR-BOT SERVER IS ACTIVE 24/7")

def run_dummy_server():
    server_address = ('0.0.0.0', 7860)
    httpd = HTTPServer(server_address, DummyHandler)
    print("✅ Dummy Server started on port 7860 for Hugging Face Health Check")
    httpd.serve_forever()

# تشغيل السيرفر في خلفية البوت
threading.Thread(target=run_dummy_server, daemon=True).start()
# =====================================================================

# التوكن مالتك الحقيقي
TOKEN = '8505607439:AAEw3-Ci_4yWATze9pfRnzr75ASq4bFpRoE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_msg = (
        "🦅 **أهلاً بك في نظام WAR || ETH السحابي!**\n\n"
        "البوت الآن يعمل بنجاح من سيرفرات Hugging Face.\n"
        "تم تطوير النظام بواسطة القائد وارة الأعرجي. 🔥\n\n"
        "**الأوامر المتاحة:**\n"
        "🚀 /war - أخبار الكلان\n"
        "📺 /links - القنوات الرسمية\n"
        "🛡️ /status - حالة السيرفر\n"
        "⚽ /barca - لعشاق البرشا"
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

@bot.message_handler(commands=['war'])
def war_clan(message):
    bot.send_message(message.chat.id, "🦅 **WAR CLAN - Delta Force**\n\nالقوة، السيطرة، والانتصار. نحن الأباطرة!")

@bot.message_handler(commands=['links'])
def social_links(message):
    links = (
        "📱 **WAR || ETH SOCIALS:**\n\n"
        "[YouTube](https://youtube.com/@war-eth)\n"
        "[TikTok](https://tiktok.com/@war-eth)"
    )
    bot.send_message(message.chat.id, links, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def check_status(message):
    status_msg = (
        "✅ **الحالة:** متصل (Online)\n"
        "🛰️ **السيرفر:** Hugging Face Cloud\n"
        "👤 **المطور:** وارة الأعرجي"
    )
    bot.send_message(message.chat.id, status_msg)

@bot.message_handler(commands=['barca'])
def barca(message):
    bot.send_message(message.chat.id, "🔵🔴 **Visca el Barça!** ⚽")

if __name__ == '__main__':
    print("🚀 WAR BOT IS DEPLOYING...")
    # استخدام polling مع إعادة محاولة تلقائية
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ حدث خطأ: {e}. إعادة الاتصال بعد 5 ثوان...")
            time.sleep(5)
