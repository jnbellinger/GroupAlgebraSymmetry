''' Special :  zero Elements '''
import sys
import copy
from Builder import Name
from Builder import Fraction
from Builder import Element
from Builder import Chain

class Zero:
    ''' Holds a collection of Names that are zero '''
    def __init__(self, klist):
        ''' Initialize given a List of Name '''
        if not isinstance(klist, list):
            print('Zero needs a list to initialize with')
            sys.exit(80)
        self.zerolist = []
        if len(klist) == 0:
            return  # init from empty gives empty, not a worry
        for entry in klist:
            if not isinstance(entry, Element.Element) and not isinstance(entry, Name.Name):
                print('Zero needs the initialization list to be Elements or Names')
                sys.exit(81)
            if isinstance(entry, Element.Element):
                kname = entry.name
            else:
                kname = entry
            if kname not in self.zerolist:
                self.zerolist.append(kname)
        self.zerolist.sort()
        #
    def add(self, other):
        ''' Add another Name or Element or set of the same to the list of zeros '''
        if (not isinstance(other, list) and 
                not isinstance(other, Chain.Chain) and
                not isinstance(other, Element.Element) and 
                not isinstance(other, Name.Name)):
            print('Zero wants Names or Elements or a list of them to add')
            sys.exit(82)
        if isinstance(other, list) or isinstance(other, Chain.Chain):
            if isinstance(other, list):
                templist = other
            else:
                templist = other.chainlist
            for entry in templist:
                if isinstance(entry, Element.Element):
                    klist = entry.name
                elif isinstance(entry, Name.Name):
                    klist = entry
                else:
                    print('Zero wants a list of Elements or Names')
                    sys.exit(81)
                if klist not in self.zerolist:
                    self.zerolist.append(klist)
        elif isinstance(other, Element.Element):
            kname = other.name
            if kname not in self.zerolist:
                self.zerolist.append(kname)
        else:  # isinstance(other, Name.Name)
            kname = other
            if kname not in self.zerolist:
                self.zerolist.append(kname)
        self.zerolist.sort()
    #
    def present(self, other):
        ''' Is the Name zero? '''
        if not isinstance(other, Name.Name) and not isinstance(other, Element.Element):
            print('Zero can only check Names or Elements ' + str(other))
            sys.exit(83)
        if isinstance(other, Element.Element):
            kname = other.name
        else:
            kname = other
        if kname in self.zerolist:
            return True
        return False
    #
    def count(self):
        ''' How many Names does this have? '''
        return len(self.zerolist)
    #
    def __str__(self):
        ''' Make a string of this '''
        self.zerolist.sort()
        base = ''
        for i in range(len(self.zerolist) - 1):
            base = base + str(self.zerolist[i]) + ','
        return base + str(self.zerolist[-1])
    def __repr__(self):
        return self.__str__()
    #
    def contents(self):
        ''' Return the contents as a new list of Names '''
        return copy.deepcopy(self.zerolist)
