# API information endpoint
@app.get("/api/info", tags=["General"])
def api_info():
    return {
        "name": "E-Commerce API",
        "description": "API for managing products in an online store",
        "version": "1.2.0",
        "documentation": "/docs",
        "status": "active"
    }