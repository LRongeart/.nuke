import sys
import time
import functools
import warnings

from rpg.terminal import TerminalColor

__all__ = (
        'getFilePosition',
        'lineno',
        'deprecated',
        'cachedproperty',
        'memoize',
        'UsageError',
        'LogColors',
        'log',
        'logWarning',
        'logError',
        )

# ---------------------------------------------------------------------------

def getFilePosition(stacklevel=0):
    """
    Returns the filename and line number 
    
    derived from warnings.py
    """

    try:
        caller = sys._getframe(stacklevel+1)
    except ValueError:
        filename = sys.__dict__.get('__file__')
        lineno = 1
    else:
        filename = caller.f_code.co_filename
        lineno = caller.f_lineno

    if filename:
        fnl = filename.lower()
        if fnl.endswith(".pyc") or fnl.endswith(".pyo"):
            filename = filename[:-1]
    else:
        module = sys.__dict__.get('__name__', '<string>')
        if module == '__main__':
            filename = sys.argv[0]
        else:
            filename = module

    return (filename, lineno)
 

def lineno(stacklevel=0):
    """
    Returns the line number of the current position in a file

    derived from warnings.py
    """
    
    try:
        return sys._getframe(stacklevel+1).f_lineno
    except ValueError:
        return 1

# ---------------------------------------------------------------------------

def deprecated(obj=None, *, msg=None, name=None, doc=None):
    """
    A decorator to mark functions or classes as deprecated.

    When the function is called, a warning will be emitted.
    """
    if obj is None:
        return lambda actual_obj: deprecated(
            actual_obj, msg=msg, name=name, doc=doc
        )

    obj_name = name or getattr(obj, "__name__", str(obj))
    obj_doc = doc or getattr(obj, "__doc__", "")
    warn_msg = msg or f"Call to deprecated object: {obj_name}"

    @functools.wraps(obj)
    def wrapped(*args, **kwargs):
        warnings.warn(warn_msg, category=DeprecationWarning, stacklevel=2)
        return obj(*args, **kwargs)

    wrapped.__doc__ = obj_doc
    wrapped.__name__ = obj_name
    return wrapped

# ---------------------------------------------------------------------------

class cachedproperty(object):
    """
    a property-like method descriptor that creates a one time property. After
    the first call, the value will be cached in the instance.

    >>> class C(object):
    ...   def __init__(self):
    ...     self.counter = 0
    ...
    ...   def foo(self):
    ...     self.counter += 1
    ...     return self.counter
    ...   foo=cachedproperty(foo)
    >>> c=C()
    >>> c.foo
    1
    >>> c.foo
    1
    """

    def __init__(self, function, name=None, doc=None):
        """
        @param function: the function to cache the results from
        @param name: if set, uses this for the __name__ instead of the
            function.__name__
        @param doc: if set, uses this for the __doc__ instead of the
            function.__doc__
        """
        
        self.__dict__.update(function.__dict__)
        if doc is None:
            doc = function.__doc__
        self.__doc__ = doc
        
        if name is None:
            name = function.__name__
        self.__name__ = name

        # we need this after the update so that it's not overwritten
        self.__function = function


    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.__function(instance)
        setattr(instance, self.__name__, value)
        return value

# ---------------------------------------------------------------------------

def memoize(func=None, *, name=None, doc=None):
    """
    A decorator to cache function results based on arguments.
    Works with functions and instance methods.
    """

    if func is None:
        return lambda actual_func: memoize(actual_func, name=name, doc=doc)

    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        try:
            if args in cache:
                return cache[args]
        except TypeError:
            # Arguments are unhashable (e.g., lists, dicts), skip caching
            return func(*args)

        result = func(*args)
        cache[args] = result
        return result

    wrapper.__name__ = name or func.__name__
    wrapper.__doc__ = doc or func.__doc__
    return wrapper

# ---------------------------------------------------------------------------

class UsageError(Exception):
    """
    Helper exception to print out usage errors

    """
    
    def __init__(self, msg, errno=2):
        self.msg = msg
        self.errno = errno

    def __str__(self):
        return str(self.msg)
# aliased for backwards compatibility
Usage = deprecated(UsageError, \
        msg='Usage is deprecated. Please use UsageError',
        name='Usage')

# ---------------------------------------------------------------------------

LogColors = {
    'yellow': TerminalColor('yellow'),
    'red': TerminalColor('red'),
    'blue': TerminalColor('blue'),
    'white': TerminalColor('white'),
    'cyan': TerminalColor('cyan')
    }


def log(msg, outfile=None, color=None):
    """Appends a time stamp and '==>' to a string before printing
    to stdout."""

    if not outfile:
        outfile = sys.stdout

    if color and LogColors.has_key(color):
        terminalColor = LogColors[color]
        msg = terminalColor.colorStr(msg)

    try:
        print >> outfile, time.ctime() + " ==> " + msg
        outfile.flush()
    except (IOError, OSError) as msg:
        pass


def logWarning(msg):
    log('WARNING: ' + msg, color='yellow')


def logError(msg):
    log('ERROR: ' + msg, color='red') 
