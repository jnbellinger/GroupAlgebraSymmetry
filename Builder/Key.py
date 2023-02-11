''' Ordered list of Name(s) '''
import sys
import copy
from Builder import Name


class Key:
    ''' Class to simplify list[Name] and make sure it is ordered '''
    def __init__(self, klist):
        ''' Initialize from a list of Name '''
        if not isinstance(klist, list):
            print('Key needs a list to initialize with')
            sys.exit(60)
        if len(klist) <= 0:
            print('Key needs a non-empty list to initialize with')
            sys.exit(61)
        self.namelist = []
        for entry in klist:
            if not isinstance(entry, Name.Name):
                print('Key needs the initialization list to be Names')
                sys.exit(62)
            if len(self.namelist) != 0:
                if entry.size != self.namelist[0].size:
                    print('Please do not mix Names from different problems')
                    sys.exit(63)
            if entry not in self.namelist:
                self.namelist.append(entry)
        self.namelist.sort()

    #
    # Methods
    def count(self):
        ''' Trivial, just the length '''
        return len(self.namelist)
    #
    def __eq__(self, other):
        ''' Only meaningful against another Key '''
        if not isinstance(other, Key):
            return False
        if self.count() != other.count():
            return False
        for i in range(len(self.namelist)):
            if self.namelist[i] != other.namelist[i]:
                return False
        return True
    # printing
    def __str__(self):
        ''' We are not likely to ever want this, except for debugging '''
        retstr = ''
        for entry in self.namelist:
            retstr = retstr + entry.__str__()
        return retstr
    def __repr__(self):
        return self.__str__()
    # overlap
    def overlap(self, other):
        ''' Return a Key of the overlap region, or null if no overlap '''
        if not isinstance(other, Key):
            print('Keys only overlap with Keys')
            sys.exit(64)
        templ = []
        for entry in self.namelist:
            for oentry in other.namelist:
                if entry == oentry:
                    templ.append(entry)
        if len(templ) == 0:
            return None
        else:
            return Key(templ)
    # present
    def present(self, other):
        ''' Present a Name.  Is it in the Key? '''
        if not isinstance(other, Name.Name):
            print('Key present wants a Name')
            sys.exit(65)
        return other in self.namelist
    # contents
    def contents(self):
        ''' Dump the contents as a list '''
        return copy.deepcopy(self.namelist)
    def tuple(self):
        ''' Dump the contents as a tuple '''
        return tuple(copy.deepcopy(self.namelist))
