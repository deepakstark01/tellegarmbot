import os
import json
import random
import logging
import datetime
from datetime import date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import pandas as pd
import openpyxl
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

ENTER_NAME, ENTER_AUSERNAME, ENTER_PHONE, ENTER_WITHDRAWAL_AMOUNT = range(4)


import os

folder_path = "images"  # Replace with the actual folder path

image_files = []
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        file_path = os.path.join(folder_path, filename)
        image_files.append(file_path)

# print(image_files)

# ad_messages = [
#     "🌈 This is the way to learn about making money",
#     "💼 Let's explore the opportunities to earn",
#     "🚀 Your journey to financial freedom starts here",
#     "💰 The secret to wealth lies in learning",
#     "🎯 Watch and learn, earn and grow",
#     "🎁 Opportunity is knocking on your door",
#     "💎 Unleash the power of ads for earnings"
# ]
orderOfINdex=0
ImageIndex=0
ad_messages = [
    "🌈 هذه هي الطريقة لتعلم كيفية جني المال",
    "💼 دعونا نستكشف الفرص لكسب المال",
    "🚀 رحلتك نحو الحرية المالية تبدأ هنا",
    "💰 سر الثروة يكمن في التعلم",
    "🎯 شاهد وتعلم، اكسب ونمو",
    "🎁 الفرصة تطرق بابك",
    "💎 استخدم قوة الإعلانات للربح"
]

def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as file:
            return json.load(file)
    return {}

def save_user_data(user_data):
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file)

def save_payment_info(user_id: str, name: str, atrex_username: str, phone: str) -> None:
    # with open('payment_info.txt', 'a') as file:
    #     file.write(f"{user_id} - {name} - {atrex_username} - {phone}\n")
    file_path = "payment_info.xlsx"
    sheet_name = 'Payment Info'
    data = {'User ID': [user_id], 'Name': [name], 'Atrex Username': [atrex_username], 'Phone': [phone]}
    new_df = pd.DataFrame(data)
    print(data)
    if os.path.isfile(file_path):  # Check if the file exists
        try:

            existing_df = pd.read_excel(file_path)
            df = existing_df.append(new_df, ignore_index=True)
            print(df)
            df.to_excel( file_path,sheet_name=sheet_name, index=False)
        except Exception as e:
            print(f"An error occurred while saving payment information: {str(e)}")
    else:
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:

                new_df.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception as e:
            print(f"An error occurred while saving payment information: {str(e)}")


