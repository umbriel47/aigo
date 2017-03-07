# encoding: utf-8

__all__ = ['settings']

class SingletonMixin(object):
    """Globally hold one instance class

    Usage:
    >>> class SpecObject(SingletonMixin):
    ...     pass

    >>> ins = SpecObject.instance()
    """
    @classmethod
    def instance(cls, *args, **kwgs):
        """Will be the only instance"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwgs)
        return cls._instance

class Settings(dict, SingletonMixin):
    """
    Philosophy was borrowed from django.conf.Settings

    As there are just few necessary values involved by tornado.options.options,
    (in httpclient and testing), and options.define is complicate and not convenient to use,
    Settings is created to replace tornado.options.options.

    by import torext module, a Settings object will be instanced and stored globally,
    then it can be involved in any place like this:
    >>> import torext
    >>> print torext.settings
    or
    >>> from torext import settings
    >>> print settings

    getting value from settings is like from a normal dict:
    >>> settings['DEBUG']
    True
    >>> settings.get('PORT')
    8000
    >>> settings.get('WTF', None)
    None

    notice that you can use lower case word to get or set the value:
    >>> settings['debug'] is settings.get('DEBUG')
    True
    >>> settings['port'] = 8765
    >>> settings['PORT']
    8765

    """
    def __init__(self):
        import base

        for i in dir(base):
            if not i.startswith('_'):
                self[i] = getattr(base, i)

        self._module = None

    def __getitem__(self, key):
        try:
            return super(Settings, self).__getitem__(key)
        except KeyError:
            try:
                return super(Settings, self).__getitem__(key.upper())
            except KeyError:
                #raise SettingsError(
                    #'Key "%s" is not defined in settings' % key
                #)
                pass

    def __setitem__(self, key, value):
        for i in key:
            if i != i.upper():
                #raise SettingsError(
                    #'Key "%s" is not allowed, you should always define'
                #                    ' UPPER CASE VARIABLE as setting' % key)
                pass
        super(Settings, self).__setitem__(key.upper(), value)

    def __str__(self):
        return '<Settings. %s >' % dict(self)

settings = Settings.instance()
