"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import logging
import os.path
import unittest
from logging.handlers import RotatingFileHandler
from threading import Lock
import time
from tema.product import Tea, Coffee


class TestMarketplace(unittest.TestCase):
    """
    Class that tests all the methods of the Marketplace class. It's used for unit testing.
    """
    def setUp(self):
        """
        Set up the Marketplace object that will be used in the tests with maximum 4 products
        per producer in order to be able to test it easily.
        """
        self.marketplace = Marketplace(4)

        self.first_producer = self.marketplace.register_producer()
        self.second_producer = self.marketplace.register_producer()
        self.third_producer = self.marketplace.register_producer()

        self.first_cart = self.marketplace.new_cart()
        self.second_cart = self.marketplace.new_cart()
        self.third_cart = self.marketplace.new_cart()

    def test_register_producer(self):
        """
        Test the register_producer() method registering 1000 producers. Each time the value
        returned by the method should be equal to the number of producers registered so far.
        """
        for i in range(1000):
            self.assertEqual(self.marketplace.register_producer(), i + 3)
            self.assertEqual(self.marketplace.producers_dictionary[i + 3],
                             self.marketplace.queue_size_per_producer)

    def test_publish(self):
        """
        Test the publish() method by publishing 1000 products for each producer.
        The first 4 products should be published successfully and the rest should not be published.
        """
        for i in range(1000):
            if i < 4:
                self.assertTrue(self.marketplace
                                .publish(self.first_producer,
                                         Coffee(name='Indonesia', price=1,
                                                acidity='5.05', roast_level='MEDIUM')))

                self.assertTrue(self.marketplace
                                .publish(self.second_producer,
                                         Tea(name='Earl Grey', price=2,
                                             type='Black')))

                self.assertTrue(self.marketplace
                                .publish(self.third_producer,
                                         Coffee(name='Ethiopia', price=10,
                                                acidity='5.09', roast_level='MEDIUM')))

                self.assertEqual(self.marketplace.producers_dictionary[self.first_producer],
                                 self.marketplace.queue_size_per_producer - i - 1)

                self.assertEqual(self.marketplace.producers_dictionary[self.second_producer],
                                 self.marketplace.queue_size_per_producer - i - 1)

                self.assertEqual(self.marketplace.producers_dictionary[self.third_producer],
                                 self.marketplace.queue_size_per_producer - i - 1)
            else:
                self.assertFalse(self.marketplace
                                 .publish(self.first_producer,
                                          Tea(name='Linden', price=9,
                                              type='Herbal')))

                self.assertFalse(self.marketplace
                                 .publish(self.second_producer,
                                          Coffee(name='Brazil', price=3,
                                                 acidity='3.05', roast_level='LIGHT')))

                self.assertFalse(self.marketplace
                                 .publish(self.third_producer,
                                          Tea(name='Green', price=4,
                                              type='Green')))

        self.assertIn((Coffee(name='Indonesia', price=1, acidity='5.05', roast_level='MEDIUM'), 0),
                      self.marketplace.products_queue)
        self.assertIn((Tea(name='Earl Grey', price=2, type='Black'), 1),
                      self.marketplace.products_queue)
        self.assertIn((Coffee(name='Ethiopia', price=10, acidity='5.09', roast_level='MEDIUM'), 2),
                      self.marketplace.products_queue)

        self.assertEqual(self.marketplace.producers_dictionary[self.first_producer], 0)
        self.assertEqual(self.marketplace.producers_dictionary[self.second_producer], 0)
        self.assertEqual(self.marketplace.producers_dictionary[self.third_producer], 0)

    def test_new_cart(self):
        """
        Test the new_cart() method by creating 1000 carts. The value returned by the method
        should be equal to the number of carts created so far.
        """
        for i in range(1000):
            self.assertEqual(self.marketplace.new_cart(), i + 3)

    def test_add_to_cart(self):
        """
        Test the add_to_cart() method by trying to add more than 4 products to each cart.
        Some of the products should be added successfully and some should not be added
        because they don't exist in the queue.
        """
        for _ in range(10):
            self.marketplace.publish(self.first_producer,
                                     Coffee(name='Indonesia', price=1,
                                            acidity='5.05', roast_level='MEDIUM'))

            self.marketplace.publish(self.second_producer,
                                     Tea(name='Earl Grey', price=2, type='Black'))

            self.marketplace.publish(self.third_producer,
                                     Coffee(name='Ethiopia', price=10,
                                            acidity='5.09', roast_level='MEDIUM'))

        for _ in range(2):
            self.assertTrue(self.marketplace.add_to_cart(self.first_cart,
                                                         Coffee(name='Indonesia', price=1,
                                                                acidity='5.05',
                                                                roast_level='MEDIUM')))

            self.assertTrue(self.marketplace.add_to_cart(self.second_cart,
                                                         Tea(name='Earl Grey', price=2,
                                                             type='Black')))

            self.assertTrue(self.marketplace.add_to_cart(self.third_cart,
                                                         Coffee(name='Ethiopia', price=10,
                                                                acidity='5.09',
                                                                roast_level='MEDIUM')))

        self.assertEqual(self.marketplace.consumers_carts[self.first_cart],
                         [(Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0)])

        self.assertEqual(self.marketplace.consumers_carts[self.second_cart],
                         [(Tea(name='Earl Grey', price=2, type='Black'), 1),
                          (Tea(name='Earl Grey', price=2, type='Black'), 1)])

        self.assertEqual(self.marketplace.consumers_carts[self.third_cart],
                         [(Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2)])

        for _ in range(2):
            self.assertTrue(self.marketplace.add_to_cart(self.first_cart,
                                                         Coffee(name='Ethiopia', price=10,
                                                                acidity='5.09',
                                                                roast_level='MEDIUM')))

            self.assertTrue(self.marketplace.add_to_cart(self.second_cart,
                                                         Coffee(name='Indonesia', price=1,
                                                                acidity='5.05',
                                                                roast_level='MEDIUM')))

            self.assertTrue(self.marketplace.add_to_cart(self.third_cart,
                                                         Tea(name='Earl Grey', price=2,
                                                             type='Black')))

        self.assertEqual(self.marketplace.consumers_carts[self.first_cart],
                         [(Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2)])

        self.assertEqual(self.marketplace.consumers_carts[self.second_cart],
                         [(Tea(name='Earl Grey', price=2, type='Black'), 1),
                          (Tea(name='Earl Grey', price=2, type='Black'), 1),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0)])

        self.assertEqual(self.marketplace.consumers_carts[self.third_cart],
                         [(Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Tea(name='Earl Grey', price=2, type='Black'), 1),
                          (Tea(name='Earl Grey', price=2, type='Black'), 1)])

        for _ in range(100):
            self.assertFalse(self.marketplace.add_to_cart(self.first_cart,
                                                          Coffee(name='Ethiopia', price=10,
                                                                 acidity='5.09',
                                                                 roast_level='MEDIUM')))

            self.assertFalse(self.marketplace.add_to_cart(self.second_cart,
                                                          Coffee(name='Indonesia', price=1,
                                                                 acidity='5.05',
                                                                 roast_level='MEDIUM')))

            self.assertFalse(self.marketplace.add_to_cart(self.third_cart,
                                                          Tea(name='Earl Grey', price=2,
                                                              type='Black')))

    def test_remove_from_cart(self):
        """
        Test the remove_from_cart method. Firstly we add some items to the carts exactly as in
        test_add_to_cart. Then we remove some of the items and check if the items were removed.
        We also try to remove some items that don't exist and check if the method does nothing.
        """
        for _ in range(4):
            self.marketplace.publish(self.first_producer,
                                     Coffee(name='Indonesia', price=1,
                                            acidity='5.05', roast_level='MEDIUM'))

            self.marketplace.publish(self.second_producer,
                                     Tea(name='Earl Grey', price=2, type='Black'))

            self.marketplace.publish(self.third_producer,
                                     Coffee(name='Ethiopia', price=10,
                                            acidity='5.09', roast_level='MEDIUM'))

        for _ in range(2):
            self.marketplace.add_to_cart(self.first_cart,
                                         Coffee(name='Indonesia', price=1,
                                                acidity='5.05', roast_level='MEDIUM'))
            self.marketplace.add_to_cart(self.second_cart,
                                         Tea(name='Earl Grey', price=2, type='Black'))
            self.marketplace.add_to_cart(self.third_cart,
                                         Coffee(name='Ethiopia', price=10,
                                                acidity='5.09', roast_level='MEDIUM'))

        self.assertEqual(self.marketplace.consumers_carts[self.first_cart],
                         [(Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0)])

        self.assertEqual(self.marketplace.consumers_carts[self.second_cart],
                         [(Tea(name='Earl Grey', price=2, type='Black'), 1),
                          (Tea(name='Earl Grey', price=2, type='Black'), 1)])

        self.assertEqual(self.marketplace.consumers_carts[self.third_cart],
                         [(Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2)])

        self.marketplace.remove_from_cart(self.first_cart,
                                          Tea(name='Earl Grey', price=2, type='Black'))
        self.assertEqual(self.marketplace.consumers_carts[self.first_cart],
                         [(Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0)])

        self.marketplace.remove_from_cart(self.first_cart,
                                          Coffee(name='Indonesia', price=1,
                                                 acidity='5.05', roast_level='MEDIUM'))
        self.assertEqual(self.marketplace.consumers_carts[self.first_cart],
                         [(Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0)])

        self.marketplace.remove_from_cart(self.first_cart,
                                          Coffee(name='Indonesia', price=1,
                                                 acidity='5.05', roast_level='MEDIUM'))
        self.assertEqual(self.marketplace.consumers_carts[self.first_cart], [])

        self.marketplace.remove_from_cart(self.first_cart,
                                          Coffee(name='Indonesia', price=1,
                                                 acidity='5.05', roast_level='MEDIUM'))
        self.assertEqual(self.marketplace.consumers_carts[self.first_cart], [])

        for _ in range(100):
            self.marketplace.remove_from_cart(self.first_cart,
                                              Coffee(name='Indonesia', price=1,
                                                     acidity='5.05', roast_level='MEDIUM'))
            self.marketplace.remove_from_cart(self.second_cart,
                                              Tea(name='Earl Grey', price=2, type='Black'))
            self.marketplace.remove_from_cart(self.third_cart,
                                              Tea(name='Earl Grey', price=2, type='Black'))

            self.marketplace.remove_from_cart(self.third_cart,
                                              Coffee(name='Ethiopia', price=10,
                                                     acidity='5.09', roast_level='MEDIUM'))
            self.marketplace.remove_from_cart(self.second_cart,
                                              Coffee(name='Ethiopia', price=10,
                                                     acidity='5.09', roast_level='MEDIUM'))

        self.assertEqual(self.marketplace.consumers_carts[self.first_cart], [])
        self.assertEqual(self.marketplace.consumers_carts[self.second_cart], [])
        self.assertEqual(self.marketplace.consumers_carts[self.third_cart], [])

    def test_place_order(self):
        """
        Test the place_order method. Firstly we add some items to the carts exactly as in
        test_add_to_cart. Then we place an order and check if the items in the cart are exactly
        the ones returned by the method.

        We also try to place an order with an empty cart and check if the method does nothing.
        """

        for _ in range(4):
            self.marketplace.publish(self.first_producer,
                                     Coffee(name='Indonesia', price=1,
                                            acidity='5.05', roast_level='MEDIUM'))

            self.marketplace.publish(self.second_producer,
                                     Tea(name='Earl Grey', price=2, type='Black'))

            self.marketplace.publish(self.third_producer,
                                     Coffee(name='Ethiopia', price=10,
                                            acidity='5.09', roast_level='MEDIUM'))

        for _ in range(4):
            self.marketplace.add_to_cart(self.first_cart,
                                         Coffee(name='Indonesia', price=1,
                                                acidity='5.05', roast_level='MEDIUM'))
            self.marketplace.add_to_cart(self.second_cart,
                                         Tea(name='Earl Grey', price=2, type='Black'))
            self.marketplace.add_to_cart(self.third_cart,
                                         Coffee(name='Ethiopia', price=10,
                                                acidity='5.09', roast_level='MEDIUM'))

        self.assertEqual(self.marketplace.place_order(self.first_cart),
                         [(Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0),
                          (Coffee(name='Indonesia', price=1,
                                  acidity='5.05', roast_level='MEDIUM'), 0)])

        for _ in range(4):
            self.marketplace.remove_from_cart(self.first_cart,
                                              Coffee(name='Indonesia', price=1,
                                                     acidity='5.05', roast_level='MEDIUM'))

        self.assertEqual(self.marketplace.place_order(self.first_cart), [])

        self.marketplace.remove_from_cart(self.second_cart,
                                          Tea(name='Earl Grey', price=2, type='Black'))
        self.marketplace.remove_from_cart(self.second_cart,
                                          Tea(name='Earl Grey', price=2, type='Black'))
        self.marketplace.remove_from_cart(self.second_cart,
                                          Tea(name='Earl Grey', price=2, type='Black'))

        self.marketplace.remove_from_cart(self.third_cart,
                                          Coffee(name='Ethiopia', price=10,
                                                 acidity='5.09', roast_level='MEDIUM'))
        self.marketplace.remove_from_cart(self.third_cart,
                                          Coffee(name='Ethiopia', price=10,
                                                 acidity='5.09', roast_level='MEDIUM'))

        for _ in range(4):
            self.marketplace.publish(self.first_producer,
                                     Tea(name='Earl Grey', price=2, type='Black'))

            self.marketplace.publish(self.second_producer,
                                     Coffee(name='Ethiopia', price=10,
                                            acidity='5.09', roast_level='MEDIUM'))

            self.marketplace.publish(self.third_producer,
                                     Tea(name='Earl Grey', price=2, type='Black'))

        self.marketplace.add_to_cart(self.second_cart,
                                     Coffee(name='Ethiopia', price=10,
                                            acidity='5.09', roast_level='MEDIUM'))
        self.marketplace.add_to_cart(self.second_cart,
                                     Coffee(name='Ethiopia', price=10,
                                            acidity='5.09', roast_level='MEDIUM'))

        self.assertEqual(self.marketplace.place_order(self.second_cart),
                         [(Tea(name='Earl Grey', price=2, type='Black'), 1),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2)])

        self.assertEqual(self.marketplace.place_order(self.third_cart),
                         [(Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2)])

        self.marketplace.add_to_cart(self.third_cart,
                                     Tea(name='Earl Grey', price=2, type='Black'))
        self.marketplace.add_to_cart(self.third_cart,
                                     Tea(name='Earl Grey', price=2, type='Black'))

        self.assertEqual(self.marketplace.place_order(self.third_cart),
                         [(Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Coffee(name='Ethiopia', price=10,
                                  acidity='5.09', roast_level='MEDIUM'), 2),
                          (Tea(name='Earl Grey', price=2, type='Black'), 1),
                          (Tea(name='Earl Grey', price=2, type='Black'), 1)])


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

        self.logger_handler = RotatingFileHandler("marketplace.log",
                                                  maxBytes=1000000, backupCount=10)

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

        self.logger.info("Producer exited register_producer() with id: %s", str(current_value))
        return current_value

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False,
        it should wait and then try again.
        """
        self.logger.info("Producer with id: %s entered publish() with product: %s",
                         str(producer_id), str(product))

        if self.producers_dictionary[producer_id] <= 0:
            self.logger.error("Producer with id: %s exited publish() "
                              "with False and could not publish %s", str(producer_id), str(product))
            return False

        self.products_queue.append((product, producer_id))
        self.producers_dictionary[producer_id] -= 1

        self.logger.info("Producer with id: %s exited publish()"
                         "with True and successfully published %s", str(producer_id), str(product))
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

        self.logger.info("Consumer exited new_cart() with cart_id: %s", str(current_value))
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
        self.logger.info("Consumer with cart_id: %s entered add_to_cart() with product: %s",
                         str(cart_id), str(product))

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

            self.logger.info("Consumer with cart_id: %s exited add_to_cart() with True and "
                             "successfully added product: %s to cart", str(cart_id), str(product))
            return True

        self.consumers_lock.release()

        self.logger.error("Consumer with cart_id: %s exited add_to_cart() with False and "
                          "failed to add product: %s to cart", str(cart_id), str(product))
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.logger.info("Consumer with cart_id: %s entered remove_from_cart() with product: %s",
                         str(cart_id), str(product))

        products_list = list(map(lambda x: x[0], self.consumers_carts[cart_id]))

        if product in products_list:
            index = products_list.index(product)
            (_, producer_id) = self.consumers_carts[cart_id][index]
            self.consumers_carts[cart_id].remove((product, producer_id))
            self.products_queue.append((product, producer_id))
            self.producers_dictionary[producer_id] -= 1

            self.logger.info("Consumer with cart_id: %s exited remove_from_cart() and "
                             "deleted product: %s", str(cart_id), str(product))

        self.logger.info("Consumer with cart_id: %s exited remove_from_cart() and "
                         "failed to delete product: %s", str(cart_id), str(product))

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        self.logger.info("Consumer with cart_id: %s entered and exited place_order()", str(cart_id))
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
        self.logger.info("Consumer with cart_id: %s and "
                         "name %s entered print_consumer()",
                         str(cart_id), consumer_name)

        buy_list = self.place_order(cart_id)
        for (current_product, _) in buy_list:
            with self.consumers_print_lock:
                print(consumer_name + " bought " + str(current_product))

        self.consumers_carts[cart_id].clear()
        self.logger.info("Consumer with cart_id: %s and "
                         "name %s exited print_consumer()",
                         str(cart_id), consumer_name)
