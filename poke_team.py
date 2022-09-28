"""
Contains code of PokeTeam, as well as  Action, and Criterion class scaffold

Defines methods that allow creation of PokeTeams along with their attributes.

"""
from __future__ import annotations

__author__ = "Scaffold by Jackson Goerner, Code by Felicity, Virani, Dylan, Edward"

from multiprocessing.dummy import Array
from tabnanny import process_tokens
from array_sorted_list import ArraySortedList
from random_gen import RandomGen
from sorted_list import ListItem, SortedList
from stack_adt import ArrayStack
from queue_adt import CircularQueue
from bset import BSet
import pokemon

from enum import Enum, auto
from pokemon_base import PokemonBase

class Action(Enum):
    '''Class for enumeration of various possible actions
    
    Complexity:
        O(1)
    '''
    
    ATTACK = auto()  #1
    SWAP = auto()    #2
    HEAL = auto()    #3
    SPECIAL = auto() #4
    
class Criterion(Enum):
    '''Class for enumeration of various possible criterion
    
    Complexity:
        O(1)
    '''
    SPD = auto()    #1
    HP = auto()     #2
    LV = auto()     #3
    DEF = auto()    #4

class PokeTeam:
    """ a team of pokemon

    Attributes:
        team_name (str)         - name of team
        battle_mode (int)       - the battle mode of team (determines ordering, retrieving and returning pokemon)
        ai_type (int)           - the AI of the team, determines what actions the team takes while battling
        
        (following three attributes only used in battle modes 2 and 3)
        criterion (Criterion)   - the attribute used to rank pokemon within the team 
        is_reversed (bool)      - keeps track of whether the team is reversed or not
        criterion_value (int)   - (only battle mode 3) the value to which the pokemon with the 
                                closest criterion value is retrieved
        
        team_numbers (list[int])                - initial team numbers
        poke_team (Stack | Queue | SortedList)  - the actual storage of the pokemon in the team
        times_healed (int)                      - keeps track of the number of times the team has healed
        types_defeated (BSet)                   - used to keep track of the defeated poke_types in a tournament with metas
        
    Complexity:
        unless otherwise stated all methods have a complexity of O(1)
    """
    TEAM_LIMIT = 6

    class AI(Enum):
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()

    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None, criterion_value=None) -> None:
        """ initialises the poke team attributes and validates input
        arg:
            team_name - string of the team name
            team_numbers - list of 5 numbers which should add to be <= TEAM_LIMIT eg [0,2,1,1,0]
            battle_mode - battle mode of the team, should be an int between 0 and 3
            ai_type - AI dictating what actions the team takes
            criterion - Criterion or None
            criterion_value - integer or None        
        
        Complexity:
            O(n) where n where n is the size of the poke team (sum of poke_nums) 
        """
        # checking that team name is a valid string
        assert type(team_name) == str and team_name != "", "team name is invalid"
        self.team_name = team_name

        # checking that battle mode is an int between 0 and 3
        assert type(battle_mode) == int and battle_mode >= 0 and battle_mode <= 3, "battle mode is invalid"
        self.battle_mode = battle_mode
        
        # checking that ai_type is in the AI enum
        assert type(ai_type) == PokeTeam.AI, "AI type is invalid"
        self.ai_type = ai_type

        # checking that criterion is not None when battle mode is 2 or 3
        assert (criterion == None and (battle_mode != 2 and battle_mode != 3)) or (type(criterion) == Criterion and (battle_mode == 2 or battle_mode == 3)), "criterion value is invalid"
        self.criterion = criterion 
        # initialising is_reversed to false
        if battle_mode == 2 or battle_mode == 3:
            self.is_reversed = False
        
        # checking when battle mode is 3, the criterion value inputted is valid, otherwise check if battle mode is not 3 when no criterion value inputted
        assert (type(criterion_value) == int and battle_mode == 3) or (battle_mode != 3), "criterion_value is invalid"
        self.criterion_value = criterion_value

        # checking team_numbers inputted is a valid list with correct length
        assert type(team_numbers) == list and len(team_numbers) == 5, "team numbers are invalid"
        
        # creating the poke_team with different ADTs depending on battle mode
        self.team_numbers = team_numbers
        self.poke_team = self.make_poke_team(team_numbers)
        self.times_healed = 0

        # creating a set for defeated poke (used only in Tournament.linked_list_with_metas)
        self.types_defeated = BSet()
        
    
    
    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs):
        """
        Creates a random team
        Args: 
            team_name (str) - name of team
            battle_mode (int) - 0 to 3
            team_size (int) - number of pokemon to be on the team
            ai_mode (AI) - ai type (1-3)
        Returns: 
            PokeTeam
        """
        # Generate random list
        if team_size == None:
            team_size = RandomGen.randint(PokeTeam.TEAM_LIMIT // 2, PokeTeam.TEAM_LIMIT)
        
        # starts the list with 0 and the team size
        rand_list = [0, team_size]

        # adds four random numbers between 0 and the team size
        for _ in range(4):
            rand_list.append(RandomGen.randint(0, team_size))

        # sorts the list
        rand_list.sort()

        # Attain number of each pokemon based on specified arithmetic
        poke_numbers = [rand_list[i+1] - rand_list[i] for i in range(len(rand_list) - 1)]

        # Set ai to random
        if ai_mode == None:
            ai_mode = PokeTeam.AI.RANDOM

        # picks a random criterion if battle mode is 2 or 3
        if battle_mode == 2 or battle_mode == 3:
            enumList = list(Criterion)
            criterion = enumList[RandomGen.randint(0,3)]
        else:
            criterion = None
        
        return PokeTeam(team_name, poke_numbers, battle_mode, ai_mode, criterion)


    def make_poke_team(self, poke_nums: list[int]) -> ArrayStack | CircularQueue | SortedList:
        """ creates the poke team using different ADTs depending on the battle mode
        :arg:
            poke_nums - a list of 5 numbers in the form: [1,0,2,0,2] indicating
                        how many of the initial pokemon should be in the team

        :complexity: O(n) where n is the size of the poke team (sum of poke_nums)
        """
        # list of initial pokemon classes
        initial_poke = [pokemon.Charmander, pokemon.Bulbasaur, pokemon.Squirtle, pokemon.Gastly, pokemon.Eevee]

        # battle mode 0 -> stack
        if self.battle_mode == 0:  
            # create a stack of team limit capacity
            poke_team = ArrayStack(PokeTeam.TEAM_LIMIT)

            # loop through the initial poke list and create the appropriate number of instances
            for i in range(len(initial_poke) - 1, -1, -1): # iterates backwards -> O(n)
                for _ in range(poke_nums[i]):
                    poke_team.push(initial_poke[i]())

        # battle mode 1 -> queue
        elif self.battle_mode == 1:
            # create a queue of team limit capacity 
            poke_team = CircularQueue(PokeTeam.TEAM_LIMIT)

            # loop through the initial poke list and create the appropriate number of instances
            for i in range(len(initial_poke)):  # O(n)
                for _ in range(poke_nums[i]):
                    poke_team.append(initial_poke[i]())

        # battle mode 2 and 3 -> sorted list
        elif self.battle_mode == 2 or self.battle_mode == 3:
            # create a sorted list of team limit capacity
            poke_team = ArraySortedList(PokeTeam.TEAM_LIMIT)
            
            # loop through the initial poke list and create the appropriate number of instances
            counter = 0
            for i in range(len(initial_poke)):  # O(n)
                for _ in range(poke_nums[i]):
                    new_poke = initial_poke[i]()
                    # set initial index it it's inverse order (so that the first item has the highest value)
                    new_poke.initial_index = PokeTeam.TEAM_LIMIT - counter
                    poke_team.add(self.make_list_item(new_poke))
                    counter += 1

        return poke_team
        
    def make_list_item(self, poke: PokemonBase) -> ListItem:
        '''Creates a list item of the Pokemon based on criterion 
        key is of the form:
            (poke criterion value * 10000) + (inverse poke pokedex index * 100) + (inverse poke initial index)
            so a poke with speed 12 and pokedex 4 and initial index 2 will have a value of 120402
        '''

        # if the list is not reversed the key is negative
        if self.is_reversed:
            multiplier = 1
        else:
            multiplier = -1

        # get the key and create the list item
        key = self.get_criterion_value(poke) * 10000 + poke.get_pokedex_index() * 100 + poke.initial_index
        return ListItem(poke, multiplier * key)


    def return_pokemon(self, poke: PokemonBase) -> None:
        """ returns a pokemon to the poke team 
        complexity:
            best case: O(1) when battle mode is 0 or 1
            worst case: O(logn) when battle mode is 2 or 3 and n is the size of the team
        """
        # first check that the poke hasn't faint
        if poke.is_fainted():
            return

        # adds/pushes/appends the poke to the team
        if self.battle_mode == 0:
            self.poke_team.push(poke) # O(1)

        elif self.battle_mode == 1:
            self.poke_team.append(poke) # O(1)

        elif self.battle_mode == 2 or self.battle_mode == 3: 
            self.poke_team.add(self.make_list_item(poke))  # O(logn)


    def retrieve_pokemon(self) -> PokemonBase | None:
        """
        Returns pokemon based on battlemode and criterion if needed
        Complexity 
            best case: O(1) when battle mode is 0 or 1
            worst case: O(n) when battle mode is 3 and n is the size of the poke team
        """
        # if there are no pokemon left return
        if self.is_empty():
            return 
        
        if self.battle_mode == 0:       # O(1)
            # gets the poke from the top of the stack
            poke = self.poke_team.pop()
            return poke
                
        elif self.battle_mode == 1:      # O(1)
            # gets the poke from the front of the queue
            poke = self.poke_team.serve()
            return poke

        elif self.battle_mode == 2:     # O(logn)
            # gets the first poke in the sorted list and removes that poke
            poke = self.poke_team[0].value
            self.poke_team.delete_at_index(0)
            return poke  

        elif self.battle_mode == 3:     # O(n)
            # gets the poke with the closest value to the given criterion value
            # for each poke the team checks if it has the min dif between its value and the criterion value
            min_index = 0
            # gets the abs dif of the first poke
            min_poke = self.poke_team[min_index].value
            min_dif = abs(self.get_criterion_value(min_poke) - self.criterion_value)
            # loops through the rest of the poke comparing to see if it has the min dif
            for i in range(1, len(self.poke_team)):
                next_poke = self.poke_team[i].value
                dif = abs(self.get_criterion_value(next_poke) - self.criterion_value)
                # Accounts for ties, previous one will be accounted for if equal
                if dif < min_dif:       # O(1) because ALWAYS compare int
                    min_poke = next_poke
                    min_dif = dif
                    min_index = i
            
            self.poke_team.delete_at_index(min_index)   # O(n) worst case
            return min_poke
    
    def special(self):
        """ enacts the special action for each battle mode
        does nothing when battle mode is 3
        :complexity: best/worst case of O(n) where n is the size of the poke team
        """
        # Battle mode 0 -> O(n)
        if self.battle_mode == 0 and len(self.poke_team) > 1:
            # STACK - Swap first and last pokemon 
            temp_stack = ArrayStack(len(self.poke_team)-2)
            first = self.poke_team.pop()
            
            # Iterate over stack until reach last item
            for _ in range(len(self.poke_team) - 1): # O(n)
                poke = self.poke_team.pop()
                temp_stack.push(poke)
            
            last = self.poke_team.pop()

            # Push 'first' as the first element (bottom of stack)
            self.poke_team.push(first)
            
            # Now put everything else back
            for _ in range(len(temp_stack)): # O(n)
                poke = temp_stack.pop()
                self.poke_team.push(poke)
            
            # Now push 'last' as last element (top of stack)
            self.poke_team.push(last)            

        # Battle mode 1 -> O(n)
        elif self.battle_mode == 1:
            # Queue-  swap first and second half and reverse old front half
            temp_stack = ArrayStack(len(self.poke_team))

            # push the first half of the queue onto a temp stack
            for _ in range(len(self.poke_team) // 2): # O(n)
                poke = self.poke_team.serve()
                temp_stack.push(poke)
            
            # append each item of the temp stack to the back of the queue
            for _ in range(len(temp_stack)): # O(n)
                poke = temp_stack.pop()
                self.poke_team.append(poke)

        # Battle mode 2 -> O(n)
        elif self.battle_mode == 2:
            # Sorted list - Reversing order
            temp = ArrayStack(len(self.poke_team))
            for _ in range(len(self.poke_team)): # O(n)
                temp.push(self.poke_team[0].value)
                # Delete at index so we don't have to create another SortedList
                self.poke_team.delete_at_index(0)

            # set is_reversed to the opposite
            self.is_reversed = (self.is_reversed == False)

            # Put Pokemon back into original list
            for _ in range(len(temp)): # O(n)
                poke = temp.pop()
                self.poke_team.add(self.make_list_item(poke))


    def regenerate_team(self):
        """ regenerates the team from the same battle numbers 
        :complexity: best/worst case is O(n) where n is the size of the poke team (sum of poke_nums)
        """
        # remakes the team from the original team numbers
        self.poke_team = self.make_poke_team(self.team_numbers)
        # resets is_reversed and times_healed
        self.is_reversed = False
        self.times_healed = 0

    def __str__(self):
        # example: "Dawn (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Charmander: 9 HP]"
        """ returns a string representation of the poke team
        :complexity: best case is O(n) when battle mode is 0 or 1
                     worst case is O(n^2) when battle mode is 2 or 3
                     where n is the size of the poke team
        """
        # create string with team name and battle mode
        the_str = f"{self.team_name} ({self.battle_mode}): ["
        
        if self.battle_mode == 0: # stack -> O(n)
            length = len(self.poke_team)
            temp_stack = ArrayStack(len(self.poke_team))
            # add poke to string and put into temporary stack
            for i in range(length):
                poke = self.poke_team.pop()
                the_str += str(poke) 
                if i != (length - 1):
                    the_str += ", "
                temp_stack.push(poke)
            # Put pokemon back into original stack
            for _ in range(len(temp_stack)):
                self.poke_team.push(temp_stack.pop())
     
        elif self.battle_mode == 1: # queue -> O(n)
            length = len(self.poke_team)
            for i in range(length):
                # serve each poke and add to string and then append to back of queue
                poke = self.poke_team.serve()
                the_str += str(poke) 
                if i != (length - 1):
                    the_str += ", "
                self.poke_team.append(poke)
        
        elif self.battle_mode == 2 or self.battle_mode == 3: # sorted list -> O(n^2) 
            length = len(self.poke_team)
            # iterate through the length and add the poke at that index to the string
            for i in range(length): # O(n)
                the_str += str(self.poke_team[i].value) # O(n) - n is the length of the linked list
                if i != (length - 1):
                    the_str += ", "
        
        the_str += "]"
        return the_str 


    def is_empty(self) -> bool:
        """ returns whether the poke team is empty """
        return self.poke_team.is_empty()

    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        """ picks an action based on the team's ai mode """

        if self.ai_type == PokeTeam.AI.ALWAYS_ATTACK:
            # always attacks
            return Action.ATTACK
        
        elif self.ai_type == PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE:
            # always selects swap if the opposing pokemon's atacks are super-effective
            their_multiplier = their_pokemon.ATTACK_MULTIPLIERS[their_pokemon.poke_type][my_pokemon.poke_type]
            
            # chooses swap if their multiplier is greater than or equal to 1.5
            if their_multiplier >= 1.5:
                return Action.SWAP
            else:
                # otherwise chooses attack
                return Action.ATTACK

        elif self.ai_type == PokeTeam.AI.RANDOM:
            # randomly picks a valid action
            actions = list(Action)
            # heal option is removed if they have already healed three times
            if self.times_healed >= 3:
                actions.remove(Action.HEAL)

            # returns a random action based on a random index 
            return actions[RandomGen.randint(0,len(actions) - 1)]

        elif self.ai_type == PokeTeam.AI.USER_INPUT:
            # prompts user for input
            user_input = ""

            # Input validation
            while not (user_input.isdigit() and (1 <= int(user_input) <= 4)):
                user_input = input("(1) for attack, (2) for swap, (3) for heal, (4) for special\n")
                # user input is incorrect (not a digit or between range 1-4)
                if not (user_input.isdigit() and (1 <= int(user_input) <= 4)):
                    print("that is not a valid option please try again")
            
            user_input = int(user_input)
            return Action(user_input)

    # bonus method (non-assessed)
    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()

    def get_criterion_value(self, poke) -> int:
        """ returns the corresponding criterion value of the poke based on the team criterion 
        """
        if self.criterion == Criterion.SPD:
            return poke.get_speed()
        
        elif self.criterion == Criterion.HP:
            return poke.get_hp()

        elif self.criterion == Criterion.LV:
            return poke.get_level()

        elif self.criterion == Criterion.DEF:
            return poke.get_defence()
