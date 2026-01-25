from dataclasses import dataclass
from datetime import datetime
from logging import getLogger

from fastapi import HTTPException

from src.constants import COOL_GROUPS, City
from src.schemas import Meta, SalaryIndexByCity, SalaryIndexResponse
from src.utils import get_city_sqm_price, get_district_city_names, load_city_prices, save_city_prices

logger = getLogger(__name__)


@dataclass
class PriceParser:
    def save_cities_sqm_price(self) -> None:
        city_prices: dict[City, int] = {}
        for city in City:
            district_name, city_name = get_district_city_names(city)
            if district_name is None or city_name is None:
                continue
            price = get_city_sqm_price(district_name, city_name)
            if price is not None:
                city_prices[city] = price
        save_city_prices(city_prices)


@dataclass
class SalaryIndex:
    actual_at: datetime
    city_prices: dict[City, int]

    @staticmethod
    def _get_cool_group(cool_index: float) -> str:
        max_threshold = max(COOL_GROUPS.keys())
        for threshold, group in COOL_GROUPS.items():
            if cool_index <= threshold:
                return group
            elif cool_index > max_threshold:
                return COOL_GROUPS[max_threshold]
        return "unknown"

    def calculate_city(self, city: City, net_salary: int) -> SalaryIndexByCity | None:
        price_per_sqm = self.city_prices.get(city)
        if price_per_sqm is None:
            return None

        cool_index = net_salary / price_per_sqm
        months_per_sqm = price_per_sqm / net_salary

        return SalaryIndexByCity(
            city=city,
            net_salary=net_salary,
            price_per_sqm=price_per_sqm,
            cool_index=round(cool_index, 4),
            cool_group=self._get_cool_group(cool_index),
            months_per_sqm=round(months_per_sqm, 4),
        )

    def calculate_other_cities(self, main_city: City, salary: int) -> list[SalaryIndexByCity]:
        other_indexes = []
        for check_city in self.city_prices.keys():
            if check_city == main_city:
                continue
            other_index = self.calculate_city(check_city, salary)
            if other_index is not None:
                other_indexes.append(other_index)
        return other_indexes

    def calculate(self, city: City, salary: int) -> SalaryIndexResponse:
        logger.debug("Calculating salary index for main city=%s and salary=%s", city, salary)
        main_index = self.calculate_city(city, salary)
        if main_index is None:
            raise HTTPException(status_code=400, detail=f"no price configured for city={city}")

        other_indexes = self.calculate_other_cities(city, salary)
        other_indexes.sort(key=lambda x: x.cool_index, reverse=True)

        return SalaryIndexResponse(
            meta=Meta(actual_at=self.actual_at, total_items=len(self.city_prices)), main=main_index, other=other_indexes
        )


async def get_salary_index_dependecy() -> SalaryIndex:
    actual_at, city_prices = load_city_prices()
    return SalaryIndex(city_prices=city_prices, actual_at=actual_at)


async def get_price_parser_dependecy() -> PriceParser:
    return PriceParser()
