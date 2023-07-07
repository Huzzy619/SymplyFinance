from django.db.models.fields import AutoFieldMeta, UUIDField, AutoFieldMixin, AutoField

from django.db.models import BigAutoField

class UUIDField(AutoField):
    def get_internal_type(self):
        return "UUIDField"

    def rel_db_type(self, connection):
        return UUIDField().db_type(connection=connection)


# , metaclass=AutoFieldMeta