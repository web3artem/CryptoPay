from pydantic import BaseModel


class CurrencySchema(BaseModel):
    blockchain: str
    ticker: str