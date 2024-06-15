import redis
from django.conf import settings

from .models import Product

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class Recommender:
    """:class:`shop.Recommender` allows product purchase tracking & retrieves suggestions.

    Recommender class allows product purchases to be stored and will retrieve product
    suggestions for a given product or products.

    """

    def get_product_key(self, id):
        """get_product_key builds the Redis key for sorted set of related products.

        This method receives the ID of a Product object and builds the Redis key for the
        sorted set where related products are stored, which looks like
        product:[id]:purchased_with.

        Args:
            id (int): ID of a Product object

        Returns:
            string: Redis key, which looks like this: product:[id]:purchased_with

        """
        return f"product:{id}:purchased_with"

    def products_bought(self, products):
        """products_bought receives a list of Product objects that were bought together.

        This method receives a list of Product objects that have been bought together
        (these belong to the same order).

        Args:
            products (list): Product objects that have been bought together (same order)

        """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        """suggest_products_for retrieves products bought together for a given product list.

        This method receives products and max_results as parameters. It performs several
        actions. It gets the product IDs for the given Product objects. If only one
        product is given, it retrieves the ID of the products bought together with the
        given product, ordered by the total number of times they were bought together.
        To do so, it uses Redis' ZRANGE command. The max_results attribute limits the
        number of results specified to 6 by default. If more than one product is given,
        a temporary Redis key built with the IDs of the products is generated. It combines
        and sums all scores for the items contained in the sorted set of each of the
        given products, using the Redis ZUNIONSTORE command. This performs a union of
        the sorted sets with the given keys and stores the aggregated sum of scores of
        the elements in a new Redis key. The aggregated scores are saved in the temporary
        key. ZREM removes the same products it is getting recommendations for from the
        generated sorted set. IDs of products are retrieved from the temporary key,
        ordered by their scores using the ZRANGE command. The results are limited by the
        max_results attribute. The temporary key is removed using the redis-py delete()
        method that executes the Redis DEL command. Finally, the Product objects with
        the given IDs are retrieved, and the products are ordered in the same order as
        the members of the sorted set.

        Args:
            products (list): list of Product objects to get receommendations for. It can
                contain one or more products.
            max_results (int, optional): Represents the maximum number of recommendations
                to return. Defaults to 6.

        Returns:
            list: suggested_products are sorted by appearance

        """
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # generate a temporary key
            flat_ids = "".join([str(id) for id in product_ids])
            tmp_key = f"tmp_{flat_ids}"
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        """clear_purchases method clears the recommendations."""
        for id in Product.objects.values_list("id", flat=True):
            r.delete(self.get_product_key(id))
