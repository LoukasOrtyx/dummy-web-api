from mongoengine import *

class User(Document):
    name = StringField()
    email = StringField()
    password = StringField()
    def to_json(self):
        return {"id": str(self.id),
                "name": self.name,
                "email": self.email,
                "password": self.password}