from fastapi import APIRouter
import app.modules.auth.route as auth
import app.modules.car.route as car
import app.modules.carriers.route as carrier
import app.modules.jobs.route as jobs
import app.modules.statements.route as statements
import app.modules.user.route as user
import app.modules.works.route as woks
import app.modules.fleet.route as fleet
import app.modules.materials.route as materials
import app.modules.payments.route as payments

router = APIRouter(prefix="/api/v1")

# Register all routers
router.include_router(auth.router)
router.include_router(car.router)
router.include_router(carrier.router)
router.include_router(jobs.router)
router.include_router(statements.router)
router.include_router(user.router)
router.include_router(woks.router)
router.include_router(fleet.router)
router.include_router(materials.router)
router.include_router(payments.router)
