from flask import Flask, render_template, request
from chatterbot import ChatBot, filters, logic
import warnings
warnings.filterwarnings('ignore')
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from test.files.Team import team_selection
import re
from test.files.Market import market_demand_function
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'teampheonix854@gmail.com',
    "MAIL_PASSWORD": 'password123@',
}

app.config.update(mail_settings)
mail = Mail(app)

bot = ChatBot(
    'Archie',
    
    logic_adapters=[

        
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.60,
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'What is time table for today',
            'output_text': 'this is the time table',
            
        },
       
        
    ],
    )



conversation = open('test/chats.txt', 'r').readlines()
conversation2 = open('test/birthdays.txt', 'r').readlines()


trainer = ListTrainer(bot)
trainer.train(conversation)
trainer.train(conversation2)


trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    n = userText.split(" ")
    if 'shana' in n or 'shambhavi' in n or 'shreya' in n or 'jyoti' in n:
        response = team_selection(n)
        return str(response) 
    
    elif 'bosch' in n:
        company = 'bosch'
        demand = int(re.search(r'\d+', userText).group())
        response = market_demand_function(demand, company)
        return str(response)
    elif 'employee' in n and 'code' in n:
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["jyoti.rani3020@gmail.com"], # replace with your email for testing
                      body="This is a test email sent by Archie - AI powered chatbot. Your OTP is: 7788")
        mail.send(msg)
        response = 'Please Enter OTP!'
        return str(response)

    
    return str(bot.get_response(userText))
    


if __name__ == "__main__":
    app.run(debug=True)