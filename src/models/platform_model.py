from peewee import Model, CharField, TextField,IntegerField,BlobField
from src.models import BaseModel,db
import config
import time
from src.customid import CustomID

class PLATFORM_TYPE:
    YOUTUBE = 1
    TIKTOK = 2
    INSTAGRAM=3
    TWITTER=4
    PLATFORM_TYPE_TEXT = [
        (YOUTUBE, "youtube"),
        (TIKTOK, "tiktok"),
        (INSTAGRAM, "instagram"),
        (TWITTER, "twitter"),

    ]

class PlatformModel(BaseModel):
    id = IntegerField(primary_key=True)    
    name = IntegerField(null=True)
    type= IntegerField(default=PLATFORM_TYPE.YOUTUBE)
    server = TextField(null=True)
    inserted_at = IntegerField(null=True)

    def add_platform(cls,platform_data):

        # Check if an platform with the same unique hash already exists
        existing_platform = cls.get_or_none(cls.type == platform_data['type'])

        if existing_platform is None:
            platform = PlatformModel(**platform_data)
            platform.insert_date = int(time.time())  # Update insert_date
            # platform.id = CustomID().to_bin()

            platform.save()
            print('plafrom add ok',platform.id)
            
            for user in PlatformModel.select():
                print(user.name)
            return True
            
        else:
            return False

    def get_platform_by_id(cls, platform_id):
        return cls.get_or_none(cls.id == platform_id)

    def update_platform(cls, platform_id, **kwargs):
        try:
            platform = cls.get(cls.id == platform_id)
            for key, value in kwargs.items():
                setattr(platform, key, value)
            platform.save()
            return platform
        except cls.DoesNotExist:
            return None

    def delete_platform( cls,platform_id):
        try:
            platform = cls.get(cls.id == platform_id)
            platform.delete_instance()
            return True
        except cls.DoesNotExist:
            return False

    def filter_platforms(cls, name=None, ptype=None, server=None):
        query = cls.select()
        print('all platfroms are ',list(query))
        if name is not None:
            query = query.where(cls.platform == name)

        if server is not None:
            query = query.where(cls.server == server)

        if ptype is not None:
            query = query.where(cls.type == ptype)
            # # Assuming 'proxy_id' is the ID of the proxy you want to work with

            # proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            # associated_platform = proxy.platform  # This will fetch the associated Account

        try:
            result = list(query)
            
        except PlatformModel.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result
