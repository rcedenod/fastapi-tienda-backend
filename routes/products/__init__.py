from fastapi import APIRouter, HTTPException, status, Query, Depends
import routes.products.models as products_models
from schemas.products import Product, BaseProduct
from middlewares import JWTBearer

products_router = APIRouter(prefix='/products', tags=['products'], dependencies=[Depends(JWTBearer())])


@products_router.get('/')
def get_products(search: str = '', page: int = Query(default=1, ge=1), per_page: int = Query(default=10, ge=1)) -> list[Product]:

    products = products_models.get_products(search, page, per_page)

    if products is None:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    products = [Product(**product) for product in products]

    return products

@products_router.get('/search/{id}')
def get_product_by_id(id: int):
    
    product = products_models.get_product_by_id(id)

    if product is False:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Product not found'})

    return product

@products_router.post('/create')
def create_product(product: Product):

    if not products_models.get_product_by_code(product.code):

        result = products_models.create_product(
            product.category_id,
            product.name,
            product.code,
            product.price,
            product.summary,
            product.description
        )

        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                                'message': 'Server internal error'})

        if result is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                'message': 'Product not created'})

        return {
            'message': 'Product created successfully',
        }
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                'message': 'Product code repeated'})

@products_router.put('/update/{id}')
def update_product(product: BaseProduct, id: int):
    

    product_exists = products_models.get_product_by_id(id)

    if product_exists is False:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Product not found'})

    result = products_models.update_product(
        id,
        product.category_id,
        product.name,
        product.price,
        product.summary,
        product.description
    )

    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    if result is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Product not created'})

    return {
        'message': 'Product updated successfully',
    }

@products_router.delete('/delete/{id}')
def delete_product(id: int):

    exists = products_models.get_product_by_id(id)

    if exists is False:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Product not found'})

    result = products_models.delete_product(id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    return {
        'message': 'Product deleted successfully',
    }

@products_router.get('/comments/{id}')
def get_product_comments(id: int):
    
    exists = products_models.get_product_by_id(id)

    if exists is False:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Product not found'})
    
    comments = products_models.get_product_comments(id)

    if len(comments) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Product has no comments'})
    
    return comments