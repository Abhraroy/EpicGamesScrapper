from fastapi import FastAPI,BackgroundTasks
from Scrapper_free_games import scrapper_free_games


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Epic Games Scraper API"}



@app.get("/scrape")
def scrap():
    result = scrapper_free_games()
    if result is None:
        return {"message": "No free games found or an error occurred."}
    return {"message":result}