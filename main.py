from core.handlers import setup_exception_handlers
from fastapi import FastAPI
from routes import category , product
app = FastAPI()
setup_exception_handlers(app)

app.include_router(category.router)
app.include_router(product.router)



@app.get("/")
def root():
    return {
        "success": True,
        "message": "Bienvenue sur l'API POC",
        "data": None,
    }