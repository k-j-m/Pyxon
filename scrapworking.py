import inspect

class Car(object):
    def __init__(self, make, model, year=2005):
        print "Making car!"
        self.make = make
        self.model = model
        self.year = year

    @classmethod
    def fromJson(cls, data):
        print cls.__init__.func_code
        args, varargs, keywords, defaults = inspect.getargspec(cls.__init__)

        print 'args:',args
        print 'varargs:',varargs
        print 'keywords:',keywords
        print 'defaults:',defaults

        nodefaults = args[1:-len(defaults)]
        defaulteds = zip(args[-len(defaults):], defaults)

        initargs = {}
        for arg in nodefaults:
            initargs[arg] = data[arg]

        for darg,default in defaulteds:
            initargs[darg] = data.get(darg,default)

        return cls(**initargs)
        
def test_name(some_string):
    def tester(**kwargs):
        pass
    try:
        tester(**{some_string:None})
        return True
    except:
        return False
