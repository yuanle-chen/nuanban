import httpx
from app.core.config import settings


async def regeo_code(latitude: float, longitude: float) -> str:
    if not settings.AMAP_KEY:
        return ""
    
    url = "https://restapi.amap.com/v3/geocode/regeo"
    params = {
        "key": settings.AMAP_KEY,
        "location": f"{longitude},{latitude}",
        "extensions": "base"
    }
    
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data.get("status") == "1" and data.get("regeocode"):
                regeocode = data["regeocode"]
                address_component = regeocode.get("addressComponent", {})
                
                province = address_component.get("province", "")
                city = address_component.get("city", "")
                district = address_component.get("district", "")
                township = address_component.get("township", "")
                
                formatted = regeocode.get("formatted_address", "")
                
                parts = []
                if province and province != city:
                    parts.append(province)
                if city:
                    parts.append(city)
                if district:
                    parts.append(district)
                if township:
                    parts.append(township)
                
                return "".join(parts) if parts else formatted
    except Exception as e:
        print(f"逆地理编码失败: {e}")
    
    return ""
