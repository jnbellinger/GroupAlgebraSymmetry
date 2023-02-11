''' routine to, given a ListOfEquivalences, Zero object, and list of Chains, generate a list of matrices '''
import sys
import copy
from Builder import Fraction as F
from Builder import Equivalence as Equiv
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Name as N
from Builder import Chain
from Builder import Matrix as M
from Builder import SolveEquations
from Builder import CommuteBundle
from Builder import Zero
# pylint: disable=invalid-name

class GenerateMatrix:
    ''' Generate the set of Matrix defining the differential operators.
    The commutators are the deliverables '''
    def __init__(self, listOfEquivalences=[], listOfChains=[]):
        if ( not isinstance(listOfEquivalences, list) or not isinstance(listOfChains, list)):
            print('GenerateMatrix:__init 320 needs listOfEquivalences, listOfChain', type(listOfEquivalences), type(listOfChains))
            sys.exit(320)
        #
        for entry in listOfEquivalences:
            if not isinstance(entry, Equiv.Equivalence):
                print('GenerateMatrix:__init 321 wants a list of *Equivalences* first')
                sys.exit(321)
        for entry in listOfChains:
            if not isinstance(entry, Chain.Chain):
                print('GenerateMatrix:__init 322 wants a list of *Chains* second', entry)
                sys.exit(322)
        #
        if len(listOfEquivalences) > 0:
            self.groupsize = listOfEquivalences[0].target.name.size
        elif len(listOfChains) > 0:
            self.groupsize = listOfChains[0].chainlist[0].name.size
        else:
            print('GenerateMatrix:__init 320 lists are both empty, nothing to do!')
            sys.exit(320)
        self.initialEquivalences = listOfEquivalences   # treat as pointer only
        self.initialChains = listOfChains  # treat as pointer only
        self.EquivChains = None  # Fill later
        self.MatrixList = None  # Fill from FindEquivChains routine(s)
        self.NumberFreeParameters = 0
        self.EquivChainPointer = None
        self.FreeChainPointer = None
        self.MatrixMatch = None
        self.UniqueList = None
        self.commutEquations = []
        self.commuteCoeffs = []
        self.commuteSolutions = []
        self.FindEquivChains()
    #
    def FindEquivChains(self):
        ''' Create structures for managing the Equivalences
        Every Name refers to a specific row&column in the representation 
        Matrix.
        For the n'th FreeChain, every Element will have Name and Fraction:
          The n'th Matrix will have the row/column from that Element's Name
          filled with the Fraction associated with it
        Each Equivalence has a target, and that target is associated with
        a Chain.  Those Chains are not included in the FreeChainPointer.  They are
        in the EquivChains, and treated differently.
        The target's Element's Name will be used to refer to a row/column
        in a number of different Matrix objects.  Each Element in the "collection"
        has a Name associated with one of the FreeChainPointer--say the m'th.  Then the
        m'th Matrix will have the row/column entry filled with the Element's Fraction,
        multiplied by whatever the Chain's Element's Fraction is for that one
        
        At the end we should have as many Matrix objects as we do FreeChainPointer
        Called from __init__() '''
        #
        # Not going to bother with sanity checks here, not meant for external use
        self.EquivChains = []
        self.EquivChainPointer = []
        self.FreeChainPointer = []
        # First load the EquivChainPointer array.  These are the chains that include
        # the targets for our Equivalences
        for entry in self.initialEquivalences:
            tname = entry.target.name
            found = False
            for n, chain in enumerate(self.initialChains):
                if chain.countpresent(tname) == 1:
                    #self.EquivChains.append(copy.deepcopy(chain))   #NOTE: will have to renormalize
                    found = True
                    self.EquivChainPointer.append(n)
                    break
            if not found:
                # If here, we did not find a Chain for the target of this Equivalence!
                print('GenerateMatrix:FindEquivChains--failed to find a Chain for', tname)
                print(self.initialChains)
                print(len(self.initialEquivalences))
                print(self.initialEquivalences)
                sys.exit(327)
        #
        # Now load the list of FreeChainPointers:  the Chains that do NOT include the targets
        # of the Equivalences--in other words, all the rest.
        for n, chain in enumerate(self.initialChains):
            if n not in self.EquivChainPointer:
                self.FreeChainPointer.append(n)
        #
        self.NumberFreeParameters = len(self.FreeChainPointer)
        if self.NumberFreeParameters == 0:
            print('GenerateMatrix:FindEquivChains--no free parameters?')
            sys.exit(323)
        self.MatrixList = []
        for n in range(self.NumberFreeParameters):
            self.MatrixList.append(M.Matrix(self.groupsize))
        #  Free chains are easy.
        for number in range(self.NumberFreeParameters):
            pointchain = self.FreeChainPointer[number]
            for elem in self.initialChains[pointchain].contents():
                self.MatrixList[number].set(elem.name, elem.fraction)
        #
        # EquivChains are messier, but so long as we keep careful track of the
        # Fractions, should be OK.
        # 0) The target in the m'th Equivalence should already be normalized
        # 00) Each Chain should be normalized such that the first Element has 1/1 for Fraction
        # 1) An Element in the "collection" will have a Fraction Fcol
        # 2) That Element's Name will match an Element in the n'th Chain; ElCh
        # 3) The Fraction associated with ElCh call Fch
        # 4) The Matrix entry in the n'th Matrix for the row/column given by the Name
        #    will be filled with Fcol*Fch
        for n, equiv in enumerate(self.initialEquivalences):
            pointchain = self.EquivChainPointer[n]
            thisequivchain = self.initialChains[pointchain]
            for element in thisequivchain.contents():
                # I know that the target.name is in this chain already
                basefraction = element.fraction
                ename = element.name
                for colelement in equiv.getCollection():
                    collectelementname = colelement.name
                    for number in range(self.NumberFreeParameters):
                        cchain = self.initialChains[self.FreeChainPointer[number]]
                        if cchain.countpresent(collectelementname) == 1:
                            for celement in cchain.contents():
                                newfraction = basefraction.multiply(colelement.fraction)
                                self.MatrixList[number].set(ename, newfraction)
        #
    #
    def CheckTheSum(self, matrixinstance, matrixbundle):
        ''' Verify that the matrixinstance is equal to the sum of the MatrixList*coefficients '''
        #
        runningmatrix = M.Matrix(self.groupsize)
        for chainentry in matrixbundle.initialChains:
            constcount = 0
            for elem in chainentry.contents():
                if elem.name.row != 0:
                    constelem = copy.deepcopy(elem)
                    constcount = constcount + 1
            if constcount != 1:
                print('GenerateMatrix:CheckTheSum did not have exactly 1 constant term')
                sys.exit(329)
            scalefrac = constelem.fraction
            for elem in chainentry.contents():
                if elem == constelem:
                    continue
                newname = elem.invert().multiply(scalefrac)
                whichmatrix = newname.name.column
                runningmatrix = runningmatrix.add(self.MatrixList[whichmatrix], fraction=newname.fraction)
        if runningmatrix == matrixinstance:
            return True
        print('GenerateMatrix:ParseIntoSum did not completely account for all bits of the input matrix\n', runningmatrix, '\n--\n', matrixinstance, '\n', matrixbundle.initialChains, '\n\n', self.UniqueList)
        sys.exit(326)
        return False    # shouldn't hit this, but if I want to remove the failure this will remind me
    #
    def CommuteAndSolve(self):
        ''' Commute the arrays one by one and try to solve them '''
        if self.NumberFreeParameters <= 1:
            return  []  # Nothing to do
        self.InitMatrix()
        commuteanswers = []
        for first in range(self.NumberFreeParameters - 1):
            for second in range(first+1, self.NumberFreeParameters):
                product1 = self.MatrixList[first].multiply(self.MatrixList[second])
                product2 = self.MatrixList[second].multiply(self.MatrixList[first])
                commut = product1.add(product2, F.Fraction(-1, 1))
                self.GenerateCommutationEquationsForOne(commut)
                self.newEquationSolver = SolveEquations.SolveEquations(self.NumberFreeParameters, self.commutEquations, Zero.Zero([]))
                self.newEquationSolver.ProcessEquationList()
                newbun = ( CommuteBundle.CommuteBundle(first, second, self.newEquationSolver.ListOfEquations,
                    self.newEquationSolver.chainlist, self.newEquationSolver.zeros) )
                if not self.CheckTheSum(commut, newbun):
                    print('GenerateMatrix:CommuteAndSolve parsed answer does not reproduce the original', first, second, commut, self.commutEquations[-1])
                    sys.exit(326)   # Same as above
                self.commuteSolutions.append(newbun)
        return self.commutEquations  # commuteanswers
        #
    def InitMatrix(self):
        ''' Initialize the MatrixMatch stuff '''
        if self.MatrixMatch is None:
            # Load up which Matrix has non-zero elements in this location
            self.MatrixMatch = []
            temparray = []
            for row in range(self.groupsize):
                temparray.append([F.Fraction(0, 1)] * self.NumberFreeParameters)
            for row in range(self.groupsize):
                self.MatrixMatch.append(copy.deepcopy(temparray))
            # Empty creation done
            for row in range(self.groupsize):
                for column in range(self.groupsize):
                    for i in range(self.NumberFreeParameters):
                        self.MatrixMatch[row][column][i] = self.MatrixList[i].get(row, column)
            # Loaded with Fractions
            F0 = F.Fraction(0, 1)
            # The self.UniqueList approach is not very useful ......................
            self.UniqueList = []
            for matrix in range(self.NumberFreeParameters):
                # find unique entries
                templist = []
                for row in range(self.groupsize):
                    for column in range(self.groupsize):
                        selfcount = 0
                        othercount = 0
                        for m in range(self.NumberFreeParameters):
                            if self.MatrixMatch[row][column][m] == F0:
                                continue
                            if m == matrix:
                                selfcount = selfcount + 1
                            else:
                                othercount = othercount + 1
                        if selfcount == 1 and othercount == 0:
                            templist.append([row, column])  # only non-zero for this matrix
                self.UniqueList.append(templist)
            # In the event, the above was not very useful ......................
    #
    def GenerateCommutationEquationsForOne(self, matrixinstance):
        ''' I have to generate a new set of Equations to be able to handle the
        [A,B] = Sum_i M_i c_i solutions
        I need to create N^2 Equations in M unknowns (N=groupsize, M=NumberFreeParameters)
        Name(0, i, NumberFreeParameters) for the unknowns, Name(NFP, 0, NFP) for the
        constant term
        These are inhomogenous equations
        Sum_i Name(i)Fraction(i)*MatrixList[i] - Names(NNN)Fraction(1)*matrixinstance = 0
        
        Naive "look for single places where commutator matches one and only one MatrixList entry"
        does not work well

        Generate a list of new Equations 
        Called from CommutAndSolve '''
        if len(self.commutEquations) != 0:
            self.commutEquations.clear()    # empty out old stuff
        if len(self.commuteCoeffs) != 0:
            self.commuteCoeffs.clear()      # empty out the old stuff
        #
        for row in range(self.groupsize):
            for column in range(self.groupsize):
                namedummy = N.Name(self.NumberFreeParameters-1, 0, self.NumberFreeParameters)
                # Special names, should almost always be incompatible with the other Names
                eqa = [E.Element(namedummy, matrixinstance.get(row, column).multiply(F.Fraction(-1, 1)))]
                # The above is the "constant term"
                for matrix in range(self.NumberFreeParameters):
                    namemat = N.Name(0, matrix, self.NumberFreeParameters)
                    eqa.append(E.Element(namemat, self.MatrixList[matrix].get(row, column)))
                    # Add on the NumberFreeParameters variables multiplied by the value in the MatrixList's row/col
                self.commutEquations.append(Eq.Equation(eqa))
        #
        # If here, we should have a nice list of NFP^2 Equations in NFP+1 unknowns.
        #
    #
    def commuteSolutionContents(self):
        ''' Return the solutions '''
        return copy.deepcopy(self.commuteSolutions)
