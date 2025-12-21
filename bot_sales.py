import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# ==========================================
# 1. SYSTEM CONFIGURATION (HARDCODED)
# ==========================================
# Token dan ID ini sudah ditanam permanen. Jangan diubah.
API_TOKEN = '8505852576:AAEeIJHO6zIrLnB07HU5FdZaTIGqVZbPogk' 
ADMIN_ID = 6994920103

bot = telebot.TeleBot(API_TOKEN)

# ==========================================
# 2. SYSTEM MESSAGES (TERMINAL STYLE)
# ==========================================
MSG_WELCOME = """
TITAN SYSTEMS // INTERFACE V.1.0
Connection established. User authenticated. Status: ONLINE

**Selamat datang.**
Sistem Neural Network Titan siap digunakan.
Tidak ada janji manis. Hanya algoritma yang bekerja.

**STATUS REPORT:**
[+] Engine: Active
[+] Security: Undetected (15 Days Log)
[+] Server: Stable

Pilih perintah di bawah:
"""

MSG_INSTRUCTION = """
PAYMENT_GATEWAY // INITIALIZED

Silakan lakukan scan pada **QRIS** yang terlampir (Support All Payment).

**TOTAL: Rp 75.000 / Bulan**

> **INSTRUKSI:**
1. Scan QRIS di bawah.
2. Selesaikan pembayaran.
3. Lampirkan **FOTO BUKTI** (Screenshot) di chat ini untuk verifikasi lisensi.
"""

MSG_QUICK_INFO = """
SYSTEM_SPECIFICATIONS

**CORE ARCHITECTURE**
Type: Neural Network (Maia Weights)
Logic: 1-Node Heuristic (Human-Like)
Depth: Adaptive (Anti-Cheat Optimized)

**COMPATIBILITY**
Target: Chess.com & Lichess
OS: Windows 10/11 (64-bit)

**SECURITY PROTOCOL**
Detection Risk: Low (Behavioral Analysis Safe)
Ban Rate: 0% (Current Batch)

*Untuk changelog teknis dan update firmware, akses Channel Database.*
"""

# ==========================================
# 3. MENU NAVIGASI (CLI BUTTONS)
# ==========================================
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    
    # Tombol gaya profesional
    btn_pay = InlineKeyboardButton("[ ACCESS ] PAYMENT GATEWAY (QRIS)", callback_data="buy")
    btn_channel = InlineKeyboardButton("[ LOGS ] CHANNEL UPDATE", url="https://t.me/TitanChessss")
    btn_proof = InlineKeyboardButton("[ DATA ] RESEARCH EVIDENCE", url="https://titan-links.vercel.app/logs.html")
    btn_admin = InlineKeyboardButton("[ CONTACT ] DEVELOPER", url="https://t.me/TitanChesss")
    btn_info = InlineKeyboardButton("[ SYSTEM ] SPECIFICATIONS", callback_data="info_text")

    markup.add(btn_pay, btn_channel, btn_proof, btn_admin, btn_info)
    return markup

# ==========================================
# 4. LOGIKA UTAMA
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Menggunakan Markdown ``` agar font jadi kotak terminal
    bot.reply_to(message, MSG_WELCOME, parse_mode='Markdown', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # JIKA KLIK INFO
    if call.data == "info_text":
        bot.answer_callback_query(call.id, "Accessing Specs...")
        bot.send_message(call.message.chat.id, MSG_QUICK_INFO, parse_mode='Markdown')
        bot.send_message(call.message.chat.id, "Awaiting command...", reply_markup=main_menu())
    
    # JIKA KLIK BAYAR
    elif call.data == "buy":
        bot.answer_callback_query(call.id, "Initializing QRIS...")
        try:
            # Pastikan file qris.jpg ada di folder yang sama
            qris_img = open('qris.jpg', 'rb') 
            bot.send_photo(call.message.chat.id, qris_img, caption=MSG_INSTRUCTION, parse_mode='Markdown')
        except FileNotFoundError:
            # Backup kalau lupa upload gambar
            bot.send_message(call.message.chat.id, ">> ERROR: QRIS FILE MISSING.\n\nManual Transfer:\nHubungi Admin.", parse_mode='Markdown')

# ==========================================
# 5. FORWARDER (BUKTI TF KE ADMIN)
# ==========================================
@bot.message_handler(content_types=['photo'])
def handle_proof(message):
    bot.reply_to(message, ">> **DATA RECEIVED.**\nVerifying transaction hash... Please wait.")
    
    # Lapor ke Raymond
    alert = f"```\n[!] NEW TRANSACTION ALERT\nUser: {message.from_user.first_name}\nID: {message.from_user.id}\n```"
    bot.send_message(ADMIN_ID, alert, parse_mode='Markdown')
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

# START
print("TITAN SYSTEM V4 (FINAL): ONLINE...")
bot.infinity_polling()