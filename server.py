from fastapi import FastAPI,BackgroundTasks
from Scrapper_free_games import scrapper_free_games


app = FastAPI()

@app.get("/scrap")
async def scrap(background_tasks: BackgroundTasks):
    
    background_tasks.add_task(scrapper_free_games)
    return {"message": "Scrapping started in the background."}