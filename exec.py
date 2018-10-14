from datetime import datetime, timezone, timedelta

# updateAt = datetime(2018, 10, 13, 12, 30, 0, 0, timezone.utc)  # datetime.now()
updateAt = datetime.now(timezone.utc)
past3days = datetime.now(timezone.utc) - timedelta(days=3)

print(past3days > updateAt)


# where(past)

