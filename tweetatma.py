from requests_oauthlib import OAuth1Session
from datetime import datetime
import time
import json

consumer_key = "kendi keyini gir"
consumer_secret = "kendi secret keyini gir"

oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print("There may have been an issue with the consumer_key or consumer_secret you entered.")

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")

authorization_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
print(f"Please go here and authorize: {authorization_url}")
verifier = input("Paste the PIN here: ")

access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

while True:
    bugun = datetime.now().strftime("%Y-%m-%d %H")  

    with open('.json dosyanın ismi', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    print("Güncel Saat:", bugun)

    found = False
    for line in lines:
        file_info = line.split("Tarih: ")[1].split(" Tweet")[0].strip()  
        print("Dosyadan Çekilen Tarih ve Saat:", file_info)
        if file_info == bugun:
            tweet_verisi = line.split("Tweet: ")[1].strip()  
            print("Eşleşen Tweet:", tweet_verisi)
            found = True
            break

    if found:
        payload = {"text": tweet_verisi} 
        response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

        if response.status_code != 201:
            raise Exception(f"Error: {response.status_code} {response.text}")

        print(f"Tweet atıldı: {response.status_code}")
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
    else:
        print("Eşleşme Yok")

    time.sleep(60)



        # bu kod bilgisayarınızda bulunan bir dosyadan veri çeker ve bu veriyi tweet olarak atar. dosyanızdaki verinin nasıl olması gerektiği json dosyasında gösterilmektedir
