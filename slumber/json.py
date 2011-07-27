from urlparse import urljoin


DATA_MAPPING = {
        'django.db.models.fields.AutoField': lambda m, i, fm, v: v,
        'django.db.models.fields.BooleanField': lambda m, i, fm, v: v,
        'django.db.models.fields.related.ForeignKey': lambda m, i, fm, v: v.pk if v else None,
    }


def to_json_data(model, instance, fieldname, fieldmeta):
    value = getattr(instance, fieldname)
    if fieldmeta['kind'] == 'object':
        return dict(display=unicode(value), data='/slumber/xxx')
    if DATA_MAPPING.has_key(fieldmeta['type']):
        return DATA_MAPPING[fieldmeta['type']](model, instance, fieldmeta, value)
    else:
        if value is None:
            return None
        else:
            return unicode(value)


def from_json_data(base_url, json):
    if json['kind'] == 'object':
        # It's a remote object
        from slumber.connector import InstanceConnector
        return InstanceConnector(
            urljoin(base_url, json['data']['data']),
            json['data']['display'])
    else:
        return json['data']
