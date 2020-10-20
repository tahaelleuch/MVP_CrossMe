#!/usr/bin/python3
from models.follow import Follow
from models.user import User

from models import storage
storage.reload()

a = Follow()
b = a.follower_list("18acb066-6860-47b2-b038-d1ef8f4c7d28")
for i in b:
    print()