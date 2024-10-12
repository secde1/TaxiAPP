from .auth import router as auth_router
from .support import router as support_router
from .preferences import router as preferences_router

__all__ = ["auth_router", "support_router", "preferences_router"]
