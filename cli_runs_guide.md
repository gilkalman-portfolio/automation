# מדריך הרצות Pytest דרך CLI לפרויקט

## 1. הרצה בסיסית

```bash
pytest

pytest -vv              # פלט מפורט לכל טסט
pytest -m smoke         # רק טסטים עם @pytest.mark.smoke
pytest -m "regression"  # רק regression
pytest -m "sanity"      # רק sanity
pytest --env=staging
pytest --env=prod
pytest --base-url="https://example.com"

pytest -m smoke --env=staging --base-url="https://staging.example.com"


pytest --browsers=chromium
pytest --browsers=chromium,firefox,webkit
pytest --devices=desktop
pytest --devices="desktop,Pixel 5"
pytest --headless=true      # headless (דיפולטי ברוב המקרים)
pytest --headless=false     # לפתוח דפדפן נראה

pytest --workers=1      # ריצה סיריאלית
pytest --workers=4      # עד 4 וורקרים (אם יש תמיכה בזה בקונפיג)
pytest --retries=0      # בלי נסיונות חוזרים
pytest --retries=2      # עד 2 ריצות חוזרות לטסט כושל
pytest -m regression --workers=4 --retries=1


pytest --trace=off                # בלי trace
pytest --trace=on                 # תמיד trace
pytest --trace=retain-on-failure  # רק על כישלון (מומלץ)
pytest --video=off
pytest --video=on
pytest --video=retain-on-failure  # (אם תחליט להשתמש בפוליסי כזה)
pytest --screenshot=only-on-failure   # דיפולט נפוץ
pytest --screenshot=on                # תמיד לצלם
pytest --screenshot=off               # לא לצלם בכלל

pytest -m smoke \
  --trace=retain-on-failure \
  --video=off \
  --screenshot=only-on-failure


pytest -m smoke \
  --browsers=chromium \
  --devices=desktop \
  --headless=true \
  --trace=retain-on-failure

pytest -m sanity \
  --env=staging \
  --base-url="https://staging.example.com"
