#
#
# File: fontanelle
# Authors: Talha Imran, Kasun Rajapaksha, Gianmario Fiorini, Shady Khalaile, Cristian Motoc
# Date: 27/06/2022
# Description: ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
##Il nostro bot sarà la salvezza per quelle persone o animali che stanno morendo di sete,
##questo bot ti consentirà di vedere una mappa di tutte le fontanelle, oppure dirti la posizione della fontana più vicina,
##con la quale poi potresti, volendo, avere indicazioni tramite google maps.
##Tutto questo sia in italiano che in Inglese!
##Buona bevuta sostenibile! :)
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
##Our bot is going be the saving for those people of animals that are dying of thirst,
##this bot will allow you to see a map of all public fountain, or telling you the position of the nearest fountain to you,
##and use google maps to get to it.
##All this both in Italian and in english!
##Have a good drink! :)
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

from telegram import *
from telegram.ext import *
import sqlite3
from math import radians, cos, sin, asin, sqrt

#var of bottons#

#italiano
italiano = "Italiano  🇮🇹"
fontanella_vicina_it = "Indicazioni per la fontanella più vicina  ➤"
fontanelle_Verona_it = "Mappa delle fontanelle di Verona  🗺"
cambia_lingua_it="Cambia lingua / Change language\n⇦ 🇮🇹 / 🇬🇧 / 🇺🇸"
tutorial_it="Come inviare la posizione 🔧"
indietro_it="Torna indietro ⇦"
tutorial_ios_it=" iOS "
tutorial_android_it="🤖  Android  🤖"
tutorial_indietro_it="Torna indietro  ⇦"
quiz_it="Quiz 📝"

#inglese
inglese = "English 🇬🇧 / 🇺🇸"
fontanella_vicina_en = "Directions to the nearest drinking fountain ➤"
fontanelle_Verona_en = "Map of Verona's drinking fountains 🗺"
cambia_lingua_en="Change language / Cambia lingua\n⇦ 🇮🇹 / 🇬🇧 / 🇺🇸"
tutorial_en="Tutorial 🔧"
indietro_en="Go back ⇦"
tutorial_ios_en="  iOS  "
tutorial_android_en="🤖 Android 🤖"
tutorial_indietro_en="Go back  ⇦"
quiz_en="Quiz  📝"

####funtions###

def startCommand(update: Update, context: CallbackContext) -> None:
    diz(update, context)
    aggiungi_dizionario(update, context, dizionario)
    buttons = [[KeyboardButton(italiano)], [KeyboardButton(inglese)]]
    testo = "Benvenuto nel nostro bot\nScegli la lingua 🇮🇹"
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
    testo = "Welcome to our bot\nChose the language 🇬🇧 / 🇺🇸"
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))

def diz(update: Update, context: CallbackContext):
    global dizionario
    dizionario = {
        "chat_id" : update.effective_chat.id,
        "lingua" : context.bot_data["lingua"]
    }
    
def aggiungi_dizionario(update: Update, context: CallbackContext, dizionario):
    if len(lista) == 0:
       lista.append(dizionario)
    trovato = False
    for i in range(len(lista)):
        if(lista[i]['chat_id'] == update.effective_chat.id):
            trovato = True
            dizionario = {
                "chat_id" : update.effective_chat.id,
                "lingua" : context.bot_data["lingua"]
            }
            lista[i] = dizionario
    if trovato == False:
        lista.append(dizionario)
    print(lista)
    print("")

def fontanella_vicina(update: Update, context: CallbackContext) -> None:
    try:
        global user_id
        lat1 = update.message.location.latitude
        lon1 = update.message.location.longitude
        d = []
        for i in range(0,len(coord_x)):
            d.append(distanza(lat1,lon1,coord_x[i],coord_y[i]))
        e = d[:]
        d.sort()
        ind = 0
        for i in range(0,len(d)):
            if d[0]==e[i]:
                ind = i
                break
        for i in range (len(lista)):
            if lista[i]["chat_id"] == update.effective_chat.id:
                user_id = update.effective_chat.id
                break
        if lista[i]["lingua"] == "it":
            testo_nome = "La fontanella più vicina è: " + denominazioni[ind]
            testo_distanza = "\nDistanza: " + str(round(d[0])) + " m"
            testo_circoscrizione= "\nCircoscrizione: " + circoscrizioni[ind]
            testo_via= "\nVia: " + nome_via[ind]
            context.bot.send_message(chat_id=user_id, text=testo_nome+testo_circoscrizione+testo_via+testo_distanza)
            update.message.reply_location(coord_x[i], coord_y[i])
        elif lista[i]["lingua"] == "en":
            testo_nome = "The closest fontanel is: " + denominazioni[ind]
            testo_distanza = "\nDistance: " + str(round(d[0])) + " m"
            testo_circoscrizione= "\nCircumscriptions: " + circoscrizioni[ind]
            testo_via= "\nStreet name: " + nome_via[ind]
            context.bot.send_message(chat_id=user_id, text=testo_nome+testo_circoscrizione+testo_via+testo_distanza)
            update.message.reply_location(coord_x[i], coord_y[i])
    except:
        #print(exception)
        testo_try = "Error 404"
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo_try)

def distanza(lat1,lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return((c * r)*1000)

def mappa_it(update: Update, context: CallbackContext):
    update.message.reply_text(
    'Clicca qua ⇩',
    reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton(text='mappa', url='http://u.osmfr.org/m/780217/')],]))

def send_tutorial_ios_it(update, context):
    chat_id = update.message.chat_id
    document1 = open('tutorial_ios_it.pdf', 'rb')
    context.bot.send_document(chat_id, document1)

def send_tutorial_android_it(update, context):
    chat_id = update.message.chat_id
    document1 = open('tutorial_android_ita.pdf', 'rb')
    context.bot.send_document(chat_id, document1)

def mappa_en(update: Update, context: CallbackContext):
    update.message.reply_text(
    'Click here ⇩',
    reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton(text='map', url='http://u.osmfr.org/m/780217/')],]))

def send_tutorial_ios_en(update, context):
    chat_id = update.message.chat_id
    document1 = open('tutorial_ios_en.pdf', 'rb')
    context.bot.send_document(chat_id, document1)

def send_tutorial_android_en(update, context):
    chat_id = update.message.chat_id
    document1 = open('tutorial_android_en.pdf', 'rb')
    context.bot.send_document(chat_id, document1)

def messageHandler(update: Update, context: CallbackContext):
    global lista
    if len(lista) > 100:
        lista = []
        diz(update, context)
        aggiungi_dizionario(update, context, dizionario)
    
    presente = False
    
    for i in range (len(lista)):
        if lista[i]["chat_id"] == update.effective_chat.id:
            user_id = update.effective_chat.id
            presente = True
            break
        
    print(lista, "**********************", len(lista))
    print(presente)
    
    if presente == False:
        diz(update, context)
        aggiungi_dizionario(update, context, dizionario)
        for i in range (len(lista)):
            if lista[i]["chat_id"] == update.effective_chat.id:
                user_id = update.effective_chat.id
                presente = True
                break
        
    if presente == True:
        #italiano
        if italiano in update.message.text:
            buttons = [[KeyboardButton(fontanella_vicina_it)], [KeyboardButton(fontanelle_Verona_it)], [KeyboardButton(quiz_it)], [KeyboardButton(cambia_lingua_it)]]
            context.bot.send_message(chat_id=user_id, text="Benvenuto!!!\nQuesto bot ti permette di trovare la fontanella più vicina a te.", reply_markup=ReplyKeyboardMarkup(buttons))

        if quiz_it in update.message.text:
            update.message.reply_text(
            'Clicca qua ⇩',
            reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Quiz', url='https://take.panquiz.com/9767-6114-0080')],]))

        if fontanella_vicina_it in update.message.text:
            context.bot_data["lingua"] = "it"
            diz(update, context)
            aggiungi_dizionario(update, context, dizionario)
            testo = "Invia la tua posizione 📍 o vedi il tutorial"
            buttons = [[KeyboardButton(tutorial_it)], [KeyboardButton(indietro_it)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
            dispatcher.add_handler(MessageHandler(Filters.location, fontanella_vicina))

        if indietro_it in update.message.text:
            context.bot_data["lingua"] = ""
            diz(update, context)
            aggiungi_dizionario(update, context, dizionario)
            testo = "Scegli un'opzione"
            buttons = [[KeyboardButton(fontanella_vicina_it)], [KeyboardButton(fontanelle_Verona_it)], [KeyboardButton(quiz_it)], [KeyboardButton(cambia_lingua_it)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))

        if tutorial_it in update.message.text:
            testo = "1 -> clicca la '📎'\n2 -> clicca su 'posizione'\n3 -> clicca su 'invia la mia posizione attuale'"
            buttons = [[KeyboardButton(tutorial_ios_it)], [KeyboardButton(tutorial_android_it)], [KeyboardButton(tutorial_indietro_it)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
            testo = "O scegli il tuo sistema operativo per scaricare un tutorial con immagini"
            context.bot.send_message(chat_id=user_id, text=testo)
        
        if tutorial_ios_it in update.message.text:
            send_tutorial_ios_it(update, context)
        
        if tutorial_android_it in update.message.text:
            send_tutorial_android_it(update, context)
        
        if tutorial_indietro_it in update.message.text:
            testo = "Scegli un'opzione"
            buttons = [[KeyboardButton(fontanella_vicina_it)], [KeyboardButton(fontanelle_Verona_it)], [KeyboardButton(quiz_it)], [KeyboardButton(cambia_lingua_it)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
        
        if fontanelle_Verona_it in update.message.text:
            mappa_it(update, context)
        
        if cambia_lingua_it in update.message.text:
            context.bot_data["lingua"] = ""
            diz(update, context)
            aggiungi_dizionario(update, context, dizionario)
            buttons = [[KeyboardButton(italiano)], [KeyboardButton(inglese)]]
            testo = "Scegli la lingua"
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
        
        #Inglese
        if inglese in update.message.text:
            buttons = [[KeyboardButton(fontanella_vicina_en)], [KeyboardButton(fontanelle_Verona_en)],[KeyboardButton(quiz_en)],[KeyboardButton(cambia_lingua_en)]]
            context.bot.send_message(chat_id=user_id, text="Welcome !!! \nThis bot allows you to find the nearest drinking fountain.", reply_markup=ReplyKeyboardMarkup(buttons))

        if quiz_en in update.message.text:
            update.message.reply_text(
            'Click here ⇩',
            reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Quiz', url='https://take.panquiz.com/9309-2766-0228')],]))

        if fontanella_vicina_en in update.message.text:
            context.bot_data["lingua"] = "en"
            diz(update, context)
            aggiungi_dizionario(update, context, dizionario)
            testo = "Send your location 📍 or watch the tutorial"
            buttons = [[KeyboardButton(tutorial_en)], [KeyboardButton(indietro_en)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
            dispatcher.add_handler(MessageHandler(Filters.location, fontanella_vicina))

        if indietro_en in update.message.text:
            context.bot_data["lingua"] = ""
            diz(update, context)
            aggiungi_dizionario(update, context, dizionario)
            testo = "Choose an option"
            buttons = [[KeyboardButton(fontanella_vicina_en)], [KeyboardButton(fontanelle_Verona_en)],[KeyboardButton(quiz_en)],[KeyboardButton(cambia_lingua_en)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))

        if tutorial_en in update.message.text:
            testo = "1 -> click on '📎'\n2 -> click on 'position'\n3 -> click on 'send my current position'"
            buttons = [[KeyboardButton(tutorial_ios_en)], [KeyboardButton(tutorial_android_en)], [KeyboardButton(tutorial_indietro_en)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
            testo = "Or choose your operating system to download a tutorial with pictures"
            context.bot.send_message(chat_id=user_id, text=testo)
        
        if tutorial_ios_en in update.message.text:
            send_tutorial_ios_en(update, context)
        
        if tutorial_android_en in update.message.text:
            send_tutorial_android_en(update, context)
        
        if tutorial_indietro_en in update.message.text:
            testo = "Choose an option"
            buttons = [[KeyboardButton(fontanella_vicina_en)], [KeyboardButton(fontanelle_Verona_en)],[KeyboardButton(quiz_en)],[KeyboardButton(cambia_lingua_en)]]
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))
        
        if fontanelle_Verona_en in update.message.text:
            mappa_en(update, context)
        
        if cambia_lingua_en in update.message.text:
            context.bot_data["lingua"] = ""
            diz(update, context)
            aggiungi_dizionario(update, context, dizionario)
            buttons = [[KeyboardButton(italiano)], [KeyboardButton(inglese)]]
            testo = "Choose language!"
            context.bot.send_message(chat_id=user_id, text=testo, reply_markup=ReplyKeyboardMarkup(buttons))

#main#  
def main():
    global dispatcher
    global lista
    lista = []
    with open("token.txt", "r") as f:
        TOKEN = f.read()
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", startCommand))
    dispatcher.bot_data = {"lingua" : ""}
    dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    ##var_of_array##
    nome_via=[]
    circoscrizioni=[]
    denominazioni=[]
    coord_x = []
    coord_y = []

    con = sqlite3.connect("fontanelle.db")
    n_via=con.execute(""" SELECT nome_via FROM fontanelle; """).fetchall()
    circ=con.execute(""" SELECT circoscrizione from fontanelle; """).fetchall()
    denom=con.execute(""" SELECT denominazione from fontanelle; """).fetchall()
    x=con.execute(""" SELECT coordinate_x FROM fontanelle; """).fetchall()
    y=con.execute(""" SELECT coordinate_y FROM fontanelle; """).fetchall()

    for i in range(0,len(n_via)):
        nome_via.append(n_via[i][0])
        circoscrizioni.append(circ[i][0])
        denominazioni.append(denom[i][0])
        coord_x.append(x[i][0])
        coord_y.append(y[i][0])
    main()
