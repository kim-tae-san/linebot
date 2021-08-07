import requests
import re

# https://jokergt.tistory.com/52
korean_re = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Naver-Client-Id': 'nFPKLdKwA0oF9MJSYH92',
    'X-Naver-Client-Secret': 'CPA7WxldGO',
}

def is_korean(text):
  return korean_re.search(text) is not None

def translate(text):
  if is_korean(text):
    return _translate(text, 'ko', 'ja')
  else:
    return _translate(text, 'ja', 'ko')

def _translate(text, source='ja', target='ko'):
  data = {'source': source, 'target':target, 'text':text}
  response = requests.post('https://openapi.naver.com/v1/papago/n2mt', headers=headers, data=data)
  json = response.json()

  return json['message']['result']['translatedText']