import telebot
import time

# التوكن الخاص بيك (المفتاح السري)
TOKEN = '8505607439:AAEw3-Ci_4yWATze9pfRnzr75ASq4bFpRoE'
bot = telebot.TeleBot(TOKEN)

# رسالة الترحيب /start
@bot.message_id_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🔥 **أهلاً بك في بوت WAR || ETH الرسمي!** 🔥\n\n"
        "أنا بوت مطور بواسطة القائد وارة (Wareth).\n"
        "عضو في قبيلة الأعرجي وفخر كلان WAR في Delta Force. 🦅\n\n"
        "استخدم الأامر التالية:\n"
        "🚀 /war - معلومات عن الكلان\n"
        "🔗 /links - روابط القنوات (YT & TikTok)\n"
        "🛡️ /hack - فحص أمني سريع (للمزح)\n"
        "⚽ /barca - رسالة لعشاق البرشا"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# أمر روابط القنوات
@bot.message_handler(commands=['links'])
def send_links(message):
    links = (
        "📱 **تابع أقوى لقطات القيمنق هنا:**\n\n"
        "📺 YouTube: [WAR || ETH](https://youtube.com/@war-eth)\n"
        "🎵 TikTok: [WAR || ETH](https://tiktok.com/@war-eth)\n\n"
        "دعمكم هو اللي يخلينا نستمر! 🦅🔥"
    )
    bot.send_message(message.chat.id, links, parse_mode='Markdown', disable_web_page_preview=False)

# أمر كلان WAR
@bot.message_handler(commands=['war'])
def war_info(message):
    bot.reply_to(message, "🦅 **WAR CLAN - Delta Force**\n\nنحن لا ننهزم، نحن ننتصر أو نتعلم. انضم إلينا في السيرفر وكن جزءاً من الأساطير!")

# أمر الهكر (للمزح بما إنك تحب الـ Ethical Hacking)
@bot.message_handler(commands=['hack'])
def simulate_hack(message):
    msg = bot.reply_to(message, "⚙️ جاري الاتصال بالسيرفر المشفر...")
    time.sleep(1)
    bot.edit_message_text("🛡️ جاري فحص الثغرات الأمنية...", message.chat.id, msg.message_id)
    time.sleep(1)
    bot.edit_message_text("✅ تم الفحص: نظامك محمي بواسطة بروتوكولات WAR || ETH!", message.chat.id, msg.message_id)

# أمر برشلونة
@bot.message_handler(commands=['barca'])
def barca_fans(message):
    bot.reply_to(message, "🔵🔴 **Visca el Barça!**\nفخر كاتالونيا وفخر وارة الأعرجي. ميسكي ان بلوس! ⚽")

# تشغيل البوت للأبد
print("البوت شغال هسة يا وحش...")
bot.infinity_polling()
