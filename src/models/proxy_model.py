from peewee import Model, CharField, IntegerField,TextField,BooleanField,BlobField
import time
import config
from src.models import BaseModel,db
from src.customid import CustomID

class PROXY_STATUS:
    VALID = 0
    INVALID = 1
    UNCHEKCED = 2

    PROXY_PROTOCOL_TEXT = [
        (VALID, "VALID"),
        (INVALID, "INVALID"),
        (UNCHEKCED, "UNCHEKCED"),
    ]
    
    
class PROXY_PROTOCOL:
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    SOCKS5 = 'SOCKS5'

    PROXY_PROTOCOL_TEXT = [
        (HTTP, "HTTP"),
        (HTTPS, "HTTPS"),
        (SOCKS5, "SOCKS5"),
    ]

class PROXY_PROVIDER_TYPE:
    CUSTOM =0
    BRIGHT_DATA = 1
    IP_FOXY = 2
    IP_IDEA = 3
    OXYLABS = 4
    KOOKEEY = 5
    IPIP_GO = 6
    IPFLY = 7
    NETNUT = 8
    PROXY_302 = 9
    IP007 = 10
    LUNA_PROXY = 11
    S5_PROXY = 12
    PIA_S5_PROXY = 13

    PROXY_PROVIDER_TYPE_TEXT = [
        (CUSTOM, "custom"),
        (BRIGHT_DATA, "BrightData"),
        (IP_FOXY, "IPFoxy"),
        (IP_IDEA, "IPIDEA"),
        (OXYLABS, "Oxylabs"),
        (KOOKEEY, "kookeey"),
        (IPIP_GO, "ipipgo"),
        (IPFLY, "IPFLY"),
        (NETNUT, "netnut"),
        (PROXY_302, "Proxy302"),
        (IP007, "IP007"),
        (LUNA_PROXY, "LunaProxy"),
        (S5_PROXY, "922S5 Proxy"),
        (PIA_S5_PROXY, "PIA S5 Proxy"),
    ]


class ProxyModel(BaseModel):
    id = IntegerField(primary_key=True)    
    inserted_at = IntegerField(null=True)    
    # Proxy Protocol (HTTP/HTTPS/SOCKS5)
    proxy_protocol = IntegerField(choices=PROXY_PROTOCOL)
    
    # Proxy Type
    proxy_provider_type = IntegerField(default=PROXY_PROVIDER_TYPE.CUSTOM,null=True)
    
    # Proxy Host
    proxy_host = CharField()
    
    # Proxy Port
    proxy_port = IntegerField()
    
    # Proxy Username
    proxy_username = CharField(null=True)
    
    # Proxy Password
    proxy_password = CharField(null=True)
    
    # IP Address
    ip_address = CharField(null=True)
    
    # Country/Region
    country = CharField(null=True)
    
    # State/Province
    state = CharField(null=True)
    
    # City
    city = CharField(null=True)
    

    
    tags = TextField(null=True)
    status = IntegerField(default=PROXY_STATUS.UNCHEKCED)

    # Proxy network
    proxy_validate_network_type = CharField(null=True)
    proxy_validate_server = TextField(null=True)
    #json保存多个核对结果 核对服务器url：核对结果json字符串
    proxy_validate_results = TextField(null=True)
    is_deleted = BooleanField(default=False)  # Add a field to flag if video is deleted
    unique_hash = TextField(index=True, unique=True, null=True, default=None)  # Add this line

    # class Meta:
    #     db_table = db


    # Create (Insert) Proxy
    def add_proxy(proxy_data):

        
        unique_hash = config.generate_unique_hash(proxy_data)

        # Check if a proxy with the same unique hash already exists
        existing_proxy = ProxyModel.select().where(ProxyModel.unique_hash == unique_hash).first()

        if existing_proxy is None:    
            proxy = ProxyModel(**proxy_data)
            proxy.insert_date = int(time.time())  # Update insert_date
            proxy.unique_hash=unique_hash
            # proxy.id = CustomID().to_bin()

            proxy.save()

            return True
        else:
            return False
    # Read (Select) Proxy by ID
    def get_proxy_by_id(proxy_id):
        try:
            proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            return proxy
        except ProxyModel.DoesNotExist:
            return None

    # Update Proxy by ID
    def update_proxy(proxy_id, **kwargs):
        try:
            proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            for key, value in kwargs.items():
                setattr(proxy, key, value)
            proxy.save()
            return proxy
        except ProxyModel.DoesNotExist:
            return None

    # Delete (Soft Delete) Proxy by ID
    def delete_proxy(proxy_id):
        try:
            proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            proxy.is_deleted = True
            proxy.save()
            return True
        except ProxyModel.DoesNotExist:
            return False
    # Assuming you have a list of proxy data named proxy_list
    def bulk_add_proxies(proxy_list):
        inserted_proxies = []
        for proxy_data in proxy_list:
            # Calculate unique hash for the proxy
            unique_hash = config.generate_unique_hash(proxy_data)

            # Check if a proxy with the same unique hash already exists
            existing_proxy = ProxyModel.select().where(ProxyModel.unique_hash == unique_hash).first()

            if existing_proxy is None:
                # Create a new proxy
                proxy = ProxyModel(**proxy_data, unique_hash=unique_hash)
                proxy.inserted_at = int(time.time())
                proxy.save()
                inserted_proxies.append(proxy)

        return inserted_proxies


    def filter_proxies(country=None, state=None, city=None, tags=None, status=None, network_type=None):
        query = ProxyModel.select()
        print('===',country,state,city,tags,status,network_type)

        for person in ProxyModel.select():
            print(person)

        if country is not None:
            query = query.where(ProxyModel.country == country)

        if state is not None:
            query = query.where(ProxyModel.state == state)

        if city is not None:
            query = query.where(ProxyModel.city == city)

        if tags is not None:
            query = query.where(ProxyModel.tags == tags)

        if status is not None:
            query = query.where(ProxyModel.status == status)

        if network_type is not None:
            query = query.where(ProxyModel.proxy_validate_network_type == network_type)
        try:
            result = list(query)
            
        except ProxyModel.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result


