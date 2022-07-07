from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot',methods=('POST',"GET"))
def chatbot():
    req=request.get_json(force=True)
    print(req) # intent의 display name으로 구분해서 대응하기
    print("req > "+req['queryResult']['queryText'])
    print('intent > ',req['queryResult']['intent']['name'])
    if(req['queryResult']['queryText']=='주문'):
        print('오답입니다.')
    #return jsonify(fulfillmentText = '챗봇 접속 성공')
    return jsonify(fulfillment_messages = [
        {
            "payload":{
                "richContent":[
                    [
                        {
                            "type": "button",
                            "icon": {
                                "type": "chevron_right",
                                "color": "#FF9800"
                            },
                            "text": "Button text",
                            "link": "https://google.com",
                            "event": {
                                "name": "",
                                "languageCode": "",
                                "parameters": {}
                            }
                        }


                    ]
                ]
            }
        }
    ])

if __name__=='__main__':
    app.run('0.0.0.0',port=5001, debug=True)