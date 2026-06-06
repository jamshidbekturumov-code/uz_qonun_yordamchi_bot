 
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
 
logging.basicConfig(level=logging.INFO)
 
TOKEN = os.environ.get("BOT_TOKEN")
 
QONUNLAR = [
    {
        "kalitlar": ["o'g'irlab", "o'g'irladi", "o'g'irishdi", "o'g'irlab ketdi", "telefon o'g'irlandi", "sumka oldi", "cho'ntakni", "cho'ntakdan", "talonchilik", "talon", "tortib oldi", "tortib ketdi", "yulqib", "yulqib oldi"],
        "qonun": "O'zR Jinoyat kodeksi 169-moddasi (O'g'irlik) va 164-moddasi (Talonchilik)",
        "jazo": "• Oddiy o'g'irlik: 3 yilgacha\n• Guruh bo'lib: 5 yilgacha\n• Qurol bilan yoki zo'rlik ishlatib (talonchilik): 8-12 yil",
        "yechim": "1. Darhol 102 (politsiya) ga qo'ng'iroq qiling\n2. Voqea joyidan ketmang\n3. Guvohlarni toping\n4. Kamera yozuvlari bo'lsa so'rang\n5. Ariza yozing — politsiya 3 kun ichida javob berishi shart"
    },
    {
        "kalitlar": ["urdi", "urishdi", "kaltakladi", "kaltaklashdi", "musht", "mushtladi", "zarb berdi", "jarohat", "qon", "og'ritdi", "zo'ravonlik"],
        "qonun": "O'zR Jinoyat kodeksi 104-moddasi (Qasddan tan jarohati) va 110-moddasi (Kaltaklash)",
        "jazo": "• Engil tan jarohati: 2 yilgacha\n• O'rtacha tan jarohati: 5 yilgacha\n• Og'ir tan jarohati: 8 yilgacha\n• Ommaviy kaltaklash: 10 yilgacha",
        "yechim": "1. Darhol 103 (tez yordam) ga qo'ng'iroq qiling\n2. Tibbiy ko'rik oling — hujjat sifatida kerak\n3. 102 ga ariza bering\n4. Guvohlar bo'lsa ismlarini oling\n5. Suratga oling"
    },
    {
        "kalitlar": ["tahdid", "qo'rqitdi", "o'ldiraman", "o'ldiradi", "qo'rqitmoqda", "xavf", "qo'rquvda", "terrorga"],
        "qonun": "O'zR Jinoyat kodeksi 112-moddasi (Tahdid qilish)",
        "jazo": "• Oddiy tahdid: 3 yilgacha\n• Qurol ko'rsatib tahdid: 5 yilgacha\n• Tizimli tahdid: 7 yilgacha",
        "yechim": "1. Tahdid xabarlarini saqlang (screenshot)\n2. Guvohlar bo'lsa yozing\n3. 102 ga ariza bering\n4. Prokuraturaga murojaat qiling"
    },
    {
        "kalitlar": ["aldadi", "firib", "firibgar", "pul oldi", "qaytarmadi", "aldab", "moliyaviy", "soxta", "yolg'on"],
        "qonun": "O'zR Jinoyat kodeksi 168-moddasi (Firibgarlik)",
        "jazo": "• 10 MMBHM gacha zarar: 3 yilgacha\n• Katta miqdor: 5 yilgacha\n• O'ta katta miqdor yoki guruh: 10 yilgacha",
        "yechim": "1. Pul o'tkazmalari, xabarlarni saqlang\n2. Bank orqali o'tgan bo'lsa — bank ko'chirmasini oling\n3. 102 ga ariza bering\n4. Fuqarolik sudiga da'vo ariza bering"
    },
    {
        "kalitlar": ["ishdan", "bo'shatishdi", "ishdan haydi", "ishdan chiqardi", "ish haqi bermaydi", "maosh bermaydi", "oylik bermasdi", "mehnat"],
        "qonun": "O'zR Mehnat kodeksi 100-moddasi (Mehnat shartnomasi) va 106-moddasi",
        "jazo": "• Asossiz bo'shatish: ish beruvchi jarima to'laydi\n• Ish haqi to'lamaslik: ma'muriy va jinoiy javobgarlik\n• Jinoiy: 2 yilgacha",
        "yechim": "1. Mehnat inspeksiyasiga murojaat qiling\n2. Sudga da'vo ariza bering\n3. Prokuraturaga shikoyat yozing\n4. Ish haqini 3 yil ichida talab qilish mumkin"
    },
    {
        "kalitlar": ["aliment", "nafaqa", "bola uchun", "er to'lamaydi", "ajrashish", "nikoh", "oila"],
        "qonun": "O'zR Oila kodeksi 99-moddasi (Aliment) va 160-moddasi",
        "jazo": "• Aliment to'lamaslik: 2 yilgacha qamoq\n• Tizimli to'lamaslik: 3 yilgacha",
        "yechim": "1. Sudga aliment undirishga ariza bering\n2. Sud ijrochisiga murojaat qiling\n3. Ijro varaqasi oling\n4. Bank hisobidan ushlab qolish mumkin"
    },
    {
        "kalitlar": ["qarz", "pul bermaydi", "qaytarmayapti", "qarzini", "shartnoma", "ijara", "uy bermasdi"],
        "qonun": "O'zR Fuqarolik kodeksi 732-moddasi (Qarz shartnomasi)",
        "jazo": "• Qarz qaytarmaslik — fuqarolik da'vosi\n• Firibgarlik bo'lsa — jinoyat: 5 yilgacha",
        "yechim": "1. Yozma talab xati yuboring\n2. 15 kun ichida javob yo'q bo'lsa — sudga bering\n3. Sud orqali mol-mulkini musodara qilish mumkin\n4. Ijro varaqasi oling"
    },
    {
        "kalitlar": ["avariya", "mashina urdi", "yo'l halokati", "haydovchi qochdi", "transport", "yo'l"],
        "qonun": "O'zR Ma'muriy javobgarlik kodeksi 135-moddasi va Jinoyat kodeksi 266-moddasi",
        "jazo": "• Oddiy avariya: jarima + huquqdan mahrum\n• Jarohat yetkazsa: 5 yilgacha\n• O'lim bo'lsa: 10 yilgacha\n• Qochib ketsa: +2 yil qo'shiladi",
        "yechim": "1. 102 va 103 ga qo'ng'iroq qiling\n2. Joyni o'zgartirmang\n3. Suratga oling\n4. Guvohlar ismini oling\n5. YHXX (GAI) ni chaqiring"
    },
    {
        "kalitlar": ["giyohvand", "narkotik", "drug", "nasha", "ganja", "mast", "ichkilik"],
        "qonun": "O'zR Jinoyat kodeksi 276-moddasi (Giyohvand moddalar)",
        "jazo": "• Saqlash: 5 yilgacha\n• Tarqatish: 10-15 yil\n• Tashkilashtirish: 15-20 yil yoki umrbod",
        "yechim": "1. Darhol 102 ga xabar bering\n2. O'zingiz teginmang\n3. Guvoh bo'lsangiz — ariza yozing"
    },
]
 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}! ⚖️\n\n"
        "Men <b>O'zbekiston Yuridik Yordamchi</b> botman.\n\n"
        "Boshingizga tushgan <b>holatni oddiy so'zlar bilan yozing</b> — men sizga:\n"
        "✅ Qaysi qonun va modda asosida\n"
        "✅ Necha yil jazo berilishini\n"
        "✅ Qanday yechim topishni aytaman\n\n"
        "Masalan:\n"
        "• «Kuchada telefonim o'g'irlandi»\n"
        "• «Qo'shnım meni kaltakladi»\n"
        "• «Ishdan asossiz bo'shatishdi»\n\n"
        "⚠️ Bu umumiy ma'lumot, rasmiy yuridik maslahat o'rnini bosmaydi.",
        parse_mode="HTML"
    )
 
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Holatni oddiy so'zlar bilan yozing.\n\n"
        "Misol: «Meni aldab pul olishdi» yoki «Telefonim o'g'irlandi»\n\n"
        "/start - boshlash"
    )
 
async def holat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.lower()
    topildi = False
 
    for qonun in QONUNLAR:
        for kalit in qonun["kalitlar"]:
            if kalit in matn:
                javob = (
                    f"⚖️ <b>Qonun:</b> {qonun['qonun']}\n\n"
                    f"🔒 <b>Jazo:</b>\n{qonun['jazo']}\n\n"
                    f"✅ <b>Siz nima qilishingiz kerak:</b>\n{qonun['yechim']}\n\n"
                    f"📞 <b>Muhim raqamlar:</b>\n"
                    f"• Politsiya: 102\n"
                    f"• Tez yordam: 103\n"
                    f"• Prokuratura: 191"
                )
                await update.message.reply_text(javob, parse_mode="HTML")
                topildi = True
                break
        if topildi:
            break
 
    if not topildi:
        await update.message.reply_text(
            "Kechirasiz, holatni aniqroq tushunolmadim. 🤔\n\n"
            "Iltimos, quyidagilardan biriga oid yozing:\n"
            "• O'g'irlik / talonchilik\n"
            "• Kaltaklash / zo'ravonlik\n"
            "• Tahdid qilish\n"
            "• Firibgarlik / aldash\n"
            "• Mehnat / ish haqi\n"
            "• Aliment / oila\n"
            "• Qarz / shartnoma\n"
            "• Avariya / yo'l\n"
            "• Giyohvand modda\n\n"
            "📞 Shoshilinch holatlarda: 102 (politsiya)"
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
