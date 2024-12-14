from flask import Flask, request, render_template, redirect, flash, make_response, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    return "Main page, nothing special..."

@app.route('/mail')
def mail():
    try:
        from connector import MailConnector
        login, password, imap_server, m_id = request.args.get('l'), request.args.get('p'), request.args.get('i'), request.args.get('mid')
        #return f'{login} {password} {imap_server}'
        mail = MailConnector(login, password, imap_server)
        if mail.connect() == True:
            mail_text = mail.get_mail_text(str(m_id), False)
            return mail_text
        else:
            return f'Неверный логин или пароль: {mail.connect()}'
    except Exception as e:
        return f'Произошла ошибка: {str(e)}'

app.run(debug=True, host='0.0.0.0', port='8080')
