from decimal import Decimal

from coupons.models import Coupon
from django.conf import settings
from shop.models import Product


class Cart:
    """Manages the shopping cart.

    Products can be added to the cart with add() and updated with save()

    """

    def __init__(self, request):
        """__init__ initializes the shopping cart.

        Stores the current session and makes it accessible to other methods of the Cart
        class. Gets the cart from the current session if it exists, if not it creates an
        empty cart. Cart is a dictionary using product IDs as keys, and for each product
        key, a dictionary will be a value that includes quantity and price. This prevents
        a product from being added more than once to the cart, simplifying cart item
        retrieval.

        Args:
            request (object): required to initialize cart.

        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def __iter__(self):
        """__iter__ iterates over the items in cart and gets products from the database.

        Yields:
            item: object in cart being iterated over

        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """__len__ counts all the items in the cart.

        Returns:
            int: sum of the quantities of all items in the cart

        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """add method adds a product to the cart or updates its quantity.

        Uses product ID as key in cart's content dictionary. Converts ID key to string
        so Django can use JSON to serialize session data. Value is a dict with quantity
        and price figures for the Product. Price is converted from decimal to string for
        serialization. The save() method is called to save the cart in the session.

        Args:
            product (object): Product to add to the cart
            quantity (int, optional): number of Product to add. Defaults to 1.
            override_quantity (bool, optional): whether the new quantity has to be added
                to the existing quantity. Defaults to False.

        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        # marks the session as 'modified' to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """remove method removes a given Product from the cart dictionary and updates cart.

        Args:
            product (object): Product to remove from cart

        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """get_total_price calculates the total cost of the items in the cart.

        Returns:
            int: the total cost of all the items in the cart.

        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    @property
    def coupon(self):
        """coupon method is defined as a property. If cart contains a coupon_id attribute,
        the Coupon object with the given ID is returned.

        Returns:
            object: Coupon object with the given ID

        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """get_discount retrieves discount rate and applies it if cart contains a coupon.

        If the cart contains a coupon, retrieves its discount rate and returns the amount
        to be deducted from the total amount of the cart.

        Returns:
            Decimal: amount to be deducted from the total amount of the cart.

        """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """get_total_price_after_discount deducts amount returned from total amount of cart.

        Returns the total amount of the cart after deducting the amount returned by the
        :method:`coupons.get_discount` method.

        Returns:
            int: the total amount of the cart after deducting the discounted amount

        """
        return self.get_total_price() - self.get_discount()
