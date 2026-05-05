from fastapi import APIRouter, HTTPException, status, Query, Depends
import routes.categories.models as categories_models
from schemas.categories import Category, BaseCategory
from schemas.products import Product
from middlewares import JWTBearer

categories_router = APIRouter(prefix='/categories', tags=['categories'], dependencies=[Depends(JWTBearer())])

@categories_router.get('/')
def get_categories(search: str = '', page: int = Query(default=1, ge=1), per_page: int = Query(default=1, ge=1)) -> list[Category]:
    
    categories = categories_models.get_categories(search, page, per_page)

    if categories is None:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})
    
    categories = [Category(**category) for category in categories]

    return categories

@categories_router.get('/{id}')
def get_category_by_id(id: int):
    
    category = categories_models.get_category_by_id(id)

    if not category:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Category not found'})

    return category

@categories_router.get('/products/{id}')
def get_products_by_category(category_id: int) -> list[Product]:
    
    exists = categories_models.get_category_by_id(category_id)

    if not exists:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Category not found'})
    
    products = categories_models.get_products_by_category(category_id)

    if not products:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'No products in this category'})
    
    products = [Product(**product) for product in products]

    return products

@categories_router.post('/create')
def create_category(category: Category):
    
    if not categories_models.get_category_by_code(category.code):

        result = categories_models.create_category(
            category.name,
            category.code,
            category.summary
        )

        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                                'message': 'Server internal error'})

        if result is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                'message': 'Category not created'})

        return {
            'message': 'Category created successfully',
        }
    
    else:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                'message': 'Category code repeated'})
        
@categories_router.put('/update/{id}')
def update_category(category:  BaseCategory, id: int):

    category_exists = categories_models.get_category_by_id(id)

    if not category_exists:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Category not found'})

    result = categories_models.update_category(
        category.name,
        category.summary,
        id
    )

    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    if result is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Category not updated'})

    return {
        'message': 'Category updated successfully',
    }

@categories_router.delete('/delete/{id}') 
def delete_category(id: int):
    
    category_exists = categories_models.get_category_by_id(id)

    if not category_exists:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Category not found'})
    
    result = categories_models.delete_category(id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    return {
        'message': 'Category deleted successfully',
    }