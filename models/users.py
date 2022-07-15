from mongoengine import *

class Users(Document):
    name = StringField()
    email = StringField()
    password = StringField()
    def to_json(self):
        return {"id": str(self.id),
                "name": self.name,
                "email": self.email}