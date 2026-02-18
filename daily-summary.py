#!/usr/bin/env python3
import os
from datetime import datetime
from notion_client import Client

# Ініціалізація
notion = Client(auth=os.getenv("NOTION_TOKEN"))
progress_bar_id = os.getenv("PROGRESS_BAR_ID")
daily_log_db = os.getenv("DAILY_LOG_DB")
daily_archive_db = os.getenv("DAILY_SUM_ARCHIVE_DB")

def has_meals_today():
    """Перевірити чи є записи в Daily log за сьогодні"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        results = notion.databases.query(
            database_id=daily_log_db,
            filter={
                "property": "Date",
                "date": {"equals": today}
            }
        )
        return len(results.get("results", [])) > 0
    except Exception as e:
        print(f"⚠️ Error checking meals: {e}")
        return False

def get_today_sums():
    """Читати готові суми з Progress bar"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not has_meals_today():
        print("⚠️ No meals today, using zeros")
        return {"kcal": 0, "prot": 0, "fat": 0, "carb": 0}
    
    try:
        page = notion.pages.retrieve(page_id=progress_bar_id)
        props = page["properties"]
        
        sums = {
            "kcal": props.get("Kcal sum", {}).get("number", 0) or 0,
            "prot": props.get("Prot sum", {}).get("number", 0) or 0,
            "fat":  props.get("Fat sum", {}).get("number", 0) or 0,
            "carb": props.get("Carb sum", {}).get("number", 0) or 0,
        }
        
        print(f"📊 Progress bar sums: {sums}")
        return sums
    except Exception as e:
        print(f"⚠️ Error reading Progress bar: {e}")
        return {"kcal": 0, "prot": 0, "fat": 0, "carb": 0}

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Processing {today}")
    
    sums = get_today_sums()
    
    # ✅ ЗМІНА: Date як DATE property, а не text/title
    results = notion.databases.query(
        database_id=daily_archive_db,
        filter={
            "property": "Date",
            "date": {"equals": today}  # ← Date filter
        }
    )
    
    if results["results"]:
        page_id = results["results"][0]["id"]
        notion.pages.update(
            page_id=page_id,
            properties={
                "Kcal daily": {"number": round(sums["kcal"])},
                "Prot daily": {"number": round(sums["prot"])},
                "Fat daily": {"number": round(sums["fat"])},
                "Carb daily": {"number": round(sums["carb"])}
            }
        )
        print("🔄 Updated Daily sum archive")
    else:
        notion.pages.create(
            parent={"database_id": daily_archive_db},
            properties={
                # ✅ ЗМІНА: Date як DATE, а не rich_text/title
                "Date": {"date": {"start": today}},
                "Kcal daily": {"number": round(sums["kcal"])},
                "Prot daily": {"number": round(sums["prot"])},
                "Fat daily": {"number": round(sums["fat"])},
                "Carb daily": {"number": round(sums["carb"])}
            }
        )
        print("✅ Created Daily sum archive record")
    
    print("🎉 Complete!")

if __name__ == "__main__":
    main()
