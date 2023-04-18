"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, Semaphore

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.register_producer_lock = Lock()
        self.products_queue = []
        self.producers_dictionary = {}
        self.current_producer_id = 0

        self.producers_lock = Lock()
        self.consumers_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.register_producer_lock.acquire()
        current_value = self.current_producer_id
        self.current_producer_id += 1
        self.register_producer_lock.release()

        self.producers_dictionary[current_value] = self.queue_size_per_producer

        return current_value

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.producers_dictionary[producer_id] <= 0:
            return False

        self.products_queue.append(product)
        self.producers_dictionary[producer_id] -= 1

        return True


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        pass

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        pass

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        pass

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        pass
