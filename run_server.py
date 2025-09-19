#!/usr/bin/env python3
"""
CONVAI Server Runner
Run this script to start the CONVAI server.
"""

import uvicorn
from convai.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "convai.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )