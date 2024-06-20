from fastapi import Depends, APIRouter, HTTPException
from connection import *
from models import BaseLoggedRequest, LoggedRequest
import datetime
from sqlalchemy import select, exc, insert, delete, update, extract, and_, or_
from pydantic import ValidationError
import json
from os import environ as env

import jwt
import httpx


SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]


async def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def decode_token(token):
    # simple token decoder
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(f"Token decode successfull {payload}")
        return payload
    except Exception as e:
        print(f"Error occured in token: {e}")
        return None


router = APIRouter()


@router.post("/trigger_calculate")
async def trigger_calculate(
        token: str,
        request_model: BaseLoggedRequest,
        session=Depends(get_session)):
    if await decode_token(token):
        # request to calculator
        n = request_model.n
        x0 = request_model.x
        rank = request_model.rank
        uuid = request_model.uuid
        data = json.dumps({"x0": x0, "n": n, "rank": rank})
        r = httpx.post(
            "http://truthteller_entrytest_taylor_calc_1:8000/calculate",
            data=data
        )
        # check for price modifier, set price modifier
        current_month = datetime.datetime.now().date().month
        current_year = datetime.datetime.now().date().year
        cmd = select(LoggedRequest).where(
            LoggedRequest.uuid == uuid,
            extract('month', LoggedRequest.date) == current_month,
            extract('year', LoggedRequest.date) == current_year)
        count = len(session.scalars(cmd).all())
        if count > 100:
            power = count // 100
            price = 10 * (1 + 2 ** power / 10)
        else:
            price = 10
        # set data, validate data, save data
        try:
            log = LoggedRequest.model_validate(request_model)
            log.price = price
            log.result = r.json()["message"]
            session.add(log)
            session.commit()
            session.refresh(log)
        except ValidationError as e:
            return HTTPException(status_code=400, detail="Broken data")
        return {"message": log}
    else:
        return HTTPException(status_code=403, detail="Forbidden")


@router.post("/get_data")
async def get_data(
        token: str,
        uuid: str,
        start: datetime.date = datetime.date.today(),
        end: datetime.date = datetime.date.today(),
        session=Depends(get_session)):
    """
        end-point for gathering all the request by uuid and
        date range
    """
    if await decode_token(token):
        cmd = select(LoggedRequest).where(
            LoggedRequest.uuid == uuid,
            and_(LoggedRequest.date < end,
                LoggedRequest.date > start))
        data = session.scalars(cmd).all()
        return data
    else:
        return HTTPException(status_code=403, detail="Forbidden")


@router.get("/get_token")
async def get_token():
    """
        simple token generator, 'sub' field could be used
        for role management in future
    """
    access_token = await create_access_token(
        {
            "sub": "tech",
            "iat": datetime.datetime.now(datetime.UTC),
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
        }
    )
    return {"access_token": access_token}
