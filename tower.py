"""Implements BattleTower and BattleTowerIterator class and respective methods"""

from __future__ import annotations
from lib2to3.pgen2.token import EQUAL

from poke_team import PokeTeam, Criterion
from battle import Battle
from random_gen import RandomGen
from linked_lists import LinkedList
from array_sorted_list import ArraySortedList
from referential_array import ArrayR
 
class BattleTower:
    """ a gauntlet run for a poke teams to battle through multiple trainers 
    
    attributes:
        battle (Battle) - the battle instance with which all battles are conducted
        my_team (PokeTeam) - the poke team that faces all of the tower teams
        tower_teams (LinkedList[ArrayR[PokeTeam, int]]) - the randomly generated poke teams the player verses
                    tower_teams is a linked list of arrays containing the poke team and their lives

    complexity:
        unless otherwise stated all methods have a best/worst case complexity of O(1)
    """
    
    def __init__(self, battle: Battle|None=None) -> None:
        '''
        Set battle passed as self.battle instance variable, create our own battle if none is passed
        Instantiate my_team and tower_teams as instance variables

        Arg:
            battle - Battle object
        '''
        # if given a battle
        if type(battle) == Battle:
            self.battle = battle
        # if not given a battle create own battle
        else:
            self.battle = Battle()

        # create instance variables and initialise them to none
        self.my_team = None
        self.tower_teams = None

    
    def set_my_team(self, team: PokeTeam) -> None:
        '''Sets the team that will be fighting through tower'''

        # Checks if team passed is a PokeTeam
        assert type(team) == PokeTeam, 'invalid PokeTeam'
        self.my_team = team
    
    def generate_teams(self, n: int) -> None:
        ''''Generates n teams that will be used for the battle tower
            
            args: 
                n = number of teams to be created
            
            Complexity: 
                best/worst case of O(n^2) where n is the number of teams to be generated in the battle tower
        '''
        # check that there is a valid number of teams given
        assert type(n) == int and n > 0, 'invalid number of teams'
        
        teams = LinkedList()
        
        for i in range(n):  # O(n)
            team_pair = ArrayR(2) # [Team, Num Lives]
            # generate random battle mode
            battle_mode = RandomGen.randint(0,1)
            # generate random team 
            team_pair[0] = PokeTeam.random_team('Team ' + str(i + 1), battle_mode)
            # generate a random number of lives between 2 and 10
            team_pair[1] = RandomGen.randint(2,10)
            # add the team/lives to the end of the linked_list
            teams.insert(len(teams), team_pair)     # O(n)

        self.tower_teams = teams

    def __iter__(self):
        """ creates an instance of the battle tower iterator """
        # first checks that the tower has appropriate my_team and tower_team values
        assert type(self.my_team) == PokeTeam and type(self.tower_teams) == LinkedList, "cannot create an iterator"
        return BattleTowerIterator(self.battle, self.my_team, self.tower_teams)


class BattleTowerIterator:
    """ iterator for iterating through the Battle Tower 
    attributes:
        battle (Battle)     - battle used for all battling throughout the tournament
        my_team (PokeTeam)  - the poke team playing against the tower team
        tower_teams (LinkedList) - list of teams to be played against
        my_team_lost (bool) - used to check whether my team has lost in order to raise StopIteration
    
    complexity:
        unless otherwise stated all methods have a best/worst complexity of O(n)
    """

    def __init__(self, battle: Battle, my_team: PokeTeam, tower_teams: LinkedList[ArrayR[PokeTeam, int]]):
        """ initialises a run though of the tower
            Arg validation performed in BattleTower __iter__
        """
        self.battle = battle
        self.my_team = my_team
        self.tower_teams = tower_teams
        self.my_team_lost = False

    def __iter__(self):
        return self
    
    def __next__(self) -> tuple(int, PokeTeam, PokeTeam, int):
        """ performs one battle in the tower
        
        complexity:
            best/worst case of O(n + B) where n is the number of tower teams
            and B is the complexity of the battle
        
        returns:
            the result of the battle, the state of the teams after the battle
            and the number of lives left for the tower team
         """
        # raises the stop iteration error when the tower teams is empty or the player has lost
        if self.tower_teams.is_empty() or self.my_team_lost:
            raise StopIteration

        # Retrieves front team from tower_teams
        tower_team = self.tower_teams[0]
        self.tower_teams.delete_at_index(0)         # O(1) (first index = no iterating)

        # regenerate teams and battle
        self.my_team.regenerate_team()
        tower_team[0].regenerate_team()
        res = self.battle.battle(self.my_team, tower_team[0])  # O(B)
        # If tower_team lose/draw, lose one life
        if res != 2: 
            tower_team[1] -= 1

        # If lives > 0, then append to end of the linked list
        if tower_team[1] > 0:
            self.tower_teams.append(tower_team)  # O(n)
        
        # once my team has lost, stop the tower
        if res == 2:
            self.my_team_lost = True
           
        # return the tuple 
        # (result, state of my team, state of tower team, tower team lives)
        return (res, self.my_team, tower_team[0], tower_team[1])

    def avoid_duplicates(self):
        """ 
        Removes all currently alive trainers from battle tower with multiple of the same type pokemon
        Comp: best/worst is O(N*P): N = num trainers remaining, P = limit on num pokemon per team
        """
        # set starting values
        current_team = self.tower_teams.head
        prev = None

        # iterates from node to node until it reaches the end
        while current_team != None: # O(N)
            has_dupes = False
            # Access number of pokemon in teams (linked list)
            for i in current_team.item[0].team_numbers: #O(P)
                # If Node in middle
                if i > 1 and prev != None: 
                    # # Link previous node to next (making current_team node redundant)
                    prev.next = current_team.next
                    self.tower_teams.length -= 1
                    has_dupes = True
                    break

                # if Node at start, set the head to the next node
                elif i > 1 and prev == None:
                    self.tower_teams.head = current_team.next
                    self.tower_teams.length -= 1
                    has_dupes = True
                    break
            # if there is no dupe prev becomes the current value otherwise prev stays the same
            if not has_dupes:
                prev = current_team

            # reassign current team
            current_team = current_team.next

            
    def sort_by_lives(self):
        '''Sort remaining trainers by lives, then name (alphabetical)
        algorithm: bubble sort
        Complexity:
            worst case of O(N^2 * comp) where n is the number of tower teams and 
                        comp is is the cost of comparison between team names
            best case of O(n * comp) where the list is already sorted by lives
        '''
        n = len(self.tower_teams)

        # iterate 1 less each time
        for i in range(n-1, 0, -1): # O(n)
            swapped = False
            # Current team is first
            current_team = self.tower_teams.head
            # No previous (at start)
            prev = None
            for _ in range(i): # O(n)
                # Create next team
                next_team = current_team.next

                # Check if there's no next item (current item = last item)
                if next_team == None:
                    break

                # Check current teams LIVES greater than next teams LIVES
                if current_team.item[1] > next_team.item[1] or \
                    (current_team.item[1] == next_team.item[1] and current_team.item[0].team_name > next_team.item[0].team_name):
                    # ^^ If lives are equal, swap alphabetically -> O(comp)

                    # swap current item and the one after (next_team)
                    if prev == None:
                        temp = self.tower_teams.head
                        self.tower_teams.head = current_team.next
                    else:
                        temp = prev.next
                        prev.next = current_team.next

                    current_team.next = next_team.next
                    next_team.next = temp

                    swapped = True

                # Step current and previous team
                elif current_team != None:  
                    prev = current_team
                    current_team = current_team.next

            # Early exit, break if no two elems were swapped by inner loop
            if not swapped:
                break
