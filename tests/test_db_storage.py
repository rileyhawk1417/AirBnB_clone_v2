import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
from os import getenv


class TestDBStorage(unittest.TestCase):
    """ Test cases for DBStorage class """

    engine = None

    @classmethod
    def setUpClass(cls):
        """ Set up the test environment """
        user = getenv('HBNB_MYSQL_USER', 'default_user')
        password = getenv('HBNB_MYSQL_PWD', 'default_password')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        database = getenv('HBNB_MYSQL_DB', 'test_db')
        # Define the MySQL connection URL using the retrieved values
        mysql_url = f"mysql://{user}:{password}@{host}/{database}"
        # Create the SQLAlchemy Engine
        cls.engine = create_engine(mysql_url, pool_pre_ping=True)
        Base.metadata.create_all(cls.engine)
        # Create a session to use in the tests
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """ Set up a new session for each test """
        self.session = self.Session()
        storage.__session = self.session

    def tearDown(self):
        """ Remove current session after each test """
        self.session.close()

    def test_all(self):
        """ Test the all method """
        # Add test data to the database
        state = State(name="California")
        city = City(name="Los Angeles", state=state)
        user = User(email="test@example.com", password="password")
        place = Place(name="Cozy Cabin", city=city, user=user)
        amenity = Amenity(name="WiFi")
        review = Review(text="Great place", place=place, user=user)
        self.session.add_all([state, city, user, place, amenity, review])
        self.session.commit()

        # Call the all method and check if the objects are in the result
        all_objects = storage.all()
        self.assertIn("State.{}".format(state.id), all_objects)
        self.assertIn("City.{}".format(city.id), all_objects)
        self.assertIn("User.{}".format(user.id), all_objects)
        self.assertIn("Place.{}".format(place.id), all_objects)
        self.assertIn("Amenity.{}".format(amenity.id), all_objects)
        self.assertIn("Review.{}".format(review.id), all_objects)

    def test_new(self):
        """ Test the new method """
        # Create a new State instance and add it using new
        state = State(name="New York")
        storage.new(state)
        self.assertIn("State.{}".format(state.id), storage.all())

    def test_save(self):
        """ Test the save method """
        # Create a new State instance, add it, and check if it's saved
        state = State(name="Texas")
        storage.new(state)
        storage.save()
        all_objects = storage.all()
        self.assertIn("State.{}".format(state.id), all_objects)

    def test_delete(self):
        """ Test the delete method """
        # Create a new State instance, add it, delete it, and check if it's removed
        state = State(name="Florida")
        storage.new(state)
        storage.save()
        all_objects = storage.all()
        self.assertIn("State.{}".format(state.id), all_objects)
        storage.delete(state)
        storage.save()
        all_objects = storage.all()
        self.assertNotIn("State.{}".format(state.id), all_objects)

    def test_reload(self):
        """ Test the reload method """
        # Create a new State instance, add it, save it, then reload and check if it's still there
        state = State(name="Illinois")
        storage.new(state)
        storage.save()
        all_objects_before_reload = storage.all()
        storage.reload()
        all_objects_after_reload = storage.all()
        self.assertEqual(all_objects_before_reload, all_objects_after_reload)


if __name__ == '__main__':
    unittest.main()
