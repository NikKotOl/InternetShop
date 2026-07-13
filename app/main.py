from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def starter_page() -> str:
    return "Welcome!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
