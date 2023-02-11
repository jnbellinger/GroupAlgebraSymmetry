# pylint: disable=invalid-name
''' Collect stuff from solving for a commutation, and display it
   We have for C_i and C_j (there are M of these)
   i        # of first
   j        # of second
   [Equation]   # Equations in Name(n, 0, M) (constant=1) and Name(0, x, M), which are the
                constant terms (=1) and the scaling factors for the C_x matrices respectively
   [Chain]  # Chains in the Name(n, 0, M) and Name(0, x, M) (only one of the former per
            Chain, I hope--may want to check that)
   Zero     # Zero instance
   Stand ready to print out the resulting commutation equation of the form
   [C1, C3] = (-1)C2 + (-2)C4
   Validation that the relations are correct is presumed to have already been done
   '''
import sys
import copy
import math
from Builder import Fraction as F
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Name as N
from Builder import Chain
from Builder import Zero

class CommuteBundle:
    ''' Generate the set of Matrix defining the differential operators.
    The commutators are the deliverables '''
    def __init__(self, first, second, listOfEquations, listOfChains, zero):
        if ( not isinstance(listOfEquations, list) or not isinstance(listOfChains, list)
                or not isinstance(zero, Zero.Zero) or not isinstance(first, int)
                or not isinstance(second, int) ):
            print('CommuteBundle:__init 320 needs i, j, listOfEquations, listOfChain, Zero', type(listOfEquations), type(listOfChains))
            sys.exit(340)
        #
        for entry in listOfEquations:
            if not isinstance(entry, Eq.Equation):
                print('CommuteBundle:__init  wants a list of *Equations* first')
                sys.exit(341)
        for entry in listOfChains:
            if not isinstance(entry, Chain.Chain):
                print('CommuteBundle:__init  wants a list of *Chains* second', entry)
                sys.exit(342)
        #
        if len(listOfEquations) == 0 and len(listOfChains) == 0 and zero.count() == 0:
            print('CommuteBundle:__init needs SOMETHING to be non-zero--even the list of zeros!', first, second)
            sys.exit(343)
        self.first = first
        self.second = second
        if len(listOfEquations) != 0:
            self.NumberFreeParameters = listOfEquations[0].target.name.size
        elif len(listOfChains) != 0:
            self.NumberFreeParameters = listOfChains[0].chainlist[0].name.size
        else:
            self.NumberFreeParameters = zero.zerolist[0].size
        # The below may seem silly, but the listOfEquations will almost always be overwritten
        # by the processing for the next commutator
        self.initialEquations = copy.deepcopy(listOfEquations)
        self.initialChains = copy.deepcopy(listOfChains)
        self.zero = zero
    #
    def __repr__(self):
        return self.__str__()
    #
    def __str__(self):
        ''' Heart and soul of this thing--format the output! '''
        # First:  Is everything zero?
        order = int(math.log10(self.NumberFreeParameters) + .0001) + 1
        baseString = '[C' + str(self.first).zfill(order) + ', C' + str(self.second).zfill(order) + '] = '
        if self.NumberFreeParameters <= self.zero.count():
            #
            if self.NumberFreeParameters < self.zero.count():
                ( print('CommuteBundle:__str NumberFreeParameters is less than the number of zeros??',
                    self.NumberFreeParameters, self.zero.count()), len(self.initialEquations),
                    len(self.initialChains), self.zero )
            #    sys.exit(344)
            return baseString + '0'
        #
        chaincount = 0
        if len(self.initialChains) != 1:
            print('CommuteBundle:__str has multiple Chains.  Not sure how to deal with this', self.initialChains)
            sys.exit(345)
        for entry in self.initialChains:    # Maybe I'll need to use multiple Chains someday
            for ele in entry.contents():
                if ele.name.row != 0:
                    continue
                chaincount = chaincount + 1
        if chaincount + self.zero.count() > self.NumberFreeParameters:
            ( print('CommuteBundle:__str NumberFreeParamers is less than the number of entries in Chains and Zeros',
                self.NumberFreeParameters, chaincount, self.zero.count()) )
            print(self.initialChains)
            print(self.zero)
            sys.exit(346)
        if chaincount + self.zero.count() == self.NumberFreeParameters:
            # I only need to note the stuff in Chains.  The zeros get ignored.
            # There should be only 1 constant term in each Chain, with a name of the form {m_0}
            for entry in self.initialChains:
                constcount = 0
                constele = E.Element(N.Name(0, 0, 100), F.Fraction(1, 1))
                for ele in entry.contents():
                    if ele.name.row != 0:
                        constele = copy.deepcopy(ele)
                        constcount = constcount + 1
                if constcount != 1:
                    print('CommuteBundle:__str The chain has two constant terms in it!', entry)
                    sys.exit(347)
                scalefrac = constele.fraction
                for ele in entry.contents():
                    if ele == constele:
                        continue
                    newname = ele.invert().multiply(scalefrac)
                    namenewname = 'C' + str(newname.name.column).zfill(order)
                    baseString = baseString + str(newname.fraction) + namenewname + ' + '
            #
            return baseString[0:-3]
        #
        return 'Not sure what to do with Equations'
    #
