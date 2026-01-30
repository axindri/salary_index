import json
from datetime import datetime
from logging import getLogger
import os

import requests
from fastapi import HTTPException

from src.config import settings
from src.constants import DOMCLICK_CITY_MAP, City

logger = getLogger(__name__)


def save_city_prices(city_prices: dict[City, int]) -> None:
    try:
        logger.debug("Saving city prices to file=%s", settings.data_file_path)
        meta = {
            "updated_at": datetime.now().isoformat(),
            "total_items": len(city_prices),
        }
        data = {
            "meta": meta,
            "data": city_prices,
        }
        with open(settings.data_file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error("Error saving city prices: %s", e)
        raise HTTPException(status_code=500, detail="Error saving city prices")


def load_city_prices() -> tuple[datetime, dict[City, int]] | tuple[None, None]:
    try:
        logger.debug("Loading city prices from file=%s", settings.data_file_path)
        if not os.path.exists(settings.data_file_path):
            return (None, None)
        with open(settings.data_file_path, "r") as f:
            data = json.load(f)
            return (data["meta"]["updated_at"], {City(key): value for key, value in data["data"].items()})
    except Exception as e:
        logger.error("Error loading city prices: %s", e)
        raise HTTPException(status_code=500, detail="Error loading city prices")


def get_district_city_names(city: City) -> tuple[str, str] | tuple[None, None]:
    for city_map in DOMCLICK_CITY_MAP:
        if city_map["city"] == city:
            return (city_map["district_name"], city_map["city_name"])
    return (None, None)


def sanitize_name(city: str) -> str:
    return city.replace("_", "-")


def get_city_sqm_price(district_name: str, city_name: str) -> int | None:
    url = f"{settings.domclick_api_url}/{sanitize_name(district_name)}"
    logger.debug("Getting city price for url=%s", url)
    params = {
        "period": "month",
        "metric": "flat_weighted_med_sq_price",
    }
    headers = {
        "User-Agent": settings.user_agent,
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    try:
        cities_data = data["data"]
        for city_data in cities_data:
            if city_data["slug"] == city_name:
                metric = city_data["metrics"][0]
                if metric["slug"] == "flat_weighted_med_sq_price":
                    price = int(metric["values"][0]["formatted"].replace(" ", "").replace("₽", ""))
                    logger.debug("Got city=%s price=%s", city_name, price)
                    return price
    except Exception as e:
        logger.error("Error getting city price for city=%s: %s", city_name, e)
    return None
