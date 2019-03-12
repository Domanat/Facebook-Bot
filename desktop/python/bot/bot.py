#Python libraries that we need to import for our bot
import random
import os
import json
from enum import Enum
from pymessenger import utils
from requests_toolbelt import MultipartEncoder
from flask import Flask, request
import requests
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAFZCAUm6cc4BAOLirdZCGowSAckVl2vTJ3ZBunQiWVoyJgZAX7z7vZBWm2SlmSyK3vvISZAMDvPQdTtbB3zXmReKtpPZALfJGrgk0hEzUZCZCdGKVu49dDtvJabdM0vQD5yzkGjyhDegHZAkWn4D9Gz3dZAvVZCornjEAqd85YEZClTxZC7kPkCsnIMLd'
VERIFY_TOKEN = 'TESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    memes1 = ['https://cs5.pikabu.ru/post_img/2014/07/08/7/1404815096_184432026.jpg',
              'http://memesmix.net/media/created/250/wux0q1.jpg',
              'https://scontent-lhr3-1.cdninstagram.com/vp/71cfc8c1f88706ff91ef7b99e6a8299f/5D13F4F9/t51.2885-15/e35/51159508_1235705929972875_3021547323884175349_n.jpg?_nc_ht=scontent-lhr3-1.cdninstagram.com&se=7&ig_cache_key=MTk4MDU1NDQyNDUzMTI0NjM4Nw%3D%3D.2',
              'https://leonardo.osnova.io/e06db842-0fdb-f553-51d8-c0d2c1ebb4fb/-/scale_crop/764x764/center/-/format/webp/',
              'https://memepedia.ru/wp-content/uploads/2019/02/1463047511138746845-1.jpg',
              'https://scontent-ams3-1.cdninstagram.com/vp/f976155e74fd8b9eb6f8b46e4f10bc25/5D1BE08A/t51.2885-15/sh0.08/e35/c0.7.1080.1080/s640x640/50666318_568754516972263_2655498064769340756_n.jpg?_nc_ht=scontent-ams3-1.cdninstagram.com',
              'https://www.meme-arsenal.com/memes/3c381dc5b71e360d3b9da4c662870b97.jpg',
              'https://scontent-ams3-1.cdninstagram.com/vp/f81ddbca6025ffde84425584ff0c9aa2/5CECC2F2/t51.2885-15/sh0.08/e35/c0.58.1080.1080/s640x640/49858742_387098008715629_4502278241435457921_n.jpg?_nc_ht=scontent-ams3-1.cdninstagram.com',
              'https://pp.userapi.com/c850628/v850628016/b60c5/zN4hXBCPNoI.jpg',
              'https://pp.userapi.com/c846217/v846217351/195172/TUrgKg1LdRs.jpg']

    memes2 = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEd8E_TOwLCvm6uUWIOqOlpit1n8xvGWLb6b-Ivr41Wzs0uTt7GA',
              'https://img.anews.com/media/gallery/102996838/650248535.jpg',
              'https://pbs.twimg.com/media/DwnHXqMXcAESyAL.jpg',
              'http://images3.memedroid.com/images/UPLOADED101/5c4f905aeb983.jpeg',
              'https://www.meme-arsenal.com/memes/1d38c8b60d5e5dec3ee769851db4ef90.jpg']


    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        recipient_id = output['entry'][0]['messaging'][0]['sender']['id']
        payload = {
                "recipient":{
                  "id": recipient_id
                },
                "message":{
                  "attachment":{
                    "type":"template",
                     "payload":{
                      "template_type":"button",
                      "text":"Choose meme theme",
                      "buttons":[
                        {
                          "type":"postback",
                          "title": "Kolyvan",
                          "payload":"first_button"
                        },
                        {
                          "type":"postback",
                          "title": "Ricardo",
                          "payload":"second_button"
                        }
                      ]
                    }
                  }
                }
            }

        for event in output['entry']:
           for message in event['messaging']:
            if message.get('message'):
                if message['message'].get('text'):
                    if 'hello' in message['message'].get('text').lower():
                        send_message(recipient_id, " Hi, dude!")
                    elif 'hi' in message['message'].get('text').lower():
                        send_message(recipient_id, " Hi!")

                    elif 'kolyvan' in message['message'].get('text').lower():   
                        bot.send_image_url(recipient_id, random.choice(memes1))

                    elif 'ricardo' in message['message'].get('text').lower():
                        bot.send_image_url(recipient_id, random.choice(memes2))

                    else: 
                        text = get_message()
                        send_message(recipient_id, "Enter text from button or click on a button")

                    bot.send_raw(payload)

            if message.get("postback"):
                if message['postback']['title'].lower() == "kolyvan":
                    bot.send_image_url(recipient_id, random.choice(memes1))

                elif message['postback']['title'].lower() == "ricardo":
                    bot.send_image_url(recipient_id, random.choice(memes2))
                bot.send_raw(payload)
                
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, message):
    bot.send_text_message(recipient_id, message)
    return "success"

if __name__ == "__main__":
    app.run()