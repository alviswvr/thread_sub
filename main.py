import random

from fastapi import FastAPI, Query

app = FastAPI()

# --- Configuration ---
TOTAL_ELEMENTS = 8407605
PAGE_SIZE = 50
COUNTRIES = ["US", "UK", "DE", "JP", "BR", "IN", "FR", "KR", "AU", "CA"]
CHINA_WEIGHT = 0.25
MAC_REAL_WEIGHT = 0.40
DEVICE_TYPES = ["PHONE", "TABLET", "TV", "WATCH"]
LAPTOP_WEIGHT = 0.40
FSC_MATCH_RANGE = (0, 10)


def rand_mac():
    return ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))


def make_item(_):
    country = "CHINA" if random.random() < CHINA_WEIGHT else random.choice(COUNTRIES)
    mac = rand_mac() if random.random() < MAC_REAL_WEIGHT else "NULL_CRA"
    device_type = "LAPTOP" if random.random() < LAPTOP_WEIGHT else random.choice(DEVICE_TYPES)
    fsc = random.randint(*FSC_MATCH_RANGE)
    return {
        "country": country,
        "mac": mac,
        "deviceType": device_type,
        "fscMatchBktI": fsc,
    }

ITEM_TEMPLATE = make_item
# ---------------------


@app.get("/items")
def get_items(page: int = Query(0, ge=0), size: int = Query(PAGE_SIZE, ge=1)):
    total = TOTAL_ELEMENTS
    total_pages = -(-total // size)
    count = min(size, total - page * size) if page * size < total else 0
    content = [ITEM_TEMPLATE(i) for i in range(count)]

    return {
        "content": content,
        "pageable": {
            "pageNumber": page,
            "pageSize": size,
            "sort": {"empty": True, "sorted": False, "unsorted": True},
            "offset": page * size,
            "paged": True,
            "unpaged": False,
        },
        "last": page >= total_pages - 1,
        "totalPages": total_pages,
        "totalElements": total,
        "first": page == 0,
        "size": size,
        "number": page,
        "sort": {"empty": True, "sorted": False, "unsorted": True},
        "numberOfElements": count,
        "empty": count == 0,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
