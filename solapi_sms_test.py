import json
import logging
import sys
import os
from solapi import SolapiMessageService
from solapi.model.message import Message

# 환경 변수 또는 secrets로 관리하는 것이 안전합니다.
API_KEY = os.environ.get('SOLAPI_API_KEY')
API_SECRET = os.environ.get('SOLAPI_API_SECRET')
if not API_KEY or not API_SECRET:
      raise Exception("SOLAPI API KEY/SECRET 환경변수가 설정되어 있지 않습니다.")

print(f"API_KEY is None? {API_KEY is None}")
print(f"API_SECRET is None? {API_SECRET is None}")

def send_bulk_sms(json_path):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    service = SolapiMessageService(API_KEY, API_SECRET)

    # JSON 파일 읽기
    with open(json_path, encoding='utf-8') as f:
        sms_list = json.load(f)

    messages = []
    for sms in sms_list:
        try:
            msg = Message(from_=sms['from'], to=sms['to'], text=sms['text'])
            messages.append(msg)
        except Exception as e:
            logging.error(f"메시지 생성 오류: {e} (데이터: {sms})")

    if not messages:
        logging.warning("전송할 메시지가 없습니다.")
        return

    try:
        logging.info(f"{len(messages)}건 문자 일괄 발송 시작")
        response = service.send(messages)
        logging.info(f"문자 일괄 발송 완료. 응답: {response}")
    except Exception as e:
        logging.error(f"문자 발송 중 오류 발생: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python sms_sender.py [json파일경로]")
        sys.exit(1)
    send_bulk_sms(sys.argv[1]) 
