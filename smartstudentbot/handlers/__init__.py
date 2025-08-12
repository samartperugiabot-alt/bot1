# This file makes the 'handlers' directory a Python package.

# You can aggregate all routers here for easier import in main.py
from .cmd_start import router as start_router
from .language import router as language_router
from .register import router as register_router
from .resources_hub import router as resources_hub_router
from .question import router as question_router
# Import other routers as they are created
# from .profile import router as profile_router
# ...

# A list of all routers to be included in the dispatcher
all_routers = [
    start_router,
    language_router,
    register_router,
    resources_hub_router,
    question_router,
    # profile_router,
]
