from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Main page, nothing special..."

@app.route('/mail')
def mail():
    try:
        from connector import MailConnector
        login, password, imap_server, m_id = request.args.get('l'), request.args.get('p'), request.args.get('i'), request.args.get('mid')
        mail = MailConnector(login, password, imap_server)
        if mail.connect() == True:
            mail_text = mail.get_mail_text(str(m_id), False)
            return f'{mail_text}'
        else:
            return f'Неверный логин или пароль: {mail.connect()}'
    except Exception as e:
        return f'Произошла ошибка: {str(e)}'

@app.route('/retell')
def retell():
    try:
        from connector import MailConnector
        login, password, imap_server, m_id, key = request.args.get('l'), request.args.get('p'), request.args.get('i'), request.args.get('mid'), request.args.get('key')
        mail = MailConnector(login, password, imap_server)
        if mail.connect() == True:
            mail_text = mail.get_mail_text(str(m_id), False)
            #return f'{mail_text}'
            from gigachat import GigaChat
            model = GigaChat(
               credentials=key,
               scope="GIGACHAT_API_PERS",
               model="GigaChat",
               verify_ssl_certs=False,
            )
            response = model.chat(f"Перескажи письмо в нескольких предложениях от лица отправителя письма. В твоем ответе должен быть только пересказ. Если по каким-либо причинам пересказ сделать невозможно (например, письмо состоит из шифра), ответь сообщением "Не удалось распознать текст письма".: {mail_text}")

            return f'{response.choices[0].message.content}'
        else:
            return f'Неверный логин или пароль: {mail.connect()}'
    except Exception as e:
        return f'Произошла ошибка: {str(e)}'

app.run(host='0.0.0.0',port=1080)
