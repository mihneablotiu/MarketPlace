"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread, Lock


class Consumer(Thread):
    """
    Class that represents a consumer.
    """
    print_lock = Lock()

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs["name"]

        self.cart_id = self.marketplace.new_cart()

    def run(self):
        for cart in self.carts:
            for current_cart in cart:
                action_type = current_cart["type"]
                product = current_cart["product"]
                quantity = current_cart["quantity"]

                for _ in range(quantity):
                    if action_type == "add":
                        while not self.marketplace.add_to_cart(self.cart_id, product):
                            time.sleep(self.retry_wait_time)

                    if action_type == "remove":
                        self.marketplace.remove_from_cart(self.cart_id, product)

        buy_list = self.marketplace.place_order(self.cart_id)
        for (current_product, _) in buy_list:
            with Consumer.print_lock:
                print(self.name + " bought " + str(current_product))
