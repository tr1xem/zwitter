import frontend
from frontend import *
from fastapi import FastAPI,HTTPException,Request
app = FastAPI()



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





frontend.init(app)

if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
