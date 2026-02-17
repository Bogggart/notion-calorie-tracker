import os
import requests
from notion_client import Client
from datetime import datetime, timedelta
import json

notion = Client(auth=os.getenv("NOTION_TOKEN"))

def get_datastore_sums(date_key):
    """Тут твоя логіка Data Store — спочатку mock"""
    return {
        "kcal": 2145,
        "prot": 132,
        "fat": 65,
        "carb": 285
    }

def create_daily_archive(date_str, sums):
    daily_db = os.getenv("DAILY_ARCHIVE_DB")
    
    # Check if exists
    results = notion.databases.query(
        database_id=daily_db,
        filter={"property": "Date", "date": {"equals": date_str}}
    )
    
    if results["results"]:
        page_id = results["results"][0]["id"]
        notion.pages.update(page_id, properties={
            "Kcal": {"number": sums["kcal"]},
            "Prot": {"number": sums["prot"]},
            "Fat": {"number": sums["fat"]},
            "Carb": {"number": sums["carb"]}
        })
    else:
        notion.pages.create(
            parent={"database_id": daily_db},
            properties={
                "Date": {"date": {"start": date_str}},
                "Kcal": {"number": sums["kcal"]},
                "Prot": {"number": sums["prot"]},
                "Fat": {"number": sums["fat"]},
                "Carb": {"number": sums["carb"]}
            }
        )

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    sums = get_datastore_sums(today)
    create_daily_archive(today, sums)
    print(f"✅ Daily Archive updated for {today}")
