''' Special :  Elements that are all equal '''
import sys
import copy
from Builder import Key
from Builder import Name
from Builder import Fraction
from Builder import Element

class Chain:
    ''' Holds a collection of Element that are equal to each other '''
    NOOP = 0    # For merging--the two Chains we compared differed completely, or that no Chain was made
    MERGED = 1  # For merging--the two Chains overlapped and were merged into self--other zero'ed
    ZEROED = 2  # For merging--the two Chains overlapped but conflicted, both were zero'ed
    MADE = 4    # For notifying that one or more Chains were created
    def __init__(self, klist):
        ''' Initialize given a List of Elements '''
        if not isinstance(klist, list):
            print('Chain needs a list to initialize with, maybe only 2')
            sys.exit(100)
        self.chainlist = []
        self.iszero = False
        self.usedup = False
        #
        key = []
        for entry in klist:
            if not isinstance(entry, Element.Element):
                print('Chain needs the initialization list to be Elements', type(entry), entry, klist)
                sys.exit(101)
            kname = entry.name
            if kname not in key:
                key.append(kname)
        if len(key) < len(klist):
            print('Chain initialization should not contain duplicates')
            sys.exit(102)
        for entry in klist:
            self.chainlist.append(entry)
        # Normalize so first has Fraction=1
        scale = self.chainlist[0].fraction.invert()
        for i in range(len(self.chainlist)):
            self.chainlist[i].fraction.mutemultiply(scale)
        #
    def Key(self):
        ''' Return Names in this Chain '''
        key = []
        for entry in self.chainlist:
            key.append(entry.name)
        return Key.Key(key)
    def count(self):
        ''' How many elements are in the Chain? '''
        return len(self.chainlist)
    #
    ###############################
    def add(self, bother):
        ''' Add another Element or set of the same to the Chain 
        You would be wisest to use the list--maybe I should force that--because
        if you use the list this routine takes care of the relationship scale
        for you.  Otherwise it just assumes you know what you are doing.  Sometimes
        you don't
          Also, probably more important: Add another Chain to this!
        '''
        # Sanity check the arguments.
        if not isinstance(bother, list) and not isinstance(bother, Chain):
            print('Chain wants a list of Elements to add or a Chain')
            sys.exit(103)
        if isinstance(bother, Chain):
            if bother.isZero():
                return  # Nothing to do, other is zero
            other = bother.chainlist
        else:
            other = bother
        argkey = []
        for entry in other:
            if not isinstance(entry, Element.Element):
                print('Chain wants a list of Elements')
                sys.exit(104)
            if entry.name not in argkey:
                argkey.append(entry.name)
        #
        if len(argkey) < len(other):
            print('Chain add list contains duplicates')
            sys.exit(105)
        # make the local name list
        lkey = []
        for entry in self.chainlist:
            lkey.append(entry.name)
        #
        overlap = []
        for lname in lkey:
            if lname in argkey:
                overlap.append(lname)
        if len(overlap) < 1:
            print('Chain new list must overlap the old')
            sys.exit(106)
        if len(overlap) > 1:
            # OK, we need to take care here.  Check that all of the overlapping
            # 
            localFrac = []
            otherFrac = []
            for name in overlap:
                for lentry in self.chainlist:
                    if name == lentry.name:
                        localFrac.append(copy.deepcopy(lentry.fraction))
                        break
                for oentry in other:
                    if name == oentry.name:
                        otherFrac.append(copy.deepcopy(oentry.fraction))
                        break
            # OK, now check that the fractions all match in the overlap region
            # If they don't--the whole Chain is 0
            comparison = []
            for i in range(len(overlap)):
                comparison.append(localFrac[i].multiply(otherFrac[i].invert()))
            for i in range(len(overlap)):
                if not comparison[i] == comparison[0]:
                    #print('Chain giving inconsistent overlap, setting everything to 0')
                    self.iszero = True
                    # Just load the other stuff willy-nilly, don't worry about scaling, all=0
                    for entry in other:
                        if not entry.name in overlap:
                            self.chainlist.append(copy.deepcopy(entry))
                            return
            # OK, if here, everything is consistent.  We just have to add the new entries
            # with the appropriate scaling
            for entry in other:
                if not entry.name in overlap:
                    self.chainlist.append(entry.multiply(comparison[0]))
            return
        # At this point we are at len(overlap) = 1, and things are fairly simple
        for lentry in self.chainlist:
            if overlap[0] == lentry.name:
                lfrac = copy.deepcopy(lentry.fraction)
                break
        for oentry in other:
            if overlap[0] == oentry.name:
                ofrac = copy.deepcopy(oentry.fraction)
                break
        lfrac.mutemultiply(ofrac.invert())
        for entry in other:
            if not entry.name in overlap:
                self.chainlist.append(entry.multiply(lfrac))
        # Done
        # 
    #
    def countpresent(self, other):
        ''' Is the Name or Element in the Chain? How many? '''
        if (not isinstance(other, Name.Name) and not isinstance(other, Element.Element)
                and not isinstance(other, list)):
            print('Chain can only check Names or Elements or list of them ' + str(other))
            sys.exit(107)
        if not isinstance(other, list):
            if isinstance(other, Element.Element):
                kname = other.name
            else:
                kname = other
            for entry in self.chainlist:
                if kname == entry.name:
                    return 1
            return 0
        #
        rkey = []
        for entry in other:
            if (not isinstance(entry, Name.Name) and not isinstance(entry, Element.Element)):
                print('Chain can only check lists of Name or Element')
                sys.exit(108)
            if isinstance(entry, Element.Element):
                rkey.append(entry.name)
            else:
                rkey.append(entry)
        #
        ocount = 0
        for entry in self.chainlist:
            if entry.name in rkey:
                ocount = ocount + 1
        return ocount
    #
    def __str__(self):
        ''' Turn into a string '''
        if len(self.chainlist) <= 0:
            return ' 0 '
        if len(self.chainlist) == 1:
            return str(self.chainlist[0])
        st = str(self.chainlist[0])
        for i in range(1, len(self.chainlist)):
            st = st + '=' + str(self.chainlist[i])
        return st
    #
    def __repr__(self):
        ''' Turn into a string '''
        return self.__str__()
    #
    def isZero(self):
        ''' Is this zero?  If so, move stuff to the Zero object '''
        return self.iszero
    def setZero(self):
        ''' Set this to zero.  All elements are 0 regardless of Fraction,
        and will later be merged into the Zero object '''
        self.iszero = True
    #
    def isUsedUp(self):
        ''' Is this completely accounted for?  If so, skip '''
        return self.usedup
    def setUsedUp(self):
        ''' Flag this as used up, for discard '''
        self.usedup = True
    #
    def merge(self, other):
        ''' Compare the other chain with this one.
        Cases:
          They do not overlap.  Do nothing.  Notify the calling program
          They _do_ overlap, but are inconsistent.  Set both to 0 and notify the calling program
          They _do_ overlap, consistently.  Merge the argument into self, and null the other, and notify
        This requires 3 different answers, so bool won't work. See constants above:  NOOP, MERGED, and
        ZEROED
            '''
        # Sanity
        if not isinstance(other, Chain):
            print('Chain:merge will not merge with anything but another Chain')
            sys.exit(109)
        if other.isUsedUp() or self.usedup:
            return Chain.NOOP
        #
        foverlap = []
        lelem = []
        oelem = []
        for lentry in self.chainlist:
            for oentry in other.chainlist:
                if lentry.name == oentry.name:
                    lelem.append(lentry)
                    oelem.append(oentry)
        if len(lelem) == 0:
            return Chain.NOOP
        #
        # If here we have overlap.
        # The question is HOW
        if len(lelem) == 1:
            if lelem[0].fraction.isZero():
                print('Chain:merge cannot merge zero Chain! ' + str(self))
                sys.exit(110)
            foverlap.append(oelem[0].fraction.multiply(lelem[0].fraction.invert()))
        else:
            for i in range(len(lelem)):
                if lelem[i].fraction.isZero():
                    print('Chain:merge cannot merge zero Chain! ' + str(self))
                    sys.exit(111)
                foverlap.append(oelem[i].fraction.multiply(lelem[i].fraction.invert()))
            for i in range(len(foverlap)):
                if foverlap[i] != foverlap[0]:
                    self.iszero = True
                    other.setZero()
                    return Chain.ZEROED
        #
        # If here we have overlap AND consistency.  Merge the other into self and null the other
        for oentry in other.chainlist:
            if oentry in oelem:
                continue    # already present and accounted for
            self.chainlist.append(oentry.multiply(foverlap[0]))  # returns a new Element
        other.setUsedUp()
        return Chain.MERGED
