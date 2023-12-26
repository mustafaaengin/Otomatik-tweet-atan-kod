import json
from requests import get
from datetime import datetime
from requests_oauthlib import OAuth1Session
import time

# Twitter API kimlik bilgileri
consumer_key = "GKdYI3JXtkzVFzgaJVPz2j0NI"
consumer_secret = "cqtjPitx0AYL7RX9A6cpbkcjf6qKFdXHQqQoFcTkCQHGB5wPdV"

# GitHub'dan veri çekme ve karşılaştırma fonksiyonu
def veri_cek_ve_karsilastir(github_url):
    try:
        response = get(github_url)
        if response.status_code == 200:
            veri = response.json()  # GitHub'dan veriyi al

            bugun = datetime.now().strftime("%Y-%m-%d %H")  # Şu anki tarih ve saat

            for line in veri:
                file_info = line["Tarih"]  # Dosyadan çekilen tarih ve saat
                if file_info == bugun:
                    tweet_verisi = line["Tweet"]  # Tweet içeriğini al
                    return tweet_verisi  # Eşleşme durumunda tweet içeriğini geri döndür

        else:
            print("Hata: İstek başarısız oldu. Status code:", response.status_code)

    except Exception as e:
        print("Hata:", str(e))

    return None  # Eşleşme yoksa veya bir hata oluşursa None döndür

# Twitter API yetkilendirme işlemleri
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
    github_url = "https://raw.githubusercontent.com/mustafaaengin/Otomatik-tweet-atan-kod/main/tweet_verisi.json"  # GitHub raw dosya URL'si
    
    # GitHub'dan tweet içeriğini çek
    tweet_icerigi = veri_cek_ve_karsilastir(github_url)

    if tweet_icerigi:
        print("Karşılanan Tweet İçeriği:", tweet_icerigi)
        
        # Tweet atma işlemi
        payload = {"text": tweet_icerigi}  # v2 API'si için text anahtarını kullanıyoruz
        response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

        if response.status_code != 201:
            raise Exception(f"Error: {response.status_code} {response.text}")

        print(f"Tweet atıldı: {response.status_code}")
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
    else:
        print("Eşleşme Yok veya Hata Oluştu.")

    time.sleep(60)  # Her bir dakika sonra tekrar döngüyü başlat
