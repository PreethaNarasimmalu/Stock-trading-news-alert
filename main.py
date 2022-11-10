import html

from twilio.rest import Client
import requests
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

price_increase = False
price_decrease = False

twilio_account_sid = ACCOUNT_SID
twilio_auth_token = AUTH_TOKEN

news_api_key = NEWS_API_KEY
alpha_api_key = API_KEY

news_end_point = "https://newsapi.org/v2/everything"
price_end_point = "https://www.alphavantage.co/query"

price_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alpha_api_key
}

news_parameters = {
    'q': COMPANY_NAME,
    # "qInTitle": COMPANY_NAME,
    "apikey": news_api_key
}

price_response = requests.get(url=price_end_point, params=price_parameters)
price_response.raise_for_status()
price_data = price_response.json()

today_date = datetime.strftime((datetime.now() - timedelta(1)).date(), "%Y-%m-%d")
yesterday_date = datetime.strftime((datetime.now() - timedelta(2)).date(), "%Y-%m-%d")
print(price_data)
today_data = float(price_data["Time Series (Daily)"][today_date]["4. close"])
yesterday_data = float(price_data["Time Series (Daily)"][yesterday_date]["4. close"])

price_difference = round(abs(((yesterday_data - today_data) / today_data) * 100), 2)

if today_data > yesterday_data :
    price_increase = True
elif yesterday_data > today_data:
    price_decrease = True

if price_difference >= 4:
    print("Get News")
    news_response = requests.get(url=news_end_point, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    news = {}
    for count in range(3):
        news[f"news_{count+1}"] = {"title": news_data["articles"][count]["title"], "description": news_data["articles"][0]["description"]}
    message_str=[]
    if price_increase == True:
        for key,value in news.items():
            message_str.append(f"{STOCK}: 🔺{price_difference}%\nHeadline: {value['title']}\nBrief: {value['description']}")
    elif price_decrease == True:
        for key,value in news.items():
            message_str.append(f"{STOCK}: 🔻{price_difference}%\nHeadline: {value['title']}\nBrief: {value['description']}")

    client = Client(twilio_account_sid, twilio_auth_token)
    for msg in message_str:
        print(msg)
        message = client.messages.create(
            body=msg,
            from_= FROM_NUM,  
            to=TO_NUM
        )
        print(message.status)
