from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import time
from ..bot import LazadaBot
import json
import random

global bot
bot = LazadaBot()

@socketio.on('joined')
def joined(message):
    print(message)
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name')}, room=room)
    emit('find_product','ntap')
  
    

@socketio.on('search_lazada')
def search_lazada(message):
    # data = {
    #     "title": f"{random.randint(1,101)} Promo Notebook Baru Asus A407MA-BV001T - Intel® Celeron® N4000 - RAM 4GB - 1TB - Intel UHD Graphics 600 - 14.0' - W10 - Grey - Laptop Murah (Gratis Tas) - Bergansi",
    #     "price_now": "Rp3.909.000",
    #     "location": "Jawa barat",
    #     "discount_price": "Rp195.000",
    #     "discount_percent": "-31%",
    #     "img_link": "https://id-test-11.slatic.net/p/93dbd5ff8c8b02ccf88c7d4ef68aa748.jpg",
    #     "link": "https://www.lazada.co.id/products/denim-original-hitam-i143570579-s157343054.html?search=1"
    # }
    # emit('response_search_lazada', json.dumps(data))
    if message['keyword']:

       
        bot.start_bot(message['keyword'])
        bot.run_finding()


@socketio.on('stop_searching')
def stop_searching(message):
    print(message)
    print(50*'=')
    bot.stop_bot()
