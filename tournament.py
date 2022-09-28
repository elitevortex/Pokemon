"""
Implementation of the Tournament class and its respective methods
"""

from __future__ import annotations

__author__ = "Scaffold by Jackson Goerner, Code by Felicity, Virani, Dylan, Edward"

from cgi import test
from re import template
from poke_team import PokeTeam
from pokemon_base import PokemonBase
from queue_adt import CircularQueue
from random_gen import RandomGen
from bset import BSet
from referential_array import ArrayR
from poke_team import PokeTeam
from battle import Battle
from linked_lists import LinkedList
from stack_adt import ArrayStack


class Tournament:
    """ randomly generated teams face off against one another in a tournament

    Attributes:
        battle (Battle)             - A Battle instance between two PokeTeams
        battle_mode (int)           - the type of battle from 0-3 which determines team's structuring 
        tourn_queue (CircularQueue) - queue where the teams and pluses are stored before their first battle
        tourn_stack (ArrayStack)    - stack where poketeams are stored when they are in the midst of the tournament
    
    Complexity:
        unless otherwise stated all methods have a best/worst case complexity of O(1)
    """

    def __init__(self, battle: Battle|None=None) -> None:
        '''Initialises Tournament instance variables and validates input
        
        arg:
            battle - a Battle instance

        returns:
            None
        '''
        # if a battle instance is passed in
        if type(battle) == Battle:
            self.battle = battle
        else:
            # if battle not passed in, a battle instance is created
            self.battle = Battle()
        
        # tourn instances initialised to None
        self.battle_mode = None
        self.tourn_queue = None
        self.tourn_stack = None

    def set_battle_mode(self, battle_mode: int) -> None:
        '''Sets the battle mode
        
        args:
            battle_mode - an integer from 0-3

        returns:
            None
        '''
        # checks that the battle mode is a valid integer
        assert type(battle_mode) == int and (battle_mode == 0 or battle_mode == 1), "battle mode is invalid"
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool: 
        '''Checks that a tournament is valid
        ie. number of teams and '+' matches so that one winner is produced

        args:
            tournament_str - string of postfix notation containing temas and '+' 
                            symbol- signiying a battle
                            
        complexity: 
            best/worst case is O(n) where n is the number of items in the split tournament string
        
        returns:
            Boolean
        '''
        
        # example string:
        # "Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"
        
        # Check empty string
        if tournament_str == "":
            return False

        # split the string by space to get the team names and pluses
        words = tournament_str.split(' ')

        temp_stack = ArrayStack(len(words))
        # Push teams onto stack, pop one team (the loser) ('+' means we have a battle pair)
        for item in words: # O(n)
            if item != "+":
                temp_stack.push(item)
            else:
                # check first if stack is empty
                if temp_stack.is_empty():
                    return False
                temp_stack.pop()
        
        # Valid stack has one team left (the winner)
        if len(temp_stack) == 1:
            return True
        return False
            

    def is_balanced_tournament(self, tournament_str: str) -> bool:
        # 1054 only
        """ determines where a tournament string is balanced or not
        arg:
            tournament_str (str) - tournament string in postfix notation
        Complexity:
            best/worst case: O(n) where n is the number of teams and pluses in the tournament_string
        """
        # example string:
        # "Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"
        
        # first checks that the string is even a valid tournament
        if not self.is_valid_tournament(tournament_str):            # O(n)
            return False

        # split the string by space to get the team names and pluses
        words = tournament_str.split(' ')

        # store all in a queue
        teams_and_pluses = CircularQueue(len(words))
        for item in words: # O(n)
            if item != "+":
                # each team name is stored in an array with the team name and then how many battles they've fought
                item_array = ArrayR(2)
                item_array[0] = item
                # the number of times the team has played
                item_array[1] = 0
                teams_and_pluses.append(item_array)
            else: # the item is a "+"
                teams_and_pluses.append(item)

        temp_stack = ArrayStack(len(words))
        
        # Push teams onto stack, pop one team (the loser) and check that they have fought the same number of battles
        for _ in range(len(teams_and_pluses)):
            # get the next item in the queue
            item = teams_and_pluses.serve()
            if item != "+":
                temp_stack.push(item)
            else:
                # pop both teams off the stack
                loser = temp_stack.pop()
                winner = temp_stack.pop()

                # check that both teams have won the same amount of battles
                if loser[1] != winner[1]:
                    return False
                
                # increment the winner's battles by 1
                winner[1] += 1
                temp_stack.push(winner)
        return True
        
        
    def start_tournament(self, tournament_str: str) -> None:
        '''Generate teams, doesn't play games
        
        args:
            tournament_str - string of postfix notation containing temas and '+' 
                            symbol- signiying a battle 

        Complexity:
            best/worst case: O(n) where n is the number of teams and pluses in the tournament_string

        returns:
            None
        '''
        # Validate tournament string
        if not self.is_valid_tournament(tournament_str):        # O(n)
            raise ValueError("tournament string is invalid")
        
        # split the string by space to get the team names and pluses
        tourn_str_split = tournament_str.split(' ')

        # for each item in the string create a poke team or add the "+"
        item_queue = CircularQueue(len(tourn_str_split))
        for item in tourn_str_split:        # O(n)
            if item != "+":
                item_queue.append(PokeTeam.random_team(item, self.battle_mode))
            else:
                item_queue.append(item)

        # set the instance variables of the tourn queue and stack
        self.tourn_queue = item_queue
        self.tourn_stack = ArrayStack(len(tourn_str_split))
        

    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        '''Simulates a single battle
        Return: None if no games remain
        Complexity: 
            best: O(B + comp) - where the plus is the first item in the queue
            worst: O(B + comp + n)  where
                B = complexity of running battle,
                n is the number of items in the tourn string (teams and pluses)
                comp is the cost of comparison of team names
        '''
        
        # if the queue is empty the tournament is done
        if len(self.tourn_queue) == 0:
            return 
        
        # adds each poke team to the stack until a plus is reached
        tourn_item = self.tourn_queue.serve()
        while tourn_item != "+":                # worst O(n), best O(1)
            self.tourn_stack.push(tourn_item)
            tourn_item = self.tourn_queue.serve()
        
        # once a plus is reached, battle the top two teams on the stack
        team2 = self.tourn_stack.pop()
        team1 = self.tourn_stack.pop()
        res = self.battle.battle(team1, team2)                  # O(B)

        # if there is a draw the higher lexographical name wins
        if res == 0:
            if team1.team_name >= team2.team_name:      # O(comp)
                res = 1
            else:
                res = 2

        # Push the winning team back onto the stack:
        if res == 1:
            self.tourn_stack.push(team1)
            
        else:
            self.tourn_stack.push(team2)

        # return both poke teams and the result of battle
        return (team1, team2, res)


    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        '''Returns the reverse ordering of the matches play
        ie. final match first => all matches lower bracket => all matches upper bracket
            (recursive)

        Complexity:
            best/worst case is the complexity of advancing the tournament (worst case: O(B + comp + n))
        '''
        l = LinkedList()
        while True:
            # advance tournament and check that it hasn't finished
            res = self.advance_tournament()         
            if res is None:
                break
            # insert both poke teams to start of a linked list
            l.insert(0, (res[0], res[1]))
        return l
    
    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        """ returns a linked list of poke types that were present in past battles but not in the current 
        :complexity: best/worst case O(M*A) where M is the number of battles to be played
                                            and A is the complexity of advancing the tournament
        """
        linked_metas = LinkedList()
        
        while True:                             # O(M) where M is the number of battles
            # advance the tournament and check that it hasn't finished
            res = self.advance_tournament()

            if res is None: 
                break

            team1, team2, res = res

            # create a set to house the current types
            current_types = BSet(len(PokemonBase.PokeType))

            # getting the poke types of the two teams that just battled
            for i in range(len(team1.team_numbers)):  # O(1) team_number list is always 5      
                if team1.team_numbers[i] > 0:
                    current_types.add(i+1) # stored as i+1 because can't put zero in a set

            for i in range(len(team2.team_numbers)):
                if team2.team_numbers[i] > 0:
                    current_types.add(i+1)

            # get the types that are in the defeated poke but not in the current battle
            defeated_types = team1.types_defeated.union(team2.types_defeated)
            type_dif = defeated_types.difference(current_types)

            # transfer types to a list
            type_dif_list = list()
            for i in range(len(PokemonBase.PokeType)): 
                if (i+1) in type_dif:
                    type_dif_list.append(PokemonBase.PokeType(i).name)
            
            # add the tuple to the start of the linked list
            linked_metas.insert(0, (team1, team2, type_dif_list))

            # added the defeated teams types to the defeated poke types set of the winning team
            if res == 1:
                # if team 1 wins add team2's poke types
                team_nums = team2.team_numbers
                temp_set = BSet()
                for i in range(len(team_nums)):
                    if team_nums[i] > 0:
                        temp_set.add(i+1)  
                team1.types_defeated = team1.types_defeated.union(temp_set) 
            else:
                # if team 2 wins add team1's poke types
                team_nums = team1.team_numbers
                temp_set = BSet()
                for i in range(len(team_nums)):
                    if team_nums[i] > 0:
                        temp_set.add(i+1)  
                team2.types_defeated = team2.types_defeated.union(temp_set) 
        return linked_metas

    def flip_tournament(self, tournament_list: LinkedList[tuple[PokeTeam, PokeTeam]], team1: PokeTeam, team2: PokeTeam) -> None:
        # 1054
        """ swaps the upper and lower brackets that led to the battle between the provided poke teams 
        arg:
            tournament_list - the linked list created during linked_list_of_games
            team1 - the first poke team in the battle
            team2 - the second poke team in the battle
        complexity:
            best/worst case of O(n * comp) where n is the length of the linked list
                                        and comp is the cost of comparison between team names
        """
        
        team1_name = team1.team_name
        team2_name = team2.team_name

        # create an iterator of the tournament list
        tourn_it = iter(tournament_list)
        cur_battle_found = False

        while True: # O(n) n = list size 
            # try to get the next item in the list
            try:
                # each cur_item is an array with two pokeTeams
                cur_item = next(tourn_it)
            except StopIteration:
                team1_first_battle = tourn_it.get_prev_node()
                break
            
            # find the battle between the two teams
            if not cur_battle_found and \
                (cur_item[0].team_name == team1_name and cur_item[1].team_name == team2_name):
                cur_battle = tourn_it.get_current_node()
                cur_battle_found = True
            
            # after the battle is found find the last battle of team 1 (occurs after all of the team 2 battles)
            if cur_battle_found and \
                (cur_item[0].team_name == team1_name or cur_item[1].team_name == team1_name):
                team1_last_battle = tourn_it.get_current_node()
                team2_first_battle = tourn_it.get_prev_node()

        if not cur_battle_found:
            raise ValueError("there was no battle between those teams")
    
        # swap chunks/brackets of battles
        # make cur point to last team1 battle
        team2_last_battle = cur_battle.next # the team 2 battle stream/bracket
        tourn_it.change_next(cur_battle, team1_last_battle)

        # make first team1 point to last team2 battle
        tourn_it.change_next(team1_first_battle, team2_last_battle)

        # first team2 battle points to nothing (at the end)
        tourn_it.change_next(team2_first_battle, None)

        # change the order of the teams in the current battle so that the teams can be flipped again if wanted
        cur_battle.item = (team2, team1)

        return 
    
    