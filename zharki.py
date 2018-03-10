import random
import time
import os
import traceback
import praw

import zharki_img
import login

def bot_login(): #para el login del bot
    print("preparando login...")
    try:
        reddit = praw.Reddit(
            client_id = login.client_id,
            client_secret = login.client_secret,
            password = login.password,
            username = login.username,
            user_agent = 'testscript for /u/zharkibot')
        print("logueado... :D ")
    except Exception as exception:
        print("Error en el login!! (╯°□°)╯︵ ┻━┻ " + str(exception) + "\n" + traceback.format_exc())
    return reddit

def run_bot(reddit, comentarios_respondidos):
    for comment in reddit.subreddit('test').comments(limit=25):
        if "/s" in comment.body  and comment.id not in comentarios_respondidos and not comment.author == reddit.user.me():
            keys = list(zharki_img.topics.keys())
            random.shuffle(keys)
            key = random.choice(keys)
            respuesta = "wow **" + str(comment.author) + "** parece que no estás muy [atento]("+zharki_img.topics[key]+")..."
            respuesta += "\n****\n"
            respuesta += "bot by u/apmauj. [source](https://github.com/apmauj/zharki_bot)"
            comment.reply(respuesta)
            print("respondiendo el comentario comment id: " + comment.id)
            #comentarios_respondidos.append(comment.id)
            with open("comm_resp.txt", "a") as f:
                f.write(comment.id + "\n")
            #print(comentarios_respondidos)
            print("durmiendo por 10 segundos")
            time.sleep(10)

def comentarios_salvados():
    if not os.path.isfile("comm_resp.txt"):
        comentarios_respondidos = []
    else:
        with open("comm_resp.txt", "r") as f:
            comentarios_respondidos = f.read()
            comentarios_respondidos = comentarios_respondidos.split("\n")
            comentarios_respondidos = filter(None, comentarios_respondidos)
    return comentarios_respondidos

reddit = bot_login()
while True:
    comentarios_respondidos = comentarios_salvados()
    try:
        run_bot(reddit, comentarios_respondidos)
    except Exception as exception:
        print("Error ejecutando el bot!! (╯°□°)╯︵ ┻━┻ -> " + str(exception))
        #print(traceback.format_exc())