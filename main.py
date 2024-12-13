from modules.frontend import *
from fastapi import FastAPI,HTTPException,Request
from modules.sqlwrapper import loglevel
from fastapi.responses import JSONResponse
app = FastAPI()
import uvicorn
import logging

LOG_FORMAT = "%(asctime)s | %(levelname)-4s | %(module)-10s:%(lineno)-4d | %(message)s"
logging.basicConfig(level = loglevel ,format=LOG_FORMAT)
# logging.debug("This is a test DEBUG log.")
# logging.info("This is a test INFO log.")
# logging.warning("This is a test WARNING log.")
# logging.error("This is a test ERROR log.")
# logging.critical("This is a test CRITICAL log.")
@app.post('/api/user/disconnect')
async def user_disconnect(request: Request):
    data = await request.json()
    user_id = data.get('userId')

    if user_id in online_users:
        logging.info(f"User {online_users[user_id]['name']} disconnected and removed from the list.")
        online_users.pop(user_id)
        update_user.refresh()

    else:
        raise HTTPException(status_code=404, detail="User not found")


# FOR CHECK S

@app.get("/check")
async def always_success():
    return JSONResponse(content={"message": "Success"}, status_code=200)



init(app)
if __name__ == '__main__':
   uvicorn.run("main:app", host="0.0.0.0", port=8080, workers=1, log_level="warning")
