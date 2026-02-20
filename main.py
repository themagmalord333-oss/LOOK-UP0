from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="MAGMAxRICH API")

# NAYA API LINK
BASE_URL = "https://normal-num-info.vercel.app/info"

@app.get("/")
def home():
    return {"message": "Welcome to MAGMAxRICH API", "status": "Active"}

@app.get("/magma/lookup")
def lookup_number(phone: str):
    if not phone:
        raise HTTPException(status_code=400, detail="Phone number is required!")

    # Naye API ke hisaab se parameter 'number' set kiya hai
    params = {"number": phone}
    
    try:
        # 1. Naye API se Data mangwaya
        response = requests.get(BASE_URL, params=params)
        original_data = response.json()
        
        # 2. Data MODIFY (Naam Badlna)
        if "data" in original_data:
            if "API BY" in original_data["data"]:
                original_data["data"]["API BY"] = "@Anysnapsupport"
            if "Owner" in original_data["data"]:
                original_data["data"]["Owner"] = "@MAGMAxRICH"
                
        elif "API BY" in original_data:
            original_data["API BY"] = "@Anysnapsupport"
            original_data["Owner"] = "@MAGMAxRICH"
            
        # 3. Badla hua data user ko bheja
        return {
            "api_name": "MAGMAxRICH",
            "result": original_data
        }
        
    except Exception as e:
        return {"error": str(e)}