# classtrees.py
"""
Climb inheritance trees using namespace links.
Displaying higher superclasses with indentation
"""
def classtree(cls, indent):
    """
    Display class tree with specified indentation
    """
    print("." * indent + cls.__name__) # print class name
    for supercls in cls.__bases__: # recur to all superclasses
        classtree(supercls, indent + 3) # May visit super > once

def instancetree(inst):
    """
    Display class tree of an instance
    """
    print('Tree of %s' % inst) # show instance
    classtree(inst.__class__, 3) # climb to its class

def selftest():
    """
    Unit test
    """
    class A: pass
    class B(A): pass
    class C(A): pass
    class D(B,C): pass
    class E: pass
    class F(D,E): pass
    instancetree(B())
    instancetree(F())

if __name__ == '__main__': selftest()
