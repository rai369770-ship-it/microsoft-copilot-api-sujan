from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

BASE = "https://rumix.shrishyamdevs.com/api/chat/copilot"

VALID_MODELS = {"smart", "chat", "search", "reasoning"}

@app.get("/")
async def root(prompt: str = Query(None), model: str = Query("smart")):
    if not prompt or not prompt.strip():
        return JSONResponse({"success": False, "response": "Empty prompt"}, status_code=400)

    model = model.lower()

    if model not in VALID_MODELS:
        return JSONResponse({"success": False, "response": "Invalid model name"}, status_code=400)

    try:
        url = f"{BASE}/{model}?p={requests.utils.quote(prompt)}"
        r = requests.get(url, timeout=30)

        if r.status_code != 200:
            return JSONResponse({"success": False, "response": "System error"}, status_code=500)

        data = r.json()
        return {"success": True, "response": data.get("response", "")}

    except:
        return JSONResponse({"success": False, "response": "System error"}, status_code=500)