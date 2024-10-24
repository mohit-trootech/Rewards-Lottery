# Customized Model for Soft Delete Method
from django.db.models import Model
from django_extensions.db.models import ActivatorModel


class SoftDeleteActivatorModelAbstractModel(Model):
    """customized model for `Soft Delete` method & required `status` fields"""

    def soft_delete(self):
        """soft Delete object by making status false"""
        self.status = ActivatorModel.INACTIVE_STATUS
        self.save(update_fields=["status"])

    class Meta:
        abstract = True
