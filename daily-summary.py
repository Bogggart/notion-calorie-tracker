#!/usr/bin/env python3
import os
from datetime import datetime
from notion_client import Client

# Ініціалізація Notion
notion = Client(auth=os.getenv("NOTION_TOKEN"))
daily_db_id = os.getenv("DAILY_SUM_ARCHIVE_DB")  # Твоя нова назва

def get_today_sums():
    """Mock Data Store - замінимо на реальний API"""
    return {
        "kcal": 2145,
        "prot": 132,
        "fat": 65,
        "carb": 285
    }

def main():
    # Сьогодні (text формат для твоєї БД)
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Processing {today}")
    
    sums = get_today_sums()
    print(f"📊 Daily sums: Kcal={sums['kcal']}, Prot={sums['prot']}, Fat={sums['fat']}, Carb={sums['carb']}")
    
    # Шукаємо існуючий запис
    results = notion.databases.query(
        database_id=daily_db_id,
        filter={
            "property": "Date",
            "rich_text": {"equals": today}  # text property
        }
    )
    
    if results["results"]:
        # Оновлюємо існуючий
        page_id = results["results"][0]["id"].replace("-", "")
        notion.pages.update(
            page_id,
            properties={
                "Kcal daily": {"number": sums["kcal"]},
                "Prot daily": {"number": sums["prot"]},
                "Fat daily": {"number": sums["fat"]},
                "Carb daily": {"number": sums["carb"]}
            }
        )
        print("🔄 Updated existing Daily sum archive")
    else:
        # Створюємо новий
        notion.pages.create(
            parent={"database_id": daily_db_id},
            properties={
                "Date": {"rich_text": [{"text": {"content": today}}]},
                "Kcal daily": {"number": sums["kcal"]},
                "Prot daily": {"number": sums["prot"]},
                "Fat daily": {"number": sums["fat"]},
                "Carb daily": {"number": sums["carb"]}
            }
        )
        print("✅ Created new Daily sum archive record")
    
    print("🎉 Daily summary complete!")

if __name__ == "__main__":
    main()