def get_new_ad_links(user_id, user_data, count=2):
    with open('ads.txt', 'r') as file:
        ads = file.read().splitlines()
    user_data.setdefault(user_id, {}).setdefault('seen_ads', [])
    unseen_ads = [ad for ad in ads if ad not in user_data[user_id]['seen_ads']]
    if unseen_ads:
        new_ads = unseen_ads[:count]
        user_data[user_id]['seen_ads'].extend(new_ads)
        save_user_data(user_data)
        return new_ads
    else:
        return None


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("❓  شرح البوت", callback_data='1'),

        ],
        [
            InlineKeyboardButton("📋 معلومات حسابي", callback_data='2'),
            InlineKeyboardButton("", callback_data='empty_button'),
            InlineKeyboardButton("👫 دعوة الاصدقاء", callback_data='4')

        ],
        # [InlineKeyboardButton("👫 دعوة الاصدقاء", callback_data='4')],
        [
            InlineKeyboardButton("🎬 👁️‍🗨️مشاهدة الاعلانات", callback_data='5'),
            InlineKeyboardButton("", callback_data='empty_button'),
            InlineKeyboardButton("💸 سحب الأرباح", callback_data='6')

        ],

        [
            InlineKeyboardButton("💳 أضافة معلومات السحب", callback_data='7')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    user_id = str(update.effective_user.id if update.effective_user else update.callback_query.from_user.id)
    user_data = load_user_data()
    if user_id not in user_data:
        user_data[user_id] = {
            'coins': 0,
            'ads_watched_today': 0,
            'invite_code': user_id,
            'seen_ads': []
        }
        save_user_data(user_data)

    if update.effective_message:
        update.effective_message.reply_text('✅ انت الان في القائمة الرئيسية لتحديث القائمة اضغط /start', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=user_id, text='🔝 القائمة الرئيسية')
        update.effective_message.reply_text('✅ انت الان في القائمة الرئيسية لتحديث القائمة اضغط /start',
                                            reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_id = str(query.from_user.id)
    user_data = load_user_data()
    keyboard = [
        [InlineKeyboardButton("🏠 العودة إلى القائمة", callback_data='menu')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    privousAndhome = [
        [
            InlineKeyboardButton("🏠 العودة إلى القائمة", callback_data='menu'),
            InlineKeyboardButton("", callback_data='empty_button'),

            InlineKeyboardButton("الإعلان التالي⏭️", callback_data='5')
         ]

    ]

    reply_NextANdHome = InlineKeyboardMarkup(privousAndhome)

    if query.data == '1':
        formatted_text = "✅ طريقة الدفع الموجودة في البوت يمكنك السحب منها عن طريق منصة atrex\n\nتنويه:\nيمكنك السحب فقط اذا كان رصيدك 100 درهم في البوت او اكثر ✅\n\nطريقة الربح في البوت:\n\n1⃣ تقوم بالدخول الى بوت  #ربح_الدرهم  ثم الضغط على زر 👫 دعوة الاصدقاء\n\n2⃣ ثم قم بنسخ الرابط الذي سيعطيك البوت إياه وتقوم بأرساله الى أصدقائك.\n\n3⃣ عندما يقوم شخص جديد بالدخول على رابطك الخاص ستحصل على 5 دراهم.\n\n✅ يمكنك السحب فقط عندما تصل إلى 100 درهم بدون أي مشاكل وبدون أي رسوم للسحب."
        query.edit_message_text(text=formatted_text, reply_markup=reply_markup)

    elif query.data == '2':
        # query.edit_message_text(text=f"Telegram ID:  {user_id}\nCoins: {user_data[user_id]['coins']}\nAds watched today: {user_data[user_id]['ads_watched_today']}\nInvite code: {user_data[user_id]['invite_code']}", reply_markup=reply_markup)
        # arabic_text = f"معرف تليجرام: {user_id}\الأرباح : {user_data[user_id]['coins']}\nالإعلانات المشاهدة اليوم: {user_data[user_id]['ads_watched_today']}\nرمز الدعوة: {user_data[user_id]['invite_code']}"
        arabic_text = f"معرف تليجرام: {user_id}\nالأرباح بالدرهم: {user_data[user_id]['coins']}\nالإعلانات المشاهدة اليوم: {user_data[user_id]['ads_watched_today']}\nرمز الدعوة: {user_data[user_id]['invite_code']}"

        query.edit_message_text(text=arabic_text, reply_markup=reply_markup)

    elif query.data == '4':
        # query.edit_message_text(text=f"Your invite code is {user_data[user_id]['invite_code']}.", reply_markup=reply_markup)
        query.edit_message_text(
            text=f". رمز الدعوة الخاص بك هو:{user_data[user_id]['invite_code']} \n💰 شارك الرمزك مع أصدقائك وكل شخص يأتي من خلال هذا الرابط الخاص بك سوف تكسب 40 درهم",
            reply_markup=reply_markup)

        # query.edit_message_text(text=f"رمز الدعوة الخاص بك هو \n 💰 شارك الرمزك مع اصدقائك وكل شخص يأتي من خلال هذا الرابط الخاص بك سوف تكسب 40 درهم{user_data[user_id]['invite_code']}.",reply_markup=reply_markup)

    elif query.data == '5':
        new_ads = get_new_ad_links(user_id, user_data, count=1)
        global numberOfads
        if user_data[user_id]['ads_watched_today'] <=10:
            if new_ads:
                for ad in new_ads:
                    print("hey")
                    global orderOfINdex
                    global ImageIndex
                    if(orderOfINdex>6):
                        orderOfINdex=0
                    if (ImageIndex >=10):
                        orderOfINdex = 0
                    motivational_message = ad_messages[orderOfINdex]
                    image_file = image_files[ImageIndex]
                    combined_message = f"{motivational_message}\n\n{ad}"
                    with open(image_file, 'rb') as file:
                        context.bot.send_photo(chat_id=user_id, photo=file, caption=combined_message)
                    ImageIndex+=1
                    orderOfINdex+=1


                    # Change the order of ad and message here
                    # combined_message = f"{motivational_message}\n\n{ad}"
                    # context.bot.send_message(chat_id=user_id, text=combined_message)
                user_data[user_id]['coins'] += len(new_ads)
                user_data[user_id]['ads_watched_today'] += len(new_ads)
                save_user_data(user_data)
                rplmsg=f"لقد شاهدت {len(new_ads)} إعلانات وحصلت على {len(new_ads)} عملة."
                # query.edit_message_text(text=f"You have watched {len(new_ads)} ads and earned {len(new_ads)} coins.", reply_markup=reply_markup)
                # query.edit_message_text(text=f"لقد شاهدت {len(new_ads)} إعلانات وحصلت على {len(new_ads)} عملة.")
                query.message.reply_text(text=rplmsg, reply_markup=reply_NextANdHome)
            else:
                # query.edit_message_text(text="No new ads available at the moment.", reply_markup=reply_markup)
                query.edit_message_text(text="لا توجد إعلانات جديدة في الوقت الحالي.", reply_markup=reply_markup)
        else:
            # query.edit_message_text(text="No new ads available at the moment.", reply_markup=reply_markup)
            query.edit_message_text(text="لا توجد إعلانات جديدة في الوقت الحالي.", reply_markup=reply_markup)

    elif query.data == '6':
        if 'name' in context.user_data and 'atrex_username' in context.user_data and 'phone' in context.user_data:
            if user_data[user_id]['coins'] >= 100:
                # query.edit_message_text(text="Please enter the amount of coins you want to withdraw:")
                query.edit_message_text(text="الرجاء إدخال كمية العملات التي ترغب في سحبها:")
                return ENTER_WITHDRAWAL_AMOUNT
            else:
                # query.edit_message_text(text="You do not have enough coins to make a withdrawal. You need at least 100 coins.", reply_markup=reply_markup)
                query.edit_message_text(
                    text="ليس لديك عدد كافٍ من العملات لإجراء عملية السحب. تحتاج على الأقل إلى 100 درهم.",
                    reply_markup=reply_markup)

        else:
            # query.edit_message_text(text="You need to enter your payment information first. Please go back to the main menu and click on 'Payment information'.", reply_markup=reply_markup)
            query.edit_message_text(
                text="يجب عليك إدخال معلومات الدفع أولاً. يرجى العودة إلى القائمة الرئيسية والنقر على 'أضافة معلومات السحب'.",
                reply_markup=reply_markup)

    elif query.data == '7':
        # query.edit_message_text(text="Please type your first and last name:")
        query.edit_message_text(text="يرجى كتابة الاسم الكامل:")
        return ENTER_NAME
    else:
        start(update, context)

def enter_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    # update.message.reply_text('Please enter your AtrexTrade username:')
    update.message.reply_text('الرجاء إدخال اسم مستخدم Atrex الخاص بك:')
    return ENTER_AUSERNAME

def enter_ausername(update: Update, context: CallbackContext) -> int:
    context.user_data['atrex_username'] = update.message.text
    # update.message.reply_text('Please enter your phone number:')
    update.message.reply_text('يرجى إدخال رقم الهاتف الخاص بك:')
    return ENTER_PHONE

def enter_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    user_id = str(update.effective_user.id if update.effective_user else update.callback_query.from_user.id)
    save_payment_info(user_id, context.user_data['name'], context.user_data['atrex_username'], context.user_data['phone'])
    # update.message.reply_text('Your payment information has been saved.')
    update.message.reply_text('تم حفظ معلومات الدفع الخاصة بك.')
    return ConversationHandler.END

def enter_withdrawal_amount(update: Update, context: CallbackContext) -> int:
    withdrawal_amount = int(update.message.text)
    user_id = str(update.effective_user.id if update.effective_user else update.callback_query.from_user.id)
    user_data = load_user_data()
    if withdrawal_amount <= user_data[user_id]['coins']:
        user_data[user_id]['coins'] -= withdrawal_amount
        save_user_data(user_data)
        update.message.reply_text(f"لقد انسحبت بنجاح {withdrawal_amount} عملات معدنية.")
    else:
        # update.message.reply_text(f"You do not have enough coins. You only have {user_data[user_id]['coins']} coins.")
        update.message.reply_text(f"ليس لديك عملات كافية. انت فقط لديك {user_data[user_id]['coins']} عملات معدنية.")
    return ConversationHandler.END

def reply_to_message(update, context):
    if update.message.chat.type == 'private':  # Check if the message is from a private chat
        text = update.message.text.lower()
        if text != '/start':
            context.bot.send_message(chat_id=update.effective_chat.id, text='❌امر خاطئ يرجى ارسال الأمر /start والمحاولة لاحقا.')


def main():
    # updater = Updater("5969940555:AAH9qqoxv7tOjYkFS47J81edXf-ZuZWeSjI", use_context=True)
    updater = Updater("5730090964:AAHRPNAsvUhppMC-V-yg9JEHDbVM7U9at_k", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CallbackQueryHandler(button)],
        states={
            ENTER_NAME: [MessageHandler(Filters.text & ~Filters.command, enter_name)],
            ENTER_AUSERNAME: [MessageHandler(Filters.text & ~Filters.command, enter_ausername)],
            ENTER_PHONE: [MessageHandler(Filters.text & ~Filters.command, enter_phone)],
            ENTER_WITHDRAWAL_AMOUNT: [MessageHandler(Filters.text & ~Filters.command, enter_withdrawal_amount)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(
        MessageHandler(Filters.text & ~Filters.command, reply_to_message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
