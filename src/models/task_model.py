from peewee import TextField, BlobField, BooleanField,IntegerField,ForeignKeyField
from src.models import BaseModel,db
import config
import time
from src.customid import CustomID
from src.models.youtube_video_model import YoutubeVideoModel
from src.models.platform_model import PLATFORM_TYPE
from src.models.upload_setting_model import UploadSettingModel
from src.models.account_model import AccountModel
class TASK_STATUS:
    PENDING = 0
    FAILURE = 1
    SUCCESS=2
    PLATFORM_TYPE_TEXT = [
        (PENDING, "pending"),
        (FAILURE, "failure"),
        (SUCCESS, "success"),
    ]


class TaskModel(BaseModel):
    id = BlobField(primary_key=True)    
    type= IntegerField(default=PLATFORM_TYPE.YOUTUBE)
    status = IntegerField(default=TASK_STATUS.PENDING)
    prorioty= BooleanField(default=False) 
    video = ForeignKeyField(YoutubeVideoModel, backref='videos')
    # video upload use which proxy
    proxy = TextField(null=True)
    # video upload to
    username = TextField(null=True)

    setting = ForeignKeyField(UploadSettingModel, backref='settings')

    inserted_at = IntegerField()
    uploaded_at = IntegerField(null=True)
    @classmethod

    def add_task(cls,task_data,taskvideo,tasksetting):


        task = TaskModel(**task_data)
        task.inserted_at = int(time.time())  # Update insert_date
        # task.id = CustomID().to_bin()
        task.id = CustomID().to_bin()
        task.video=taskvideo
        task.setting=tasksetting
        task.save(force_insert=True) 
        
        print('task add ok',task.id)
        return task
        
            # for user in TaskModel.select():
            #     print(user.name)
            # return True
    @classmethod

    def get_task_by_id(cls, id):
        return cls.get_or_none(cls.id == id)
    
    @classmethod
    def update_task(cls, id,videodata=None,settingdata=None,accountdata=None,taskdata=None,**kwargs):
        try:
            task = cls.get(cls.id == id)
            if taskdata:
                task = TaskModel(**taskdata)
                if accountdata:
                    account=AccountModel(**accountdata)
                    account.inserted_at = int(time.time())  # Update insert_date

                    account.save()
                if settingdata:
                    setting=UploadSettingModel(**settingdata)
                    setting.inserted_at = int(time.time())  # Update insert_date

                    setting.save()
                if videodata:
                    video=YoutubeVideoModel(**videodata)
                    video.inserted_at = int(time.time())  # Update insert_date

                    video.save()

            else:            
            
                for key, value in kwargs.items():
                    setattr(task, key, value)
            task.inserted_at = int(time.time())  # Update insert_date

            task.save() 
            return task
        except cls.DoesNotExist:
            return None
    @classmethod

    def delete_task( cls,id):
        try:
            task = cls.get(cls.id == id)
            task.delete_instance()
            return True
        except cls.DoesNotExist:
            return False
    @classmethod


    @classmethod

    def filter_tasks(cls, status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title=None,video_id=None,username=None,pageno=None,pagecount=None,start=None,end=None,data=None):
            query=TaskModel.select()
            counts=query.count()
            query = (TaskModel
                    .select(TaskModel, YoutubeVideoModel, UploadSettingModel, AccountModel)
                    .join(YoutubeVideoModel)  # Join favorite -> user (owner of favorite).
                    .switch(TaskModel)
                    .join(UploadSettingModel)  # Join favorite -> tweet
                    .join(AccountModel))   # Join tweet -> user        

            if video_title is not None :
                query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.

                query = (query
                # .join(YoutubeVideoModel,on=(TaskModel.video_id == YoutubeVideoModel.id))
                .where(YoutubeVideoModel.video_title.regexp(video_title))

                )
                query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.


            if video_id is not None:
                query = query.join(YoutubeVideoModel,on=(TaskModel.video == YoutubeVideoModel.id)).where(YoutubeVideoModel.youtube_video_id == video_id)
                query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.

            # 如果存在account 相关的查询参数，先找到对应的 setting id集合
            if username is not None:
                query = query.join(UploadSettingModel,on=(TaskModel.setting == UploadSettingModel.id)).join(AccountModel,on=(UploadSettingModel.account == AccountModel.id)).where(AccountModel.username.regexp(username))

                query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.


            try:
                print('=====',len(list(query)))
                print(f"{pageno}")
                print(f"{pagecount}")

                counts=len(list(query))
                if pageno:
                    
                    query=query.paginate(pageno, pagecount)
                    print(f'this is the {pageno} {list(query)}')

                elif type(start)==int and type(start)==int and start<end:
                    startpage=start/pagecount
                    endpage=end/pagecount
                    query=query.paginate(startpage, pagecount)

                print('==current pagi===',len(list(query)))

                return list(query),counts

                
            except cls.DoesNotExist:
                query = None  # Set a default value or perform any other action

            return query
