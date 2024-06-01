from datetime import datetime, timezone

from peewee import *

database = DatabaseProxy()  # use a proxy object, as we will init real db client inside web.py


class BaseModel(Model):
    class Meta:
        database = database


class Config(BaseModel):

    id = BigAutoField()
    key = CharField(unique=True)
    value = TextField()
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "config"


class Announce(BaseModel):

    id = BigAutoField()
    destination_hash = CharField(unique=True)  # unique destination hash that was announced
    aspect = TextField(index=True)  # aspect is not included in announce, but we want to filter saved announces by aspect
    identity_hash = CharField(index=True)  # identity hash that announced the destination
    identity_public_key = CharField()  # base64 encoded public key, incase we want to recreate the identity manually
    app_data = TextField(null=True)  # base64 encoded app data bytes

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "announces"


class LxmfMessage(BaseModel):

    id = BigAutoField()
    hash = CharField(unique=True)  # unique lxmf message hash
    source_hash = CharField(index=True)
    destination_hash = CharField(index=True)
    state = CharField()  # state is converted from internal int to a human friendly string
    progress = FloatField()  # progress is converted from internal float 0.00-1.00 to float between 0.00/100 (2 decimal places)
    is_incoming = BooleanField()  # if true, we should ignore state, it's set to draft by default on incoming messages
    title = TextField()
    content = TextField()
    fields = TextField()  # json string
    timestamp = FloatField()  # timestamp of when the message was originally created (before ever being sent)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "lxmf_messages"


class LxmfConversationReadState(BaseModel):

    id = BigAutoField()
    destination_hash = CharField(unique=True)  # unique destination hash
    last_read_at = DateTimeField()

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "lxmf_conversation_read_state"
