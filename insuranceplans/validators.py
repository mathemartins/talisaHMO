# In your app's validators.py:
#
# def validate_file_extension(value):
#     import os
#     from django.core.exceptions import ValidationError
#     ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
#     valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
#     if not ext.lower() in valid_extensions:
#         raise ValidationError('Unsupported file extension.')
#
# Then in your models.py:
#
# from .validators import validate_file_extension
#
# ... and use the validator for your form field:
#
# class Document(models.Model):
#     file = models.FileField(upload_to="documents/%Y/%m/%d", validators=[validate_file_extension])
