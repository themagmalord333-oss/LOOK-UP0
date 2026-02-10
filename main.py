import os
import asyncio
from fastapi import FastAPI, HTTPException
from pyrogram import Client

app = FastAPI()

# --- Aapki Details ---
API_ID = 37314366
API_HASH = "bd4c934697e91942ac911a5a287b46"
STRING_SESSION = "BQI5Xz4AQqz9RmhHLzmvF9-Bt6WIN65bdc6IbDerxk8kuuZbVy9dstGTN120mILr9sqR4qxYl-VpJ0GpKxpECmbUqSla0-Y49Lj-ENjxA9np0_hLpVBY6xCw0TWBgetpfMygqv2VVKIHMcDlqXzQUJq4cdAviXxwwFa5C89PcsCt4LKwb45gboSbir8YCmHWy_ob5D7sHthy-5o68JtW68o9lZenYRuEzSZXI8_kFv_RK8NL5cMR2zF1epTDJhV6blnLAuQ1eyMVLI4fOBByo6pvZLYdOFExbxneMKos7sPI6qy4DRLYIN8cWqIl0_38zDbT55t2WEUl3fmsBraSW82Yl9AHNAAAAAFJSgVkAA"

# Pyrogram Client Setup
client = Client(
    "bridge_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True
)

@app.on_event("startup")
async def startup():
    if not client.is_connected:
        await client.start()

@app.get("/")
async def health_check():
    return {"status": "running", "bot": "online"}

@app.get("/fetch")
async def fetch_data(id: str):
    # --- YAHAN TARGET BOT KA USERNAME DALEIN ---
    target_bot = "@Target_Bot_Username" 
    
    try:
        # 1. Target bot ko message bhejna
        sent = await client.send_message(target_bot, id)
        
        # 2. Reply ka wait karna (Maximum 10 seconds)
        for _ in range(10):
            await asyncio.sleep(1)
            async for message in client.get_chat_history(target_bot, limit=1):
                if message.id > sent.id:
                    return {
                        "status": "success",
                        "query": id,
                        "data": message.text or "Content received (Media/File)"
                    }
        
        return {"status": "timeout", "message": "Bot ne reply nahi diya."}
        
    except Exception as e:
        return {"status": "error", "details": str(e)}