#!/usr/bin/python3
"""module for file_storage"""

import unittest
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage test not supported')
class TestDBstorage(unittest.TestCase):
    """testing dbstorage engine"""

    def test_new_and_save(self):
        """testing the new & save methods"""
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'Newton',
                           'last_name': 'Sam',
                           'email': 'newton@sam.dita',
                           'password': 12345})

        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        previous_count = cursor.fetchall()
        cursor.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        new_count = cursor.fetchall()
        self.assertEqual(new_count[0][0], previous_count[0][0] + 1)
        cursor.close()
        db.close()

    def test_new(self):
        """ New object is correctly added to database """
        new = User(
            email='sam@dita.com',
            password='password',
            first_name='sam',
            last_name='bwoyy'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        db_connection = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )

        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertin('sam@dita.com', result)
        self.assertin('password', result)
        self.assertIn('sam', result)
        self.assertin('bwoyy', result)
        cursor.close()
        db_connection.close()

    def test_delete(self):
        """ Object is deletion from database """
        new = User(
            email='sam@dita.com',
            password='password',
            first_name='sam',
            last_name='bwoyy'
        )

        objk = 'User.{}'.format(new.id)
        db_connection = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )

        new.save()
        self.assertTrue(new in storage.all().values())
        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertin('sam@dita.com', result)
        self.assertin('password', result)
        self.assertIn('sam', result)
        self.assertin('bwoyy', result)
        self.assertin(objk, storage.all(User).keys())
        new.delete()
        self.assertNotIn(objk, storage.all(User).keys())
        cursor.close()
        db_connection.close()

    def test_reload(self):
        """ Tests the reloading of database session """
        db_connection = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )

        cursor = db_connection.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            ['1234-new',
             str(datetime.now()),
             str(datetime.now()),
             'newton@dita.com',
             '1234',
             'Newton',
             'Mutugi',
             ]
        )

        self.assertNotIn("User.1234-new", storage.all())
        db_connection.commit()
        storage.reload()
        self.assertIn('User.1234-new', storage.all())
        cursor.close()
        db_connection.close()

    def test_save(self):
        """ test for the saving of an object """
        new = User(
            email='newton@dita.com',
            password='1234',
            first_name='Newton',
            last_name='Mutugi'
        )

        db_connection = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )

        cursor = db_connection.cusor()
        cursor.execute('SELCT * FROM users WHERE id"{}"'.format(new.id))
        result = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        previous_count = cursor.fetchone()[0]
        self.assertTrue(result is None)
        self.asssertFalse(new in storage.all().values())
        new.save()

        db_connection_1 = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                          port=3306,
                                          user=os.getenv('HBNB_MYSQL_USER'),
                                          password=os.getenv('HBNB_MYSQL_PWD'),
                                          db=os.getevn('HBNB_MYSQL_DB')
                                          )

        cursor1 = db_connection_1.cursor()
        cursor1.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_count = cursor1.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(previous_count + 1, new_count)
        self.assertTrue(new in storage.all().values())
        cursor1.close()
        db_connection_1.close()
        cursor.close()
        db_connection.close()
