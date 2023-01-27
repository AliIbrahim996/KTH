from django.core.management.base import BaseCommand
from core.models import *
from rest_framework.authtoken.models import Token

""" Clear all data and creates Skills """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('seeding done!.')


def clear_data(self):
    """Deletes all the table data"""
    self.stdout.write("Delete instances")
    User.objects.all().delete()
    Chef.objects.all().delete()
    Category.objects.all().delete()
    Meal.objects.all().delete()
    Token.objects.all().delete()


users = [None] * 3


def create_user():

    id_ = [3, 4, 5]
    full_name_ = ["ali", "ahmad", "emma"]
    user_name_ = ["ali_a", "ahmad_a", "emma_a"]
    phone_number_ = ["+963990289109", "+963990289110", "+963990289111"]
    email_ = ["aa@ex.com", "ah@ex.com", "em@ex.com"]
    password_ = ["ASDF@#1234", "ASDF@#1234", "ASDF@#1234"]
    profile_img_ = ["images/profile/f1.jfif", "images/profile/f2.jfif", "images/profile/f3.jfif"]

    for i in range(3):
        user = User.objects.create(
            id=id_[i],
            full_name=full_name_[i],
            username=user_name_[i],
            phone_number=phone_number_[i],
            email=email_[i],
            password=password_[i],
            profile_img=profile_img_[i]
        )
        user.save()
        users[i] = user

    return "3 users created"


chefs = [None] * 3


def create_chef():
    id_ = [3, 4, 5]
    loc_lat_ = ["44.584111", "47.584111", "46.584111"]
    loc_lan_ = ["32.584111", "44.584111", "32.584111"]
    id_card_ = ["images/id1.jfif", "images/id2.png", "images/id3.jfif"]
    heart_number_ = [0, 5, 0]
    delivery_cost = [4, 5, 6]

    for i in range(3):
        chef = Chef.objects.create(
            id=id_[i],
            user=users[i],
            loc_lat=loc_lat_[i],
            loc_lan=loc_lan_[i],
            id_card=id_card_[i],
            heart_number=heart_number_[i],
            delivery_cost=delivery_cost[i],
        )
        chef.save()
        chefs[i] = chef

    return "3 chefs created"


categories = [None] * 3


def create_category():
    id_ = [2, 3, 4]
    name_ = ["meat", "sweets", "vegetable"]
    icon_ = ["images/category/ca1_W8woZVl.jfif", "images/category/ca2sw.jfif", "images/category/ca3veg.jfif"]

    for i in range(3):
        category = Category.objects.create(
            id=id_[i],
            name=name_[i],
            icon=icon_[i],
        )
        category.save()
        categories[i] = category

    return "3 category created"


def create_meal():
    id_ = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    chef_ = [chefs[0], chefs[0], chefs[1], chefs[2], chefs[1], chefs[2], chefs[0], chefs[1], chefs[2]]
    title_ = ["salad", "beef", "fried", "budha", "roasted veg", "chicken", "sweet 1", "sweet 2", "sweet 3"]
    price_ = [20.0, 65.0, 44.0, 25.0, 30.5, 44.0, 22.5, 30.0, 24.0]
    image_ = ["images/salad.jfif", "images/beef1.jfif", "images/fried_chicken.jfif", "images/vegetarian-green-curry-budha.webp", "images/roasted-vegetables.jpg", "images/meal2.jfif", "images/sweets1.jfif", "images/sweets2.jfif", "images/sweets3.jfif"]
    dishes_count_ = [2, 2, 5, 5, 7, 4, 4, 4, 4]
    category_ = [categories[2], categories[0], categories[0], categories[2], categories[2], categories[0], categories[1], categories[1], categories[1]]

    for i in range(9):
        meal = Meal.objects.create(
            id=id_[i],
            chef=chef_[i],
            title=title_[i],
            description="description not available",
            price=price_[i],
            image=image_[i],
            dishes_count=dishes_count_[i],
            category=category_[i]
        )
        meal.save()

    return "9 meals created"


def create_data(self):
    """Create new data"""
    self.stdout.write("Create instances")
    self.stdout.write(create_user())
    self.stdout.write(create_chef())
    self.stdout.write(create_category())
    self.stdout.write(create_meal())


def run_seed(self, mode):
    """ Seed database based on mode
    """
    # Clear data from tables
    clear_data(self)
    if mode == MODE_CLEAR:
        return

    create_data(self)



