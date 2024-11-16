from django.db import models
from django.apps import apps

def create_model(name, fields):
    class Meta:
        app_label = 'my_app'

    attrs = {'__module__': 'my_app.models', 'Meta': Meta}
    attrs.update(fields)
    new_model = type(name, (models.Model,), attrs)
    models.Model.add_to_class(name, new_model)
    return new_model


def create_model_with_relationships(name, fields, relationships):
    class Meta:
        app_label = 'my_app'

    attrs = {
        '__module__': 'my_app.models',
        'Meta': Meta,
    }
    for field_name, field_type in fields.items():
        if field_type == 'ForeignKey':
            related_model = relationships.get(field_name)
            attrs[field_name] = models.ForeignKey(
                related_model, on_delete=models.CASCADE, null=True, blank=True
            )
        elif field_type == 'OneToOneField':
            related_model = relationships.get(field_name)
            attrs[field_name] = models.OneToOneField(
                related_model, on_delete=models.CASCADE, null=True, blank=True
            )
        elif field_type == 'ManyToManyField':
            related_model = relationships.get(field_name)
            attrs[field_name] = models.ManyToManyField(related_model, blank=True)
        else:
            attrs[field_name] = models.CharField(max_length=255)

    new_model = type(name, (models.Model,), attrs)
    models.Model.add_to_class(name, new_model)
    return new_model