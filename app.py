from flask import Flask, render_template, request, jsonify
import json
from geopy.geocoders import Nominatim # 가까운 병원 위경도 값으로 찾기
from haversine import haversine

def get_lat_and_log(address):
    '''
    주소 입력 시 위경도 값 출력하는 함수

    https://wonhwa.tistory.com/29
    :param address: 주소값
    :return: 위도값, 경도값
    '''
    try:
        geo_local = Nominatim(user_agent='South Korea')

        while(not geo_local.geocode(address)):
            # 마지막 어절 하나씩 제거
            address = address[:-len(address.split(' ')[-1])-1]
        geo=geo_local.geocode(address)

        return geo.latitude, geo.longitude # 위도, 경도 순으로 반환
    except:
        print(address,'에러!!!')
        return (0.0,0.0)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

'''
1. 외부에서 로컬 pc로 접속하기
ngrok 실행 (ngrok 외부에서 로컬로 접속 가능하게 해주는 기능)
ngrok.exe http 5001 입력
포워딩 주소 나옴 예시)  https://97d2-112-221-224-124.jp.ngrok.io -> http://localhost:5001

2. DialogFlow에서 Webhook에 url등록하기
DialogFlow > Fulfillment > Webhook > https://97d2-112-221-224-124.jp.ngrok.io/chatbot 입력

3. Intent들 Fulfilment > Enable webhook call for this intent 해주기
'''
@app.route('/chatbot',methods=('POST',"GET"))
def chatbot():
    # 사용자 두피 상태 진단 예측 결과
    scalp_type_result = '양호' # 진단결과 붙일때 마지막 func()[-1]

    # 사용자가 챗봇에 입력 시 데이터 받기
    req = request.get_json(force=True)
    # print(req)  # intent의 display name으로 구분해서 대응하기
    # print("쿼리텍스트 > "+req['queryResult']['queryText'])
    # print("인텐트 이름:"+req['queryResult']['intent']['displayName']) # Default Fallback Intent

    if (req['queryResult']['intent']['displayName'] == "Default Welcome Intent"):
        print("접속 인텐트: Default Welcome Intent")
        return jsonify(fulfillment_messages=[
            {
                "payload":{
                  "richContent": [
                    [
                      {
                        "rawUrl": "https://t1.daumcdn.net/cfile/tistory/99559F435DEEDFCB1D",
                        "type": "image",
                        "accessibilityText": "두피 진단 예측 welcome"
                      },
                      {
                        "title": "두피 진단 예측 서비스",
                        "type": "info",
                        "subtitle": "당신의 두피를 최고의 AI 기술을 이용해 진단해드립니다."
                      },
                      {
                        "options": [
                          {
                            "text": "진단결과 확인하기",
                            "image": {
                              "src": {
                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                              }
                            }
                          }
                        ],
                        "type": "chips"
                      }
                    ]
                  ]
                }
            }
        ])

    if (req['queryResult']['intent']['displayName'] == "Default Fallback Intent"):
        print("접속 인텐트: Default Fallback Intent")
        return jsonify(fulfillment_messages=[
            {
                "payload":{
                  "richContent": [
                    [
                      {
                        "rawUrl": "https://www.sciencetimes.co.kr/wp-content/uploads/2020/10/GettyImages-1222023758-scaled.jpg",
                        "type": "image",
                        "accessibilityText": "두피 진단 예측"
                      },
                      {
                        "subtitle": "예측된 두피 진단 결과로 다음과 같은 서비스를 이용해보세요",
                        "title": "당신의 두피 상태는 '"+ scalp_type_result +"'입니다.",
                        "type": "info"
                      },
                      {
                        "type": "chips",
                        "options": [
                          {
                            "image": {
                              "src": {
                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                              }
                            },
                            "text": "제품 추천 무료로 받기"
                          },
                          {
                            "image": {
                              "src": {
                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                              }
                            },
                            "text": "가까운 병원 무료로 찾기"
                          },
                          {
                            "link": "https://c3be-112-221-224-124.jp.ngrok.io/",
                            "text": "두피 진단 다시 해보기",
                            "image": {
                              "src": {
                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                              }
                            }
                          }
                        ]
                      }
                    ]
                  ]
                }
            }
        ])


    # 제품 추천
    # intent Recomend_Products 확인
    if(req['queryResult']['intent']['displayName']=="Recomend_Products"):
        print("접속 인텐트: Recomend_Products")
        with open('./products.json', 'r', encoding="UTF-8") as file:
            products = json.load(file)
            # print('제품 정보:', products)
            return jsonify(fulfillment_messages=[
                {
                    "payload": {
                      "richContent": [
                        [
                          {
                            "type": "description",
                            "title": "브랜드평판지수"
                          },
                          {
                            "subtitle": products['scalp_type'][scalp_type_result]['브랜드평판지수'][0]['line'],
                            "image": {
                              "src": {
                                "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['브랜드평판지수'][0]['image']
                              }
                            },
                            "type": "info",
                            "title": products['scalp_type'][scalp_type_result]['브랜드평판지수'][0]['product_name']
                          },
                          {
                            "subtitle": products['scalp_type'][scalp_type_result]['브랜드평판지수'][1]['line'],
                            "image": {
                              "src": {
                                "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['브랜드평판지수'][1]['image']
                              }
                            },
                            "type": "info",
                            "title": products['scalp_type'][scalp_type_result]['브랜드평판지수'][1]['product_name']
                          },
                          {
                            "subtitle": products['scalp_type'][scalp_type_result]['브랜드평판지수'][2]['line'],
                            "type": "info",
                            "title": products['scalp_type'][scalp_type_result]['브랜드평판지수'][2]['product_name'],
                            "image": {
                              "src": {
                                "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['브랜드평판지수'][2]['image']
                              }
                            }
                          }
                        ],
                        [
                          {
                              "type": "description",
                              "title": "의사 추천"
                          },
                          {
                              "image": {
                                  "src": {
                                      "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['의사추천'][0]['image']
                                  }
                              },
                              "title": products['scalp_type'][scalp_type_result]['의사추천'][0]['product_name'],
                              "type": "info",
                              "subtitle": products['scalp_type'][scalp_type_result]['의사추천'][0]['line']
                          },
                          {
                              "subtitle": products['scalp_type'][scalp_type_result]['의사추천'][1]['line'],
                              "image": {
                                  "src": {
                                      "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['의사추천'][1]['image']
                                  }
                              },
                              "title": products['scalp_type'][scalp_type_result]['의사추천'][0]['product_name'],
                              "type": "info"
                          },
                          {
                              "type": "info",
                              "image": {
                                  "src": {
                                      "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['의사추천'][2]['image']
                                  }
                              },
                              "title": products['scalp_type'][scalp_type_result]['의사추천'][2]['product_name'],
                              "subtitle": products['scalp_type'][scalp_type_result]['의사추천'][2]['line']
                          }
                        ],
                        [
                            {
                                "type": "description",
                                "title": "화해 랭킹순"
                            },
                            {
                                "type": "info",
                                "image": {
                                    "src": {
                                        "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['화해 랭킹순'][0]['image']
                                    }
                                },
                                "subtitle": products['scalp_type'][scalp_type_result]['화해 랭킹순'][0]['line'],
                                "title": products['scalp_type'][scalp_type_result]['화해 랭킹순'][0]['product_name']
                            },
                            {
                                "image": {
                                    "src": {
                                        "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['화해 랭킹순'][1]['image']
                                    }
                                },
                                "type": "info",
                                "subtitle": products['scalp_type'][scalp_type_result]['화해 랭킹순'][1]['line'],
                                "title": products['scalp_type'][scalp_type_result]['화해 랭킹순'][1]['product_name']
                            },
                            {
                                "type": "info",
                                "image": {
                                    "src": {
                                        "rawUrl": './static/images/products/'+products['scalp_type'][scalp_type_result]['화해 랭킹순'][2]['image']
                                    }
                                },
                                "title": products['scalp_type'][scalp_type_result]['화해 랭킹순'][2]['product_name'],
                                "subtitle": products['scalp_type'][scalp_type_result]['화해 랭킹순'][2]['line'],
                            }
                        ],
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                                            }
                                        },
                                        "text": "가까운 병원 무료로 찾기"
                                    },
                                    {
                                        "link": "https://c3be-112-221-224-124.jp.ngrok.io/",
                                        "text": "두피 진단 다시 해보기",
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                      ]
                    }
                }
            ])


    # 병원 추천
    # intent Recomend_Hospitals 확인
    if(req['queryResult']['intent']['displayName']=="Recomend_Hospitals"):
        print("접속 인텐트: Recomend_Hospitals")
        return jsonify(fulfillment_messages=[
            {
                "payload":{
                  "richContent": [
                    [
                      {
                        "type": "description",
                        "title": "현재 주소를 입력해 주세요.",
                        "text": [
                          "입력하신 주소와 가장 가까운 두피, 모발 전문병원을 추천해드립니다.",
                            "입력받은 주소의 위경도 값을 계산하여 가장 가까운 병원을 소개해드립니다."
                        ]
                      }
                    ]
                  ]
                }
            }
        ])

    # 병원 추천 > 주소 입력받고 > db에 저장된 병원 위경도값 비교해서 최단거리 병원 출력
    if (req['queryResult']['intent']['displayName'] == "Closest_Hospitals"):
        print("접속 인텐트: Closest_Hospitals")

        # 현재 위치 위경도값 계산
        current_position = get_lat_and_log(req['queryResult']['queryText'])
        # print(current_position)

        # 병원 json파일 열기
        with open('./hospitals.json', 'r', encoding="UTF-8") as file:
            hospitals = json.load(file)
            # print('병원 정보:',hospitals)
            # print('병원 위경도:',type(list(hospitals.keys())))
            # print('병원 개수:',len(hospitals.keys()))

            tmp_dic={} # 딕셔너리 키(병원 위경도):값(거리)
            for i, hospital_lat_lon in enumerate(hospitals):
                # print(hospital_lat_lon) # hospitals의 키
                # print(tuple(list(map(float, hospital_lat_lon.split(',')))))
                # print(tuple(hospital_lat_lon))
                # print(type(hospital_lat_lon))
                # print("거리:",haversine(current_position,tuple(list(map(float, hospital_lat_lon.split(','))))))

                # 딕셔너리 저장 키(병원 위경도):값(거리)
                tmp_dic[hospital_lat_lon]=haversine(current_position,tuple(list(map(float, hospital_lat_lon.split(',')))))

            # 오름차순 정렬, 최단거리 순으로 정렬
            tmp_dic=dict(sorted(tmp_dic.items(), key=lambda x: x[1]))
            # print(tmp_dic)

            # # 최단거리 3개만 출력
            # for i in range(0,3):
            #     print(list(tmp_dic.keys())[i])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원명'])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원 주소'])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원 홈페이지'])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원 전화번호'])

            return jsonify(fulfillment_messages=[
                {
                    "payload":{
                      "richContent": [
                        [
                          {
                            "type": "info",
                            "title": hospitals[list(tmp_dic.keys())[0]]['병원명'],
                            "subtitle": hospitals[list(tmp_dic.keys())[0]]['병원 전화번호'] + '/' + hospitals[list(tmp_dic.keys())[0]]['병원 주소'],
                            "actionLink": hospitals[list(tmp_dic.keys())[0]]['병원 홈페이지']
                          }
                        ],
                        [
                          {
                            "type": "info",
                            "title": hospitals[list(tmp_dic.keys())[1]]['병원명'],
                            "subtitle": hospitals[list(tmp_dic.keys())[1]]['병원 전화번호'] + '/' + hospitals[list(tmp_dic.keys())[1]]['병원 주소'],
                            "actionLink": hospitals[list(tmp_dic.keys())[1]]['병원 홈페이지']
                          }
                        ],
                        [
                          {
                            "type": "info",
                            "title": hospitals[list(tmp_dic.keys())[2]]['병원명'],
                            "subtitle": hospitals[list(tmp_dic.keys())[2]]['병원 전화번호'] + '/' + hospitals[list(tmp_dic.keys())[2]]['병원 주소'],
                            "actionLink": hospitals[list(tmp_dic.keys())[2]]['병원 홈페이지']
                          }
                        ],
                        [
                              {
                                "type": "chips",
                                "options": [
                                    {
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                                            }
                                        },
                                        "text": "제품 추천 무료로 받기"
                                    },
                                    {
                                        "link": "https://c3be-112-221-224-124.jp.ngrok.io/",
                                        "text": "두피 진단 다시 해보기",
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://cdn-icons.flaticon.com/png/512/3430/premium/3430162.png?token=exp=1659073150~hmac=ad38f9e6c105d507f5e194f82ca7dd69"
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                      ]
                    }
                }

            ])



if __name__=='__main__':
    app.run('0.0.0.0',port=5001, debug=True)




'''
https://dialogflow.cloud.google.com/
https://cloud.google.com/dialogflow#section-5
# 응답 메세지로 버튼, 이미지 등
https://cloud.google.com/dialogflow/es/docs/intents-rich-messages?hl=ko#where
https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger#df-request-sent
'''