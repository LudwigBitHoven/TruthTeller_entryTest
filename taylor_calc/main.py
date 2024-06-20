from fastapi import FastAPI, Request
import uvicorn
import sympy as sp
import json


app = FastAPI()


@app.post("/calculate")
async def calculate(request: Request):
    temp = await request.json()
    n = int(temp["n"])
    x0 = int(temp["x0"])
    rank = int(temp["rank"])
    print(n, x0, rank)
    x = sp.symbols("x")
    func = n * sp.log(x)
    result = func.subs(x, x0)

    for i in range(1, rank):
        result += sp.diff(func, x, i).subs(x, x0) * (x - x0)**i / sp.factorial(i)
    # sp.pretty_print(result)
    return {"message": f"{result.evalf(subs={x: x0})}"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8001)