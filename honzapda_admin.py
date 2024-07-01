from pymongo import MongoClient, IndexModel, ASCENDING
from datetime import datetime, timedelta, timezone

from decouple import config
from opencv import scanPeople

def insert_document(collection,shopId):
    count = scanPeople()
    expire_at = datetime.now(timezone.utc) + timedelta(seconds=20)
    result=collection.insert_one({'count': count, 'expire_at': expire_at, 'shopId': shopId})
    return result.inserted_id


def admin_main(shopId):   
  
    # MongoDB 연결
    client = MongoClient(config('MONGO_URI'))

    db = client[config('MONGO_DB')]  
    collection = db[config('MONGO_COLLECTION')]  

    index = IndexModel([("expire_at", ASCENDING)], expireAfterSeconds=0)
    collection.create_indexes([index])

    inserted_id=insert_document(collection,shopId)
    print(inserted_id)

    # Change Stream 생성
    with collection.watch() as stream:
        for change in stream:
            # 삭제된 문서의 _id를 출력하고, 데이터를 다시 삽입합니다.
            if change['operationType'] == 'delete' and change['documentKey']['_id'] == inserted_id:
                print(f"Document deleted: {inserted_id}")
                inserted_id=insert_document(collection,shopId)
                print(inserted_id)