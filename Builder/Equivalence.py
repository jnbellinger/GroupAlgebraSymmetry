''' Class to hold a set of Elements that sum to another Element with Fraction 1/1 '''
import sys
import copy
from Builder import Name as N
from Builder import Fraction as F
from Builder import Key
from Builder import Element
from Builder import Equation

class Equivalence:
    ''' Class to hold a set of Elements that sum to zero '''
    def __init__(self, other, singleton):
        ''' Initialize from a list of Elements and an Element
            or from an Equation and an Element/Name in that Equation
            normalize to the unique one '''
        # Cases:  other,    singleton
        #         Equation, Name in the Equation
        #         Equation, Element in the Equation
        #       [Element],  Element not in the list
        # sanity checks
        if isinstance(other, list):
            if not isinstance(singleton, Element.Element):
                print('Equivalence([Element], *Element*)')
                sys.exit(90)
            if len(other) <= 0:
                print('Equivalence(non-empty [Element], Element)')
                sys.exit(91)
            for x in other:
                if not isinstance(x, Element.Element):
                    print('Equivalence([*Element*], Element)')
                    sys.exit(92)
            if singleton not in other:
                print('Equivalence([Element], Element *not in []*')
                sys.exit(93)
        elif isinstance(other, Equation.Equation):
            if not isinstance(singleton, N.Name) and not isinstance(singleton, Element.Element):
                print('Equivalence(Equation, *Name or Element*)')
                sys.exit(94)
            if not other.present(singleton):
                print('Equivalence(Equation, Name or Element *in the Equation*)')
                sys.exit(95)
        else:
            print('Equivalence want either a list[Element] or Equation first arg')
            sys.exit(96)
        #
        # Initializing from an Equation
        # The singleton is used to specify which is the Element to single out
        # and scale the rest by.
        if isinstance(other, Equation.Equation):
            if isinstance(singleton, Element.Element):
                kname = singleton.name
            else:
                kname = singleton
            self.target = other.giveElement(kname)
            self.collection = []
            for entry in other.elementlist:
                if not entry == self.target:
                    self.collection.append(copy.deepcopy(entry))
            # Now scale everything
            basescale = self.target.fraction.invert().multiply(F.Fraction(-1, 1))
            for entry in self.collection:
                entry.mutemultiply(basescale)
        else:
            # This is for a list of Elements vs an Element.  No negation needed
            # sanity checks already done
            self.target = copy.deepcopy(singleton)
            self.collection = []
            for entry in other:
                self.collection.append(copy.deepcopy(entry))
            # Now scale everything
            basescale = self.target.fraction.invert()
            for entry in self.collection:
                entry.mutemultiply(basescale)
        self.target.fraction.mutereplace(1, 1)
        self.iszero = False
        self.targetzero = False
    #
    def isZero(self):
        return self.iszero
    def isTargetZero(self):
        return self.targetzero
    #
    def count(self):
        return len(self.collection)
    #
    def __eq__(self, other):
        ''' Check that the two Equivalences are the same, modulo a scaling factor 
        Note that there are two possible meanings for equality:
            1) The targets are the same and the balances are the same 
            2) The fundamental equations are the same, but there are potentially
            different targets 
        Here we use the first.  I should create another that represents the
        other:  call it equivalent(self, other) '''
        if not isinstance(other, Equivalence):
            print('Equivalence can only equal another Equivalence')
            sys.exit(74)
        if self.iszero and other.iszero:
            return True
        if self.target.name != other.target.name or len(self.collection) != len(other.collection):
            return False
        # Check the scale factor for each term
        scales = [self.target.fraction.multiply(other.target.fraction.invert())]  # list of Fractions
        for entry in self.collection:
            for oentry in other.collection:
                if entry.name == oentry.name:
                    # Relies on Element being clean!  No zero Fractions allowed
                    scales.append(entry.fraction.multiply(oentry.fraction.invert()))
        if len(scales) != len(self.collection) + 1:
            return False
        for x in scales:   # wastes a step, but for cleanliness of code...
            if not x == scales[0]:
                return False
        return True
    #
    def equivalent(self, other):
        ''' Check that the two Equivalences have the same Equation, modulo a scaling factor 
        Note that there are two possible meanings for equality:
            1) The targets are the same and the balances are the same 
            2) The fundamental equations are the same, but there are potentially
            different targets 
        Here we use the second.  The __eq__ is the other '''
        if not isinstance(other, Equivalence):
            print('Equivalence can only be equivalent to another Equivalence')
            sys.exit(171)
        if self.iszero and other.iszero:
            return True
        templist = copy.deepcopy(self.collection)
        templist.append(copy.deepcopy(self.target).multiply(F.Fraction(-1, 1)))
        tempself = Equation.Equation(templist)
        tempoth = copy.deepcopy(other.getCollection())
        tempoth.append(copy.deepcopy(other.getTarget()).multiply(F.Fraction(-1, 1)))
        tempother = Equation.Equation(tempoth)
        if tempself != tempother:
            return False
        return True
    #
    def cleanup(self):
        ''' Check if anything is zero.  Add together any Elements with the same Name
        In both cases, remove the redundant/zero stuff.
        Set the iszero flag if everything is zero.
        Also check if this is trivial, in which case flag it as iszero '''
        if self.iszero:
            return  # nothing to do
        if len(self.collection) < 1:
            self.iszero = True
            return
        if len(self.collection) == 1:
            if self.collection[0].fraction.isZero():
                self.iszero = True
                return
        #OK more than one item
        for i in range(len(self.collection)-1, -1, -1):
            # Loop backwards
            if self.collection[i].fraction.isZero():
                self.collection.pop(i)
        # Just in case...
        if len(self.collection) == 0:
            self.iszero = True
            return
        #
        maxr = len(self.collection) - 1
        i = maxr
        j = i - 1
        while i >= 0 and j >= 0:
            if self.collection[i].name == self.collection[j].name:
                self.collection[j].muteadd(self.collection[i])
                self.collection.pop(i)
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
        for i in range(len(self.collection)-1, -1, -1):
            # Loop backwards
            if self.collection[i].fraction.isZero():
                self.collection.pop(i)
        # Just in case...  Should be taken care of elsewhere already, but backstop it
        if len(self.collection) == 0:
            self.iszero = True
            return
        #
        maxr = len(self.collection) - 1
        i = maxr
        while i >= 0:
            if self.collection[i].name != self.target.name:
                i = i - 1
                continue
            self.target.muteadd(self.collection[i].multiply(F.Fraction(-1, 1)))
            self.collection.pop(i)
            i = i - 1
        # Can kill ourselves here:
        if self.target.isZero():
            if len(self.collection) == 0:
                self.iszero = True
                self.targetzero = True
                return
            # Now what?  pick another target if possible
            if len(self.collection) == 1:
                # Just a singleton left.  Announce that the target is zero; shouldn't happen
                self.target = self.collection[0]
                self.collection.pop(0)
                self.targetzero = True
                self.iszero = True
                return
            maxr = len(self.collection) - 1
            self.target = self.collection[-1]
            self.collection.pop(maxr)
            for entry in self.collection:
                entry.fraction.mutemultiply(self.target.fraction.invert())
            self.target.fraction.mutereplace(1, 1)  # cancels to 1, just replace
            return
        if maxr >= len(self.collection):
            # we have made changes; rescale
            for entry in self.collection:
                entry.mutemultiply(self.target.fraction.invert())
            self.target.fraction.mutereplace(1, 1)  # cancels to 1, just replace
        if len(self.collection) == 0:   # Once more for safety's sake, but shouldn't happen
            self.targetzero = True
            self.iszero = True
            return
        if len(self.collection) == 1:
            if self.target == self.collection[0]:
                # We have a trivial Equivalence
                self.iszero = True
                return
        # done
        ################## NOPE CHECK AGAINST TARGET ##############
        return
    #
    def present(self, other):
        ''' Is the other Element/Name present in the Equivalence? '''
        if isinstance(other, Element.Element):
            sear = other.name
        elif isinstance(other, N.Name):
            sear = other
        else:
            print('Searching an Equivalence for something not a Name or Element')
            sys.exit(75)
        #
        if sear == self.target.name:
            return True
        for entry in self.collection:
            if sear == entry.name:
                return True
        return False
    #
    def key(self):
        ''' Return the Key for this Equivalence First Element name followed by the rest '''
        temp = [self.target.name]
        for entry in self.collection:
            temp.append(copy.deepcopy(entry.name))
        return Key.Key(temp)
    #
    def scale(self, scaler):
        ''' Multiply all Elements of this Equivalence by the Fraction scaler '''
        if not isinstance(scaler, F.Fraction):
            print('Scale an Equivalence with a Fraction')
            sys.exit(76)
        if scaler == F.Fraction(0, 1):  # Do not bother, just set flag to 0
            self.iszero = True
            return
        for entry in self.collection:
            entry.mutemultiply(scaler)
        self.target.mutemultiply(scaler)
        return
    #
    def __str__(self):
        ''' Make into a string '''
        if self.iszero:
            return ' 0 '    # No need to be fancy
        if len(self.collection) == 1:
            return str(self.target) + '=' + str(self.collection[0])
        base = str(self.target) + '='
        for i in range(len(self.collection) - 1):
            base = base + str(self.collection[i]) + '+'
        if len(self.collection) == 0:
            return base + '0'
        return base + str(self.collection[-1])
    #
    def __repr__(self):
        return self.__str__()
    #
    def replace(self, other):
        ''' Using the equivalence provided, replace an instance of the target Name, if any,
        with the rest of the Equation '''
        if not isinstance(other, Equivalence):
            print('Equation:replace wants an Equivalence')
            sys.exit(77)
        # We have an equivalence to use
        # Special case--targets are the same
        if self == other:
            return  # Nothing to do
        if self.target == other.target:
            # targets are the same but the rest is not.
            # VIP! Subtraction is probably in order, creating a new Equation, not
            # a new Equivalence.  But just in case, know how to do a replacement
            for entry in self.collection:
                entry.fraction.mutemultiply(F.Fraction(1, 2))
            for entry in other.collection:
                self.collection.append(entry.multiply(F.Fraction(1, 2)))
            self.cleanup()  # May wind up being zero.
            return
        # targets are not the same
        eletarg = other.target
        elename = eletarg.name
        for entry in self.collection:
            if entry.name == elename:
                scale = entry.fraction.multiply(eletarg.fraction.invert())
                entry.muteforceZero()
                for oentry in other.collection:
                    self.collection.append(oentry.multiply(scale))
                break
        self.cleanup()
    #
    def mutemultiply(self, other):
        ''' Scale everything (including target!) by a Fraction
        This is NOT for general use, because it rescales the target!
        Use for something like adding two Equivalences, or subtracting them.  '''
        if not isinstance(other, F.Fraction):
            print('Equivalance:mutemultiply wants a Fraction')
            sys.exit(78)
        if other.isZero():
            self.iszero = True
            return
        self.target.mutemultiply(other)
        for entry in self.collection:
            entry.mutemultiply(other)
        return
    #
    def subtract(self, other):
        ''' If the targets are the same, find their difference (an Equation) '''
        if not isinstance(other, Equivalence):
            print('Equivalence:subtract wants an Equivalence')
            sys.exit(79)
        if not self.target == other.target:
            print('Equivalence:subtract wants the targets to be the same.  Wrong tool')
            sys.exit(170)
        collect = []
        for entry in self.collection:
            collect.append(copy.deepcopy(entry))
        for entry in other.collection:
            collect.append(entry.multiply(F.Fraction(-1, 1)))
        return Equation.Equation(collect)
    #
    def getTarget(self):
        return self.target      # Not meant to be mutable
    def getCollection(self):
        return self.collection  # Not meant to be mutable
    #
    def reverseToEquation(self):
        ''' Return an Equation congruent to the one this was made from '''
        xxx = copy.deepcopy(self.collection)
        xxx.append(self.target.multiply(F.Fraction(-1,1)))
        return Equation.Equation(xxx)
    #
