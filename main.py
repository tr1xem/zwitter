import frontend
from frontend import *
from fastapi import FastAPI,HTTPException,Request
app = FastAPI()
import uvicorn


@app.post('/api/user/disconnect')
async def user_disconnect(request: Request):
    data = await request.json()
    user_id = data.get('userId')

    if user_id in online_users:
        print(f"[LOG]: User {online_users[user_id]['name']} with ID {user_id} disconnected.")
        online_users.pop(user_id)
        update_user.refresh()

    else:
        raise HTTPException(status_code=404, detail="User not found")


# FOR CHECKS

@app.get("/check")
async def always_success():
    return JSONResponse(content={"message": "Success"}, status_code=200)



frontend.init(app)

if __name__ == '__main__':
   uvicorn.run("main:app", host="127.0.0.1", port=8080, workers=1, log_level="info")
