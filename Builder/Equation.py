''' Class to hold a set of Elements that sum to zero '''
import sys
import copy
from Builder import Name
from Builder import Fraction
from Builder import Element
from Builder import Key
from Builder import Chain
from Builder import Zero
from Builder import Equivalence

class Equation:
    ''' Class to hold a set of Elements that sum to zero '''
    def __init__(self, klist):
        ''' Initialize from a list of Element '''
        if not isinstance(klist, list):
            print('Equation needs a list to initialize with')
            sys.exit(70)
        if len(klist) <= 0:
            print('Equation needs a non-empty list to initialize with')
            sys.exit(71)
        self.elementlist = []
        for entry in klist:
            if not isinstance(entry, Element.Element):
                print('Equation needs the initialization list to be Elements')
                sys.exit(72)
            if len(self.elementlist) == 0:
                if not entry.fraction.isZero():
                    self.elementlist.append(copy.deepcopy(entry))
                continue
            if entry.name.size != self.elementlist[0].name.size:
                print('Please do not mix Names from different problems')
                sys.exit(73)
            dupe = False
            for already in self.elementlist:  # Duplicate Names forbidden 
                if entry.name == already.name:
                    already.muteadd(entry)
                    dupe = True
                    continue
            if not dupe:
                # If here, elementlist is not empty and this is not duplicate
                self.elementlist.append(copy.deepcopy(entry))
        for i in range(len(self.elementlist)-1, -1, -1):
            if self.elementlist[i].fraction.isZero():
                self.elementlist.pop(i)
        self.iszero = (len(self.elementlist) == 0)
    #
    def isZero(self):
        return self.iszero
    #
    def count(self):
        return len(self.elementlist)
    #
    def __eq__(self, other):
        ''' Check that the two equations are the same, modulo a scaling factor '''
        if not isinstance(other, Equation):
            print('Equation can only equal another Equation')
            sys.exit(74)
        if self.isZero() and other.isZero():
            return True
        if (self.isZero() and not other.isZero()) or (not self.isZero() and other.isZero()):
            return False
        if self.key() != other.key():
            return False
        # Check the scale factor for each term
        scales = []   # list of Fractions
        for entry in self.elementlist:
            for oentry in other.elementlist:
                if entry.name == oentry.name:
                    # Relies on Element being clean!  No zero Fractions allowed
                    scales.append(entry.fraction.multiply(oentry.fraction.invert()))
        for x in scales:   # wastes a step, but for cleanliness of code...
            if not x == scales[0]:
                return False
        return True
    #
    def cleanup(self):
        ''' Check if anything is zero.  Add together any Elements with the same Name
        In both cases, remove the redundant/zero stuff.
        Set the iszero flag if everything is zero. '''
        if self.iszero:
            return  # Nothing to do
        if len(self.elementlist) < 1:
            # If empty, bail
            self.iszero = True
            return
        if len(self.elementlist) == 1:
            if self.elementlist[0].fraction.isZero():
                self.iszero = True
                return
        #OK more than one item
        for i in range(len(self.elementlist)-1, -1, -1):
            # Loop backwards
            if self.elementlist[i].fraction.isZero():
                self.elementlist.pop(i)
        # Just in case...
        if len(self.elementlist) == 0:
            self.iszero = True
            return
        #
        maxr = len(self.elementlist)
        i = maxr - 1
        j = i - 1
        while i >= 0 and j >= 0:
            if self.elementlist[i].name == self.elementlist[j].name:
                self.elementlist[j].muteadd(self.elementlist[i])
                self.elementlist.pop(i)
                maxr = maxr - 1
                i = i - 1
                j = i - 1
            else:
                j = j - 1
            if j < 0:
                i = i - 1
                j = i - 1
        # Should be no duplicates here
        # BUT.  Some Elements may have cancelled.  So repeat
        for i in range(len(self.elementlist)-1, -1, -1):
            # Loop backwards
            if self.elementlist[i].fraction.isZero():
                self.elementlist.pop(i)
        # Just in case...
        if len(self.elementlist) == 0:
            self.iszero = True
            return
        # done
        return
    #
    def giveElement(self, other):
        ''' Return the Element that other matches '''
        if isinstance(other, Element.Element):
            sear = other.name
        elif isinstance(other, Name.Name):
            sear = other
        else:
            print('Searching an Equation for something not a Name or Element')
            sys.exit(75)
        #
        for entry in self.elementlist:
            if sear == entry.name:
                return copy.deepcopy(entry)
        return None
    #
    def present(self, other):
        ''' Is the other Chain/Element/Name present in the Equation? '''
        if isinstance(other, Chain.Chain):
            for ele in other.contents():
                if self.present(ele):
                    return True
            return False
        if isinstance(other, Element.Element):
            sear = other.name
        elif isinstance(other, Name.Name):
            sear = other
        else:
            print('Searching an Equation for something not a Name or Element')
            sys.exit(75)
        #
        for entry in self.elementlist:
            if sear == entry.name:
                return True
        return False
    #
    def key(self):
        ''' Return the Key for this Equation '''
        temp = []
        for entry in self.elementlist:
            temp.append(copy.deepcopy(entry.name))
        return Key.Key(temp)
    #
    def scale(self, scaler):
        ''' Multiply all Elements of this Equation by the Fraction scaler '''
        if not isinstance(scaler, Fraction.Fraction):
            print('Scale an Equation with a Fraction')
            sys.exit(76)
        if scaler == Fraction.Fraction(0, 1):  # Do not bother, just set flag to 0
            self.iszero = True
            return
        for entry in self.elementlist:
            entry.mutemultiply(scaler)
        return
    #
    def __str__(self):
        ''' Make into a string '''
        if self.iszero:
            return ' 0 '    # No need to be fancy
        if len(self.elementlist) == 1:
            return '0=' + str(self.elementlist[0])
        base = '0='
        for i in range(len(self.elementlist) - 1):
            base = base + str(self.elementlist[i]) + '+'
        return base + str(self.elementlist[-1])
    #
    def __repr__(self):
        return self.__str__()
    #
    def inchain(self, other):
        ''' Are all Elements' Names in this Equation already present in the [Chain] '''
        if not isinstance(other, list):
            print('Element:inchain wants a *list* of Chain', type(other))
            sys.exit(77)
        for entry in other:
            if not isinstance(entry, Chain.Chain):
                print('Element:inchain wants a list of *Chain*', type(entry))
                sys.exit(78)
        #
        if len(self.elementlist) == 0:
            return True     # Nothing unique here
        lkey = self.key().contents()
        ckeys = []
        for entry in other:
            ckeys.extend(entry.Key().contents())
        noverlap = 0
        for k in lkey:
            if k in ckeys:
                noverlap = noverlap + 1
                continue
        if noverlap == len(lkey):
            return True # all entries are accounted for in Chains
        return False
    #
    def formalSolve(self, other):
        ''' return an Equivalence based on solving for the given Element '''
        if not isinstance(other, Element.Element) and not isinstance(other, Name.Name):
            print('Equation:formalSolve wants something to solve for')
            sys.exit(79)
        if isinstance(other, Element.Element):
            exname = other.name
        else:
            exname = other
        notfound = True
        for entry in self.elementlist:
            if exname == entry.name:
                notfound = False
                break
        if notfound:
            print('Equation:formalSolve needs an element it HAS to solve for')
            sys.exit(170)
        return Equivalence.Equivalence(self, exname)
    #
    def reduce(self, other):
        ''' Make substitutions of any elements that are in Zero or in the Chain
        or the list of Chains--3 possible arguments '''
        # Sanity checking
        if (not isinstance(other, Chain.Chain) and 
                not isinstance(other, Zero.Zero) and
                not isinstance(other, list)):
            print('Equation:reduce wants Zero or Chain or list[Chain]')
            sys.exit(171)
        #
        if isinstance(other, list):
            for entry in other:
                if not isinstance(entry, Chain.Chain):
                    print('Equation:reduce wants Zero or Chain or *list[Chain]*')
                    sys.exit(172)
        #
        # Do the Zero first.  Easiest.
        if isinstance(other, Zero.Zero):
            for zname in other.zerolist:
                for entry in self.elementlist:
                    if zname == entry.name:
                        entry.fraction.muteforceZero()
            self.cleanup()
            return
        # A single Chain
        if isinstance(other, Chain.Chain):
            self.reducechain(other)
            return
        # A list [Chain]
        for chainentry in other:
            self.reducechain(chainentry)
        return
    #
    def reducechain(self, other):
        ''' Utility to handle a single Chain -- not to be used outside of reduce() '''
        if isinstance(other, Chain.Chain):
            ifraction = other.chainlist[0].fraction
            iname = other.chainlist[0].name
            for centry in other.chainlist:
                cname = centry.name
                for i in range(len(self.elementlist)):
                    lentry = self.elementlist[i]
                    if cname == lentry.name:
                        # replace with scaled first element in chain:
                        # lentry.fraction * chainlist[0].fraction / centry.fraction
                        newfrac = ifraction.multiply(lentry.fraction).multiply(centry.fraction.invert())
                        self.elementlist[i] = Element.Element(iname, newfrac)
            self.cleanup()
    #
    def replace(self, other):
        ''' Using the equivalence provided, replace an instance of the target Name, if any,
        with the rest of the Equation '''
        if not isinstance(other, Equivalence.Equivalence):
            print('Equation:replace wants an Equivalence')
            sys.exit(173)
        # Have an equivalence
        eletarg = other.target
        elename = eletarg.name
        for entry in self.elementlist:
            if entry.name == elename:
                scale = entry.fraction.multiply(eletarg.fraction.invert())
                entry.muteforceZero()
                for oentry in other.collection:
                    self.elementlist.append(oentry.multiply(scale))
                break
        self.cleanup()
    #
    def contents(self):
        ''' Return a copy of the contents '''
        templist = []
        for entry in self.elementlist:
            templist.append(copy.deepcopy(entry))
        return templist
    #
    def __hash__(self):
        ''' Hash of the contents '''
        return hash(tuple(self.elementlist))
