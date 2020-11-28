from typing import List, Dict

from pymongo import MongoClient


class DataClient:
    def __init__(
        self, uri: str, db: str, collection: str, pipeline: List[Dict]
    ) -> List[Dict]:
        self.uri = uri
        self.pipeline = pipeline

        self.client = MongoClient(self.uri)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def fetch(self) -> List[Dict]:
        return list(self.collection.aggregate(self.pipeline))
