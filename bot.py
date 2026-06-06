import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

# Token Render'dan maxfiy o'zgaruvchi sifatida olinadi (kodda ochiq emas)
TOKEN = os.environ.get("BOT_TOKEN")

QONUNLAR = [
    {
        "kalitlar": ["ish", "ishdan", "ish haqi", "mehnat", "ta'til", "oylik", "ishga"],
        "javob": (
            "⚖️ <b>Mehnat munosabatlari</b>\n\n"
            "O'zR Mehnat kodeksi:\n"
            "• Ish haqi o'z vaqtida to'lanishi shart.\n"
            "• Ishdan asossiz bo'shatish taqiqlanadi.\n"
            "• Yillik mehnat ta'tili kamida 15 ish kuni.\n\n"
            "📌 Maslahat: huquqlaringiz buzilsa, mehnat inspeksiyasiga murojaat qiling."
        ),
    },
    {
        "kalitlar": ["ajrashish", "nikoh", "er", "xotin", "aliment", "bola", "oila", "nafaqa"],
        "javob": (
            "⚖️ <b>Oilaviy munosabatlar</b>\n\n"
            "O'zR Oila kodeksi:\n"
            "• Nikohni bekor qilish sud yoki FHDYo orqali.\n"
            "• Bolaga aliment: 1 bolaga daromadning 1/4 qismi.\n"
            "• Ota-ona bolani boqishga majbur.\n\n"
            "📌 Maslahat: aliment masalasida sudga ariza bering."
        ),
    },
    {
        "kalitlar": ["ijara", "uy", "kvartira", "shartnoma", "qarz", "pul", "bermayapti"],
        "javob": (
            "⚖️ <b>Fuqarolik munosabatlari (shartnoma, qarz)</b>\n\n"
            "O'zR Fuqarolik kodeksi:\n"
            "• Qarz shartnomasi yozma bo'lishi kerak.\n"
            "• Qarzni qaytarmaslik — sudga murojaat asosi.\n"
            "• Ijara shartnomasi yozma tuzilishi lozim.\n\n"
            "📌 Maslahat: shartnoma va to'lov hujjatlarini saqlang."
        ),
    },
    {
        "kalitlar": ["o'g'irlik", "firib", "jinoyat", "kaltak", "tahdid", "aldash", "urdi"],
        "javob": (
            "⚖️ <b>Jinoiy javobgarlik</b>\n\n"
            "O'zR Jinoyat kodeksi:\n"
            "• O'g'irlik — jarima yoki ozodlikdan mahrum qilish.\n"
            "• Firibgarlik — jazo ko'lamiga qarab belgilanadi.\n"
            "• Tan jarohati yetkazish jazolanadi.\n\n"
            "📌 Maslahat: darhol politsiyaga (102) yoki prokuraturaga murojaat qiling."
        ),
    },
    {
        "kalitlar": ["yo'l", "mashina", "avto", "haydovchi", "jarima", "tezlik", "avariya"],
        "javob": (
            "⚖️ <b>Yo'l harakati</b>\n\n"
            "O'zR Ma'muriy javobgarlik kodeksi:\n"
            "• Tezlikni oshirish uchun jarima belgilanadi.\n"
            "• Mast holda haydash — huquqdan mahrum qilish.\n"
            "• Avariya holatida YHXXga xabar bering.\n\n"
            "📌 Maslahat: avariyada joyni o'zgartirmang, suratga oling."
        ),
    },
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}! ⚖️\n\n"
        "Men yuridik yordamchi botman.\n"
        "Boshingizga tushgan <b>holatni yozib yuboring</b>, "
        "men O'zbekiston qonunlaridan mos qoidani topib beraman.\n\n"
        "Masalan:\n"
        "• «Meni ishdan asossiz bo'shatishdi»\n"
        "• «Erim aliment to'lamayapti»\n"
        "• «Qarz berdim, qaytarmayapti»\n\n"
        "⚠️ Diqqat: bu umumiy ma'lumot, rasmiy yuridik maslahat o'rnini bosmaydi.",
        parse_mode="HTML"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Holatingizni oddiy so'zlar bilan yozing, men mos qonunni topaman.\n"
        "/start - boshlash"
    )

async def holat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.lower()
    topildi = False
    for qonun in QONUNLAR:
        for kalit in qonun["kalitlar"]:
            if kalit in matn:
                await update.message.reply_text(qonun["javob"], parse_mode="HTML")
                topildi = True
                break
        if topildi:
            break
    if not topildi:
        await update.message.reply_text(
            "Kechirasiz, bu holat bo'yicha aniq qonun topa olmadim. 🤔\n\n"
            "Iltimos, holatni boshqacharoq yozib ko'ring. Masalan, mavzu:\n"
            "• ish / mehnat\n• oila / aliment\n• qarz / shartnoma\n"
            "• jinoyat / o'g'irlik\n• yo'l harakati / jarima\n\n"
            "Murakkab holatlarda professional yuristga murojaat qiling."
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, holat_handler))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
