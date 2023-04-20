"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import logging
import os.path
from logging.handlers import RotatingFileHandler
from threading import Lock
import time


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
        self.consumers_print_lock = Lock()

        for i in range(10):
            if os.path.exists("marketplace.log" + "." + str(i)):
                os.remove("marketplace.log" + "." + str(i))

        self.logger = logging.getLogger("marketplace_logger")
        self.logger.setLevel(logging.INFO)

        self.logger_handler = RotatingFileHandler("marketplace.log", maxBytes=1000000, backupCount=10)

        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.formatter.converter = time.gmtime

        self.logger_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.logger_handler)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.logger.info("Producer entered register_producer()")
        with self.register_producer_lock:
            current_value = self.current_producer_id
            self.current_producer_id += 1

        self.producers_dictionary[current_value] = self.queue_size_per_producer

        self.logger.info("Producer exited register_producer() with id: " + str(current_value))
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
        self.logger.info("Producer with id: " + str(producer_id) + " entered publish() with product: " + str(product))
        if self.producers_dictionary[producer_id] <= 0:
            self.logger.error("Producer with id: " + str(producer_id)
                              + " exited publish() with False and could not publish" + str(product))
            return False

        self.products_queue.append((product, producer_id))
        self.producers_dictionary[producer_id] -= 1

        self.logger.info("Producer with id: " + str(producer_id)
                         + " exited publish() with True and successfully published " + str(product))
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.logger.info("Consumer entered new_cart()")
        with self.register_new_cart_lock:
            current_value = self.current_cart_id
            self.current_cart_id += 1

        self.logger.info("Consumer exited new_cart() with cart_id: " + str(current_value))
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
        self.logger.info("Consumer with cart_id: " + str(cart_id)
                         + " entered add_to_cart() with product: " + str(product))

        self.consumers_lock.acquire()
        products_list = list(map(lambda x: x[0], self.products_queue))
        if product in products_list:
            index = products_list.index(product)
            (_, producer_id) = self.products_queue[index]
            self.products_queue.pop(index)
            self.producers_dictionary[producer_id] += 1

            self.consumers_lock.release()

            if cart_id in self.consumers_carts:
                self.consumers_carts[cart_id].append((product, producer_id))
            else:
                self.consumers_carts[cart_id] = []
                self.consumers_carts[cart_id].append((product, producer_id))

            self.logger.info("Consumer with cart_id: " + str(cart_id)
                             + " exited add_to_cart() with True and successfully added product: "
                             + str(product) + " to cart")
            return True

        self.consumers_lock.release()

        self.logger.error("Consumer with cart_id: " + str(cart_id)
                          + " exited add_to_cart() with False and failed to add product: "
                          + str(product) + " to cart")
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.logger.info("Consumer with cart_id: " + str(cart_id) + " entered remove_from_cart() with product: " + str(product))
        products_list = list(map(lambda x: x[0], self.consumers_carts[cart_id]))

        if product in products_list:
            index = products_list.index(product)
            (_, producer_id) = self.consumers_carts[cart_id][index]
            self.consumers_carts[cart_id].remove((product, producer_id))
            self.products_queue.append((product, producer_id))
            self.producers_dictionary[producer_id] -= 1

            self.logger.info("Consumer with cart_id: " + str(cart_id)
                             + " exited remove_from_cart() with True and deleted product: " + str(product))

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.info("Consumer with cart_id: " + str(cart_id) + " entered and exited place_order()")
        return self.consumers_carts[cart_id]

    def print_consumer(self, consumer_name, cart_id):
        """
        Prints the products that the consumers bought
        from the marketplace.

        :type consumer_name: str
        :param consumer_name: the name of the consumer

        :type cart_id: int
        :param cart_id: the cart that is currently bought
        """
        self.logger.info("Consumer with cart_id: " + str(cart_id) + " and name "
                         + consumer_name + " entered print_consumer()")

        buy_list = self.place_order(cart_id)
        for (current_product, _) in buy_list:
            with self.consumers_print_lock:
                print(consumer_name + " bought " + str(current_product))

        self.consumers_carts[cart_id].clear()
        self.logger.info("Consumer with cart_id: " + str(cart_id) + " and name "
                         + consumer_name + " exited print_consumer()")
