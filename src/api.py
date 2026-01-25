from logging import getLogger

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from src.config import settings
from src.constants import City
from src.schemas import SalaryIndexResponse
from src.service import PriceParser, SalaryIndex, get_price_parser_dependecy, get_salary_index_dependecy

logger = getLogger(__name__)

router = APIRouter(prefix="/api")


@router.post("/parse-price")
async def parse_price(
    auth: str = Header(..., description="Authorization"),
    parser: PriceParser = Depends(get_price_parser_dependecy),
) -> dict[str, str]:
    if auth != settings.secret_key:
        raise HTTPException(status_code=401, detail="Invalid token")
    parser.save_cities_sqm_price()
    return {"message": "Success"}


@router.get("/cities")
async def get_cities() -> list[City]:
    return list(City)


@router.get("/calculate")
async def get_salary_index(
    city: City = Query(..., description="City for calculation"),
    salary: int = Query(..., ge=1, le=100_000_000, description="Salary in RUB (net)"),
    salary_index: SalaryIndex = Depends(get_salary_index_dependecy),
) -> SalaryIndexResponse:
    return salary_index.calculate(city, salary)
