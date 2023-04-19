"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock

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

        self.products_queue = []

        self.current_producer_id = 0
        self.register_producer_lock = Lock()
        self.producers_dictionary = {}

        self.current_cart_id = 0
        self.register_new_cart_lock = Lock()
        self.consumers_carts = {}

        self.consumers_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.register_producer_lock:
            current_value = self.current_producer_id
            self.current_producer_id += 1

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

        if self.producers_dictionary[producer_id] == 0:
            return False

        self.products_queue.append((product, producer_id))
        self.producers_dictionary[producer_id] -= 1

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.register_new_cart_lock:
            current_value = self.current_cart_id
            self.current_cart_id += 1

        return current_value

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        self.consumers_lock.acquire()
        products_list = list(map(lambda x: x[0], self.products_queue))
        if product in products_list:
            index = products_list.index(product)
            (_, producer_id) = self.products_queue[index]
            self.products_queue.remove(self.products_queue[index])
            self.producers_dictionary[producer_id] += 1

            self.consumers_lock.release()

            if cart_id in self.consumers_carts:
                self.consumers_carts[cart_id].append((product, producer_id))
            else:
                self.consumers_carts[cart_id] = []
                self.consumers_carts[cart_id].append((product, producer_id))

            return True

        self.consumers_lock.release()
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        products_list = list(map(lambda x: x[0], self.consumers_carts[cart_id]))

        if product in products_list:
            index = products_list.index(product)
            (_, producer_id) = self.consumers_carts[cart_id][index]
            self.consumers_carts[cart_id].remove((product, producer_id))
            self.products_queue.append((product, producer_id))
            self.producers_dictionary[producer_id] -= 1

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.consumers_carts[cart_id]
