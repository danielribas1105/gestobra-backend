from fastapi import APIRouter
import app.modules.auth.route as auth
import app.modules.car.route as car
import app.modules.jobs.route as jobs
import app.modules.statements.route as statements
import app.modules.user.route as user
import app.modules.works.route as woks


router = APIRouter(prefix="/api/v1")

# Register all routers
router.include_router(auth.router)
router.include_router(car.router)
router.include_router(jobs.router)
router.include_router(statements.router)
router.include_router(user.router)
router.include_router(woks.router)
