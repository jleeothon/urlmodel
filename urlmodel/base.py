from django.core.urlresolvers import reverse


__all__ = ('UrlModel', 'CrudUrlModel', 'ListUrlModel')


def format_action(model, action):
    return '%s-%s' % (model, action)


class UrlModel(object):

    slug_kwarg_name = None
    slug_field_name = None
    action_url_formatter = format_action

    @classmethod
    def format_action(cls, action):
        return cls.action_url_formatter(cls._meta.model_name, action)

    @classmethod
    def get_class_url(cls, url_name, *args, **kwargs):
        url = reverse(url_name, args=args, kwargs=kwargs)
        return url

    @classmethod
    def get_class_action_url(cls, action, *args, **kwargs):
        url_name = cls.format_action(action)
        return cls.get_class_url(url_name, *args, **kwargs)

    def get_instance_url(self, url_name, *args, **kwargs):
        slug_kwarg = self.slug_kwarg_name or 'pk'
        slug_field = self.slug_field_name or 'pk'
        kwargs[slug_kwarg] = getattr(self, slug_field)
        url = reverse(url_name, args=args, kwargs=kwargs)
        return url

    def get_instance_action_url(self, action, *args, **kwargs):
        url_name = self.format_action(action)
        return self.get_instance_url(url_name, *args, **kwargs)


class ListUrlModel(UrlModel):

    @classmethod
    def list_url(cls, *args, **kwargs):
        return cls.get_class_action_url('list', *args, **kwargs)


class CrudUrlModel(UrlModel):
    """
    Provides implementation for five 'action' URLs:
    - create (classmethod)
    - detail (instance method)
    - update (instance method)
    - delete (instance method)
    """

    def get_absolute_url(self):
        """
        Defaults to `detail_url`.
        """
        return self.detail_url()

    @classmethod
    def create_url(cls, *args, **kwargs):
        return cls.get_class_action_url('create', *args, **kwargs)

    def detail_url(self, *args, **kwargs):
        return self.get_instance_action_url('detail', *args, **kwargs)

    def update_url(self, *args, **kwargs):
        return self.get_instance_action_url('update', *args, **kwargs)

    def delete_url(self, *args, **kwargs):
        return self.get_instance_action_url('delete', *args, **kwargs)
