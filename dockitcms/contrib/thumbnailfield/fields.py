from schemamaker.fields import BaseFieldSchema, BaseField
from schemamaker.schema_specifications import default_schema_specification as registry
from schemamaker.utils import prep_for_kwargs

import dockit

import properties

IMAGE_FORMATS = [('JPEG', '.jpg'),
                 ('PNG', '.png'),]

CROP_CHOICES = [('smart', 'Smart'),
                ('scale', 'Scale'),]

class ThumbnailFieldEntrySchema(dockit.Schema):
    format = dockit.CharField(blank=True, null=True, choices=IMAGE_FORMATS)
    quality = dockit.IntegerField(blank=True, null=True)
    width = dockit.IntegerField(blank=True, null=True)
    height = dockit.IntegerField(blank=True, null=True)
    upscale = dockit.BooleanField(default=False, help_text='Upsize the image if it doesn\'t match the width and height')
    crop = dockit.CharField(blank=True, null=True, choices=CROP_CHOICES)
    autocrop = dockit.BooleanField(default=False, help_text='Remove white space from around the image')

class ThumbnailFieldSchema(BaseFieldSchema):
    thumbnails = dockit.ListField(dockit.SchemaField(ThumbnailFieldEntrySchema))

class ThumbnailField(BaseField):
    schema = ThumbnailFieldSchema
    field = properties.ThumbnailField
    
    def create_field(self, data):
        kwargs = prep_for_kwargs(data)
        kwargs.pop('field_type', None)
        kwargs.pop('name', None)
        if kwargs.get('verbose_name', None) == '':
            del kwargs['verbose_name']
        thumbnails = kwargs.pop('thumbnails', [])
        for thumb in thumbnails:
            resize = {}
            for key in ['width', 'height', 'crop', 'upscale']:
                if key in thumb:
                    resize[key] = thumb.pop(key)
            if resize:
                thumb['resize'] = resize
        kwargs['config'] = {'thumbnails':thumbnails}
        return self.field(**kwargs)

registry.register_field('ThumbnailField', ThumbnailField)

