from django.db import models
from django.core.urlresolvers import reverse


__all__ = ('UrlModelMixin', 'UrlModel', 'CrudUrlModelMixin', 'CrudUrlModel')


class UrlModelMixin(object):

    slug_kwarg_name = None
    slug_field_name = None
    action_url_formatter = lambda model, action: '%s-%s' % (model, action)

    # this signature will override action_url_formatter
    # @classmethod
    # def format_action(cls, modelname, action):
    #     pass

    @classmethod
    def get_action_url_formatter(cls, action):
        if hasattr(cls, 'format_action'):
            return self.format_action(cls._meta.model_name, action)
        elif cls.action_url_formatter:
            return cls.action_url_formatter(cls._meta.model_name, action)

    @classmethod
    def get_class_url(cls, url_name, *args, **kwargs):
        url = reverse(url_name, args=args, kwargs=kwargs)
        return url

    @classmethod
    def get_class_action_url(cls, action, *args, **kwargs):
        url_name = cls.get_action_url_formatter(action)
        return cls.get_class_url(url_name, *args, **kwargs)

    def get_instance_url(self, url_name, *args, **kwargs):
        slug_kwarg = self.slug_kwarg_name or 'pk'
        slug_field = self.slug_field_name or 'pk'
        kwargs[slug_kwarg] = getattr(self, slug_field)
        url = reverse(url_name, args=args, kwargs=kwargs)
        return url

    def get_instance_action_url(self, action, *args, **kwargs):
        url_name = self.get_action_url_formatter(action)
        return self.get_instance_url(action, *args, **kwargs)


class UrlModel(UrlModelMixin, models.Model):
    """
    A class for any basic model that will only implement the UrlModelMixin.
    """


class CrudUrlModelMixin(UrlModelMixin):
    """
    Provides implementation for a non-lazy evaluation of a five 'action' URLs:
    - list (classmethod)
    - search(classmethod)
    - create (classmethod)
    - detail (instance method)
    - update (instance method)
    - delete (instance method)
    """

    def get_absolute_url(self):
        """
        Returns the URL for the detail view assuming that it does not receive
        any other arguments or keywords. The `detail_url` could be overriden
        to make this also work.
        """
        return self.detail_url()
    
    @classmethod
    def list_url(cls, *args, **kwargs):
        return cls.get_class_action_url('list', *args, **kwargs)

    @classmethod
    def search_url(cls, *args, **kwargs):
        return cls.get_class_action_url('search', *args, **kwargs)

    @classmethod
    def create_url(cls, *args, **kwargs):
        return cls.get_class_action_url('create', *args, **kwargs)

    def detail_url(self, *args, **kwargs):
        return self.get_instance_action_url('detail', *args, **kwargs)

    def update_url(self, *args, **kwargs):
        return self.get_instance_action_url('update', *args, **kwargs)

    def delete_url(self, *args, **kwargs):
        return self.get_instance_action_url('delete', *args, **kwargs)

class CrudUrlModel(CrudUrlModelMixin, models.Model):
    """
    This class should be enough for most applications. But you might want
    evaluation of urls to be lazy. Consider using `LazyCrudUrlModel`.
    """
