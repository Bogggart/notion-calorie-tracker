#!/usr/bin/env python3 
import os
from datetime import datetime
from notion_client import Client

# ініціалізація
notion = Client(auth=os.getenv("NOTION_TOKEN"))
daily_db_id = os.getenv("DAILY_SUM_ARCHIVE_DB")

def get_today_sums():
    return {
        "kcal": 2145,
        "prot": 132,
        "fat": 65,
        "carb": 285,
    }

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Processing {today}")
    sums = get_today_sums()
    print(f"📊 Daily sums: {sums}")

    # ВИПРАВЛЕНО: іменовані параметри замість dict
    results = notion.databases.query(
        database_id=daily_db_id,
        filter={
            "property": "Date",
            "rich_text": {"equals": today},
        }
    )

    if results["results"]:
        page_id = results["results"][0]["id"]
        notion.pages.update(
            page_id=page_id,
            properties={
                "Kcal daily": {"number": sums["kcal"]},
                "Prot daily": {"number": sums["prot"]},
                "Fat daily": {"number": sums["fat"]},
                "Carb daily": {"number": sums["carb"]},
            }
        )
        print("🔄 Updated existing record")
    else:
        notion.pages.create(
            parent={"database_id": daily_db_id},
            properties={
                "Date": {"rich_text": [{"text": {"content": today}}]},
                "Kcal daily": {"number": sums["kcal"]},
                "Prot daily": {"number": sums["prot"]},
                "Fat daily": {"number": sums["fat"]},
                "Carb daily": {"number": sums["carb"]},
            }
        )
        print("✅ Created new record")

    print("🎉 Done!")

if __name__ == "__main__":
    main()
