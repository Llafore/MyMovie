from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()

@router.get('/first-reviews')
def get_first_reviews():
    initial_media = load_initial_media()
    JSONResponse(to_json(initial_media))
    return