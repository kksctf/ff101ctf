#!/usr/bin/env python

'''
plan
Accept-Language https://flaviocopes.com/http-request-headers/#accept-language
Date https://flaviocopes.com/http-request-headers/#date
User-Agent 
Accept


idea

Date = Помню было 24 января 1999 года...
Accept-Language = Я должен был встретится c связным из Чехии...
User-Agent = Агентом был служащий, позывным "Рысь"... (Lynx, текстовый браузер)
Accept = От него я ожидал получить фотоматериалы объекта... (image/png)

Но Он мне передал лишь записку: Вы раскрыты, ваш новый пароль - ptctf{...}


Solve:
curl --header 'Date: Tue, 24 Jan 1999' --header 'Accept-Language: cs-cs' --header 'User-Agent: Lynx/2.8.9' --header 'Accept: image/png' http://0.0.0.0:5000/
'''


from flask import Flask, request, render_template
from secret import flag
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    flag_Language = False
    flag_Agent = False
    flag_Accept = False
    flag_flag = False

    date = request.headers.get('Date')
    if date != None and "1999" in date and "24 Jan" in date:
        flag_Language = True
    
    language = request.headers.get('Accept-Language')
    if language != None and ("cs" in language.lower() or "cz" in language.lower()):
        flag_Agent = True
    
    agent = request.headers.get('User-Agent')
    if agent != None and "Lynx" in agent:
        flag_Accept = True
    
    filetype = request.headers.get('Accept')
    if filetype != None and "image/png" in filetype:
        flag_flag = True
    
    return render_template('index.html', f = flag, f_flag = flag_flag, f_accept = flag_Accept, f_agent = flag_Agent, f_lang = flag_Language)

#app.run(host='0.0.0.0', port=5000, debug=True)
app.run(host='0.0.0.0', port=5000, debug=False)
