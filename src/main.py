import uvicorn
from fastapi import FastAPI
from src.api.users import router as users_router



app = FastAPI(debug=True)

app.include_router(users_router)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)