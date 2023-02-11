''' routine to, given a Table, return a ListOfEquations '''
import sys
import copy
from Builder import Group as G
from Builder import Fraction as F
from Builder import Name as N
from Builder import Element as E
from Builder import Equation as Eq
from Builder import Equivalence as Eqi
from Builder import Zero as Z
from Builder import Chain
# pylint: disable=invalid-name

class SolveEquations:
    ''' Given a group size, list of Equations, and a Zero, solve the system
    The ListOfEquations WILL be modified, as will the Zero object '''
    def __init__(self, groupSize, ListOfEquations, zeros):
        ''' Load initial list of equations, generated elsewhere '''
        if not isinstance(zeros, Z.Zero):
            print('SolveEquations was not given a Zero')
            sys.exit(350)
        if not isinstance(ListOfEquations, list):
            print('SolveEquations was not given a *list* of Equations')
            sys.exit(351)
        for entry in ListOfEquations:
            if not isinstance(entry, Eq.Equation):
                print('SolveEquations was not given a list of *Equations*')
                sys.exit(352)
        if not isinstance(groupSize, int):
            print('SolveEquations was not given an integer group size')
            sys.exit(353)
        if groupSize < 0:
            print('SolveEquations groupSize is negative')
            sys.exit(354)
        self.groupSize = groupSize
        self.keyclusters = []   # list of keys that have been processed already
        self.chainlist = []
        self.zeros = zeros  # This WILL be modified!
        self.ListOfEquations = ListOfEquations  # This WILL be modified!
        self.ListOfEquivalences = [] # load this later
    #
    def bulkInfo(self):
        ''' Return text of basic info '''
        stemp = ''
        stemp = stemp + 'SolveEquations: List of Equations has ' + str(len(self.ListOfEquations)) + ' Equations'
        stemp = stemp + '\nSolveEquations: has ' + str(len(self.chainlist)) + ' Chains'
        stemp = stemp + '\nSolveEquations: has ' + str(self.zeros.count()) + ' zeros in the Zero chain\n'
        return stemp
    #
    def ProcessEquationList(self):
        ''' Master routine '''
        #
        self.cleanUpDups()
        oldlen = 1
        newlen = -1
        while oldlen != newlen:
            oldlen = len(self.ListOfEquations)
            self.reduceZeros()
            self.cleanUpDups()
            self.findZeros()
            newlen = len(self.ListOfEquations)
        answer = -1
        answer2 = self.removeTwos()
        self.cleanUpDups()
        bigkeylist = self.getSameKey()
        if bigkeylist is not None:
            answer = self.compareSameTwoKey(bigkeylist)
        for eq in self.ListOfEquations:
            eq.reduce(self.chainlist)
        self.cleanUpDups()
        #
        if answer == Chain.Chain.ZEROED:
            # Some work to do?
            for eq in self.ListOfEquations:
                eq.reduce(self.zeros)
            #
            self.cleanUpDups()
            newbigkeylist = self.getSameKey()
            if newbigkeylist is not None:
                answer = self.compareSameTwoKey(newbigkeylist)
                answer2 = self.removeTwos()
                self.cleanUpDups()
                return self.ListOfEquations, self.zeros, newbigkeylist, answer, answer2
        answer2 = self.removeTwos()
        self.cleanUpDups()
        self.findZeros()
        unac, tot = self.unaccounted()
        self.cleanChains()
        if unac == 0 and len(self.ListOfEquations) > 0:
            self.reduceEquationsToEquivalences()
            #self.turnEquationsToEquivalence()
        #else:
        #    print('SolveEquations:ProcessEquationList: unaccounted, listofequations', unac, self.ListOfEquations, self.chainlist)
        return self.ListOfEquations, self.zeros, bigkeylist, answer, answer2
    #
    def cleanUpDups(self):
        ''' Get rid of duplicates '''
        for i in range(len(self.ListOfEquations)-1, -1, -1):
            for j in range(i):
                if self.ListOfEquations[i] == self.ListOfEquations[j]:
                    self.ListOfEquations.pop(i)
                    break
        #
    #
    def reduceZeros(self):
        ''' Remove zero elements '''
        for eq in self.ListOfEquations:
            eq.reduce(self.zeros)
        #
    #
    def cleanChains(self):
        ''' Get rid of Chains that are zero '''
        listofbad = []
        numchain = len(self.chainlist)
        for ic, chain in enumerate(self.chainlist):
            for ele in chain.contents():
                if not self.zeros.present(ele):
                    continue
                # if here, the Chain contains a zero--so all are zero
                # Add them to the Zero object
                self.zeros.add(chain.contents())
                listofbad.append(ic)
                break
            #
        # Get the zero Chains out of here
        if len(listofbad) > 0:
            listofbad.reverse()
            for ic in listofbad:
                self.chainlist.pop(ic)
        # Done.
    #
    def findZeros(self):
        ''' Remove zero elements '''
        for i in range(len(self.ListOfEquations)-1, -1, -1):
            if self.ListOfEquations[i].count() > 1:
                continue
            if self.ListOfEquations[i].isZero():
                self.ListOfEquations.pop(i)
                continue
            self.zeros.add(self.ListOfEquations[i].key().contents()[0])
            self.ListOfEquations.pop(i)
        #
    # Next put something together that looks at Keys for the equations and
    # groups those with the same Key together, for Chain-ing or Equivalence-ing
    # That's the easy bit of the solution system.
    #
    def getSameKey(self):
        ''' Find the largest, or first if a tie, collection of Equations with
        the same key signature, that has not already been processed (listed in
        self.keyclusters) '''
        localKeyDict = {}
        # Load our dictionary with counts of the number of unprocessed keys
        for entry in self.ListOfEquations:
            curkey = entry.key()
            if curkey in self.keyclusters:   # already investigated
                continue
            if curkey.tuple() in localKeyDict:
                localKeyDict[curkey.tuple()] = localKeyDict[curkey.tuple()] + 1
            else:
                localKeyDict[curkey.tuple()] = 1
        #
        if len(localKeyDict) == 0:
            return None     # Everything has already been processed!
        kmax = -1
        for lkey in localKeyDict:
            if localKeyDict[lkey] > kmax:
                kmax = localKeyDict[lkey]
                kkey = lkey # This is a tuple, not a list or Key
        # Since the dict is not empty there has to be a "maximum" or tied count.
        # But, if the maximum is 1, there are no duplicate keys remaining to be
        # combined/compared, and we're done
        if kmax == 1:
            #print('kmax = 1')
            return None
        #
        eqListSameKey = []
        for n, entry in enumerate(self.ListOfEquations):
            if not entry.key().tuple() == kkey:
                continue
            eqListSameKey.append(entry)
        return eqListSameKey
    #
    def makeChain(self, other):
        ''' If the equation has 2 elements, make it into a Chain and return that, else return None '''
        if not isinstance(other, Eq.Equation):
            print('SolveEquations:makeChain wants an Equation')
            sys.exit(355)
        if other.count() != 2:
            return None
        return Chain.Chain([copy.deepcopy(other.elementlist[0]), other.elementlist[1].multiply(F.Fraction(-1, 1))])
    #
    def compareSameTwoKey(self, eqListSameKey):
        ''' 2-Element equations and try to combine them '''
        if not isinstance(eqListSameKey, list):
            print('SolveEquations:compareSameTwoKey wants a *list* of Equations of 2 elements')
            sys.exit(356)
        templist = []
        for entry in eqListSameKey:
            if not isinstance(entry, Eq.Equation):
                print('SolveEquations:compareSameTwoKey wants a list of *Equation*s')
                sys.exit(357)
            if entry.count() == 2:
                templist.append(entry)
        #
        if len(templist) == 0:
            return Chain.Chain.NOOP
        for i in range(len(templist)-1, -1, -1):
            for j in range(i):
                if templist[i] == templist[j]:
                    templist.pop(i)
        #
        if len(templist) >= 2:
            # The Equations are distinct, and if we have more than 1 we have
            # formal solutions, which in this case will demand that both Elements
            # must be zero.
            self.keyclusters.append(templist[0].key())
            temp = templist[0].contents()
            self.zeros.add(temp)
            # Now get rid of the zero'd equations
            for i in range(len(self.ListOfEquations)-1, -1, -1):
                for eq in templist:
                    if eq == self.ListOfEquations[i]:
                        self.ListOfEquations.pop(i)
                        break
            return Chain.Chain.ZEROED
        #
        self.chainlist.append(self.makeChain(templist[0]))
        return Chain.Chain.MADE
    #
    def removeTwos(self):
        ''' Run through all 2-Element Equations and make them into Chains
        Then see which can be consolidated. '''
        origlen = len(self.ListOfEquations)
        origch = len(self.chainlist)
        origzero = self.zeros.count()
        #
        if len(self.ListOfEquations) == 0:
            return Chain.Chain.NOOP
        for eq in self.ListOfEquations:
            if eq.isZero():
                continue
            if eq.count() != 2:
                continue
            #
            self.chainlist.append(Chain.Chain([copy.deepcopy(eq.elementlist[0]), eq.elementlist[1].multiply(F.Fraction(-1, 1))]))
        #
        chlen = len(self.chainlist)
        didSomething = False
        for i in range(chlen - 1):
            if self.chainlist[i].isUsedUp():
                continue
            for j in range(i+1, chlen):
                answer = self.chainlist[i].merge(self.chainlist[j])
                if answer != Chain.Chain.NOOP:
                    didSomething = True
        if not didSomething:
            return Chain.Chain.NOOP
        for i in range(len(self.chainlist)-1, -1, -1):
            if self.chainlist[i].isUsedUp():
                self.chainlist.pop(i)
        #
        # Now look for the zeros and load up our zero array
        for i in range(len(self.chainlist)-1, -1, -1):
            if not self.chainlist[i].isZero():
                continue
            key = self.chainlist[i].Key()
            self.zeros.add(key.contents())
            self.chainlist.pop(i)
        #
        # As long as we're in the neighborhood, redo the zeros
        for i in range(len(self.ListOfEquations)-1, -1, -1):
            self.ListOfEquations[i].reduce(self.zeros)
            if self.ListOfEquations[i].isZero():
                self.ListOfEquations.pop(i)
        newlen = len(self.ListOfEquations)
        newch = len(self.chainlist)
        newzero = self.zeros.count()
        #
        if newlen == origlen and newch == origch and newzero == origzero:
            return Chain.Chain.NOOP
        return Chain.Chain.MERGED
    #
    def giveKeys(self):
        ''' Return a list of the Keys for the Equations '''
        templ = []
        for eq in self.ListOfEquations:
            templ.append(eq.key())
        return templ
    #
    def unaccounted(self):
        ''' Return a count of all the variables (Names) in Equations which are NOT
        in Chains and in Zero.  Also return the sum of the three, as a check '''
        templ = []
        for ch in self.chainlist:
            newlist = ch.Key().contents()
            for el in newlist:
                if el not in templ:
                    templ.append(el)
        chaincount = len(templ)
        zerocount = self.zeros.count()
        templ.extend(self.zeros.contents())
        templ.sort()
        #
        tempe = []
        for eq in self.ListOfEquations:
            newlist = eq.key().contents()
            for el in newlist:
                if el not in tempe:
                    tempe.append(el)
        tempe.sort()
        eqcount = len(tempe)
        stempl = set(templ)
        overlap = [value for value in tempe if value in stempl]
        notoverlappingcount = eqcount - len(overlap)
        total = chaincount + zerocount + notoverlappingcount
        return notoverlappingcount, total
    #
    def GiveChains(self):
        ''' Return a pointer to the Chains within.  Not meant to be mutable '''
        return self.chainlist
    def GiveEquivalences(self):
        ''' Return a pointer to the Equivalences within.  Not meant to be mutable '''
        return self.ListOfEquivalences
    #
    # If the notoverlapping count is 0, we can use each Equation to create an
    # Equivalence, provided this is actually possible to do.
    # A) How can I tell whether there is a way to pick such a non-overlapping set
    # of targets, given the set of Equations?
    # B) What does it mean if I can't?  What should I do?
    #
    def turnEquationsToEquivalence(self):
        ''' Only call this if self.unaccounted() == 0.  Try to make different targets
        for each Equation in self.ListOfEquations '''
        # 24-Jan-2023.  Actually,  different targets is not always going to be ideal.
        # It is more useful, at least sometimes, to find two Equations with potentially
        # the same target, and combine them to solve for the target in one and eliminate
        # it in the other.  At the end of the day, one can wind up with equivalent
        # Equivalences, which can be simplified.
        if len(self.ListOfEquations) == 0:
            print('SolveEquations:turnEquationsToEquivalence should have at least one Equation')
            sys.exit(358)
        if len(self.ListOfEquations) == 1:
            # Easy.  Just solve for the first element in the only Equation
            self.ListOfEquivalences = [self.ListOfEquations[0].formalSolve(self.ListOfEquations[0].contents()[0])]
            return
        #
        # OK, now some BFI stuff
        EqInfo = []
        NameTemp = {}
        NameInfo = {}
        TempListOfEquivalences = []
        for eq in self.ListOfEquations:
            EqInfo.append([eq.count(), False])
            for el in eq.contents():
                if el.name not in NameTemp:
                    NameTemp[el.name] = 1
                else:
                    NameTemp[el.name] = NameTemp[el.name] + 1
        #
        for key in NameTemp:
            NameInfo[key] = [NameTemp[key], False]
            #print(' NameInfo[key]', key, NameInfo[key])
        #
        remaining = len(self.ListOfEquations)
        while remaining > 0:
            mineqsize = 10000000    # Yes, it is hardwired, but for groups big enough for this to matter this is too slow
            mineqnumber = -1
            for i in range(len(self.ListOfEquations)):
                if not EqInfo[i][1] and EqInfo[i][0] < mineqsize:
                    mineqsize = EqInfo[i][0]
                    mineqnumber = i
            #
            lowuse = 10000000
            minelemnumber = -1
            for i, elem in enumerate(self.ListOfEquations[mineqnumber].elementlist):
                ename = elem.name
                if not NameInfo[ename][1] and NameInfo[ename][0] < lowuse:
                    lowuse = NameInfo[ename][0]
                    minelemnumber = i
            #
            if minelemnumber < 0:
                print('SolveEquations:turnEquationsToEquivalences could not find unused Name to solve for')
                print('Algorithm is stupid simple.', len(self.ListOfEquations))
                print('NEED to see if how many of these equations turn to 0!!')
                print(EqInfo)
                print('======')
                print(NameInfo)
                print('######')
                for x in self.ListOfEquations:
                    print(x)
                sys.exit(359)
            elem = self.ListOfEquations[mineqnumber].contents()[i]
            ename = elem.name
            TempListOfEquivalences.append(self.ListOfEquations[mineqnumber].formalSolve(ename))
            EqInfo[mineqnumber][1] = True
            a = NameInfo[ename][0]
            NameInfo[ename] = [a, True]
            remaining = remaining - 1
        #
        # OK, if that didn't barf it gave us a unique list.  I use the Temp array because I
        # may need to roll back things if the stupid algorithm above wedges.
        self.ListOfEquivalences = copy.deepcopy(TempListOfEquivalences)
    #
    def GiveEquations(self):
        ''' Return the ListOfEquations   potentially mutable '''
        return self.ListOfEquations
    def GiveZeros(self):
        ''' Return the Zero object:  OK if this is modified '''
        return self.zeros
    #
    def countInstancesOfChainInEquations(self):
        ''' Do what it says:  return an array of the number of instances of each
            Chain (any entry) in all of the Equations, in the order of the chainlist '''
        chainelementcount = [0]*len(self.chainlist)
        if len(self.ListOfEquations) == 0:
            return chainelementcount
        #
        for ic, chain in enumerate(self.chainlist):
            for entry in chain.contents():
                for equa in self.ListOfEquations:
                    if equa.present(entry.name):
                        chainelementcount[ic] = chainelementcount[ic] + 1
        return chainelementcount
    #
    def reduceEquationsToEquivalences(self):
        ''' Make an Equivalence of each Equation, methodically replacing instances
        in the remaining ones.  This REMOVES Equations from the list.  This
        is not the same as earlier behavior, but I think it will be OK. '''
        # This ASSUMES that the ListOfEquations has been simplified so that
        # there is no more than a single representative from any Chain in each
        # Equation.
        oldlen = len(self.ListOfEquations)
        newlen = -1
        while newlen != oldlen:
            nextequiv = self.doNextReduceEquationToEquivalence()
            if nextequiv is not None:
                self.ListOfEquivalences.append(nextequiv)
            if newlen != -1:
                oldlen = newlen
            newlen = len(self.ListOfEquations)
        #
    def doNextReduceEquationToEquivalence(self):
        ''' Do a single pass to find the next Equation to transform and apply
        the Equivalence to all the rest of the Equations to which this applies,
        and discard the Equation it came from '''
        chaincount = self.countInstancesOfChainInEquations()
        # Chains that don't appear are either free Chains or already accounted for
        if len(self.ListOfEquations) == 0:
            return None
        mincount = 3 * len(chaincount)
        minsize = mincount
        for ic, ch in enumerate(chaincount):
            if ch == 0:
                continue
            if ch < minsize:
                mincount = ic
                minsize = ch
        if mincount > 1 + len(chaincount):
            # There aren't any non-zero entries, nothing to do
            return None
        if minsize == 1:
            # Just picking the first, entries from this Chain don't appear
            # anywhere else, so just make an Equivalence for the Equation
            # that contains a Name from this Chain.
            for ele in self.chainlist[mincount].contents():
                for ieq, eq in enumerate(self.ListOfEquations):
                    if eq.present(ele):
                        #return copy.deepcopy(eq.formalSolve(ele))
                        equiv = eq.formalSolve(ele)
                        self.ListOfEquations.pop(ieq)
                        self.reduceEquivalences(equiv)
                        return copy.deepcopy(equiv)
            # Easy as pie.  I could optimize this, but this probably isn't a bottleneck
        # If here, each Chain has representatives in more than one Equation.  Thus,
        # we need to create an Equivalence, replace that for the other representatives,
        # and simplify/consolidate all the Equations.  And then return the Equivalence
        # Pick the first.  I might do better to pick the shortest Equation, but don't
        # optimize prematurely
        # This is the first Chain with the minimum count.
        pairs = []
        for ele in self.chainlist[mincount].contents():
            for ie, eq in enumerate(self.ListOfEquations):
                if eq.present(ele):
                    pairs.append([ele, ie])
        # Now I should have a list with length mincount, thanks to the assumption
        # that the ListOfEquations has been simplfied before calling this tree.
        newequiv = self.ListOfEquations[pairs[0][1]].formalSolve(pairs[0][0])
        for ie, eq in enumerate(self.ListOfEquations):
            if ie == pairs[0][1]:
                continue    # This is the one the Equivalence was made from
            # Now, which Element in the Equation needs solution?
            # Problem:  the "replace" method assumes that the target is the
            # Element that needs to be replaced.  I hate to create a new
            # Equivalence just for the purpose, but I hate to duplicate code too.
            # Duplicate the code, there are enough differences
            for ele in self.chainlist[mincount].contents():
                if eq.present(ele):
                    # Two Fractions:  the scale of the Element in the Chain
                    # and the scale of the Element in the Equation
                    eqEle = eq.giveElement(ele)
                    scaleEle = eqEle.fraction
                    scaleCh = ele.fraction.invert()
                    scale = scaleCh.multiply(scaleEle)
                    for entry in eq.elementlist:
                        if entry == eqEle:
                            entry.muteforceZero()
                            for oentry in newequiv.collection:
                                eq.elementlist.append(oentry.multiply(scale))
                            eq.reduce(self.zeros)  # Try to clean up the Equation
        # OK, done going through the Equations.
        # Now clean up.
        # Discard the Equation that turned into an Equivalence
        self.ListOfEquations.pop(pairs[0][1])
        self.cleanUpDups()
        self.reduceEquivalences(newequiv)
        return copy.deepcopy(newequiv)
    #
    def reduceEquivalences(self, equiv):
        ''' Take the given NEW!!! Equivalence and plug it into the older ones.
        Then see if any reduce/become trivial or zero, and pop those out. '''
        if len(self.ListOfEquivalences) == 0:   # Nothing to do
            return
        if not isinstance(equiv, Eqi.Equivalence):
            print('SolveEquations:reduceEquivalences was not given an Equivalence')
            sys.exit(360)
        zerolist = []
        for inum, entry in enumerate(self.ListOfEquivalences):
            if entry.present(equiv.target):
                entry.replace(equiv)
                entry.cleanup()
                #print(entry)
                if entry.isZero():
                    zerolist.append(inum)   # delete this later
        if len(zerolist) == 0:
            return
        zerolist.reverse()
        for inum in zerolist:
            self.ListOfEquivalences.pop(inum)
    #
