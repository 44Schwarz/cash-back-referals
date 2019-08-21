#!/usr/bin/env python3
import unittest
import os.path

from find_clients import LOG_FILE, main, parse_log


class TestFindClients(unittest.TestCase):
    def test_log_file_exists(self):
        self.assertTrue(os.path.isfile(LOG_FILE))

    def test_main(self):
        user_activity_example = {
            'user1': [
                ('https://shop.com/products/?id=2', 'yandex.ru'),
                ('https://shop.com/products/id?=2', 'referal.ours.com'),
                ('https://shop.com/products/id?=2', 'ad.theirs1.com'),
                ('https://shop.com/checkout', 'shop.com')
            ],
            'user2': [
                ('https://shop.com/', 'referal.ours.com'),
                ('https://shop.com/products/id?=10', 'shop.com'),
                ('https://shop.com/products/id?=25', 'shop.com'),
                ('https://shop.com/cart', 'shop.com'),
                ('https://shop.com/checkout', 'shop.com')
            ],
            'user3': [
                ('https://shop.com/products/id?=2', 'ad.theirs2.com'),
                ('https://shop.com/products/?id=2', 'yandex.ru'),
                ('https://shop.com/products/id?=2', 'referal.ours.com'),
                ('https://shop.com/products/id?=2', 'ad.ours.com'),
                ('https://shop.com/checkout', 'shop.com')
            ],
            'user4': [
                ('https://shop.com/products/id?=2', 'ad.ours.com'),
                ('https://shop.com/checkout', 'shop.com'),
                ('https://shop.com/products/id?=2', 'referal.theirs2.com'),
                ('https://shop.com/products/id?=2', 'ad.ours.com'),
                ('https://shop.com/checkout', 'shop.com')
            ]
        }

        self.assertEqual(main(user_activity_example), ['user2', 'user3', 'user4', 'user4'])

    def test_parse_log(self):
        logs_example = {"logs": [
            {
                "client_id": "user1",
                "User-Agent": "Firefox 59",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/products/id?=2",
                "date": "2018-04-04T08:59:16.222000Z"
            },
            {
                "client_id": "user2",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
                "date": "2018-05-23T18:59:13.286000Z"
            },
            {
                "client_id": "user2",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-05-23T18:59:20.119000Z"
            }
        ]}

        wanted_result = {
            'user1': [('https://shop.com/checkout', 'shop.com')],
            'user2': [('https://shop.com/', 'referal.ours.com'), ('https://shop.com/products/id?=10', 'shop.com')]
        }

        self.assertEqual(parse_log(logs_example), wanted_result)


if __name__ == '__main__':
    unittest.main()
