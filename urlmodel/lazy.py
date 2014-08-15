from django.db import models

from .base import UrlModelMixin


__all__ = (
    'LazyUrlModelMixin', 
    'LazyUrlModel', 
    'LazyCrudUrlModelMixin', 
    'LazyCrudUrlModel',
)


class LazyUrlModelMixin(UrlModelMixin):

    @classmethod
    def get_class_url_lazy(cls, url_name, attr_name, *args, **kwargs):
        """
        `attr_name` should be a valid Python identifier; preferrably, make it
        similar to `url_name` and start with an underscore.
        """
        if not hasattr(cls, attr_name):
            url = cls.get_class_url(url_name, *args, **kwargs)
            setattr(cls, attr_name, url)
        return getattr(cls, attr_name)

    @classmethod
    def get_class_action_url_lazy(cls, action, *args, **kwargs):
        """
        `action` needs to be a valid Python identifier.
        """
        url_name = cls.get_action_url_formatter(action)
        attr_name = '_%s_url' % action
        return cls.get_class_url_lazy(url_name, attr_name, *args, **kwargs)

    def get_instance_url_lazy(self, url_name, attr_name, *args, **kwargs):
        """
        `attr_name` should be a valid Python identifier; preferrably, make it
        similar to `url_name` and start with an underscore.
        """
        if not hasattr(self, attr_name):
            url = self.get_instance_url(url_name, *args, **kwargs)
            setattr(self, attr_name, url)
        return getattr(self, attr_name)

    def get_instance_action_url_lazy(self, action, *args, **kwargs):
        """
        `action` needs to be a valid Python identifier.
        """
        url_name = self.get_action_url_formatter(action)
        attr_name = '_%s_url' % action
        return self.get_instance_url_lazy(url_name, attr_name, *args, **kwargs)


class LazyUrlModel(LazyUrlModelMixin, models.Model):
    pass


class LazyCrudUrlModelMixin(LazyUrlModelMixin):
    """
    All default provided methods are lazily evaluated.
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
        return cls.get_class_action_url_lazy('list', *args, **kwargs)

    @classmethod
    def search_url(cls, *args, **kwargs):
        return cls.get_class_action_url_lazy('search', *args, **kwargs)

    @classmethod
    def create_url(cls, *args, **kwargs):
        return cls.get_class_action_url_lazy('create', *args, **kwargs)

    def detail_url(self, *args, **kwargs):
        return self.get_instance_action_url_lazy('detail', *args, **kwargs)

    def update_url(self, *args, **kwargs):
        return self.get_instance_action_url_lazy('update', *args, **kwargs)

    def delete_url(self, *args, **kwargs):
        return self.get_instance_action_url_lazy('delete', *args, **kwargs)


class LazyCrudUrlModel(LazyCrudUrlModelMixin, models.Model):
    pass
