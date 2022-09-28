"""
Implements battle class and its respective method
"""
__author__ = "Scaffold by Jackson Goerner, Code by Felicty, Virani, Dylan, and Edward"

from print_screen import print_game_screen
from random_gen import RandomGen
from poke_team import Action, PokeTeam, Criterion
from print_screen import print_game_screen

class Battle:
    """ a class for battles between two PokeTeams
    Attributes:
        verbosity (int) - indicating how much logging of the battle is wanted
    
    Complexity:
        Unless otherwise stated, the complexity for all methods is O(1)
    """
    def __init__(self, verbosity=0) -> None:
        '''Initialises battle instance
        
        Attributes:
            verbosity - determines extent of game representation when performing battle

        Returns:
            None
        '''
        self.verbosity = verbosity
        # 0 -> no printing
        # 2 -> printing actions and returning/retrieving pokemon
        # 3 -> above and print out the game screen

    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        """Performs the battle between team1 and team2. battle should return 0 1 or 2. 0 representing a
        draw, and 1 or 2 representing player 1 or player 2 winning respectively.

        Complexity:
            Best: O(n) where one team wins in the first attack
            Worst: O(B * n) 
                where n is the size of the poke team, and B is the length of the battle/number of actions
        """

        # regerate teams:
        team1.regenerate_team()                             # O(n) n = poketeam size
        team2.regenerate_team() 

        # battle starts with the first poke
        team1_poke = team1.retrieve_pokemon()               # best O(1) , worst O(n)
        team2_poke = team2.retrieve_pokemon()

        while team1_poke != None or team2_poke != None:     # O(length of battle)
            
            if self.verbosity >= 2:
                print()
                print(str(team1))
                print("in the field:", str(team1_poke))
                print(str(team2))
                print("in the field:", str(team2_poke))
                print()

                if self.verbosity >= 3:
                    # O(n)
                    print_game_screen(team1_poke.get_poke_name(), team2_poke.get_poke_name(), team1_poke.get_hp(), team1_poke.get_max_hp(team1_poke.get_level()), team2_poke.get_hp(), team2_poke.get_max_hp(team2_poke.get_level()), team1_poke.get_level(), team2_poke.get_level(), team1_poke.status_effect, team2_poke.status_effect, len(team1.poke_team) + 1, len((team2.poke_team)) + 1)

            # pick action 
            team1_action = team1.choose_battle_option(team1_poke, team2_poke) # O(1)
            team2_action = team2.choose_battle_option(team2_poke, team1_poke)

            if self.verbosity >= 2:
                print("Team 1 chose to", team1_action.name)
                print("Team 2 chose to", team2_action.name)               

            # team 1 swaps, specials and heals
            if team1_action == Action.SWAP:
                team1.return_pokemon(team1_poke)
                team1_poke = team1.retrieve_pokemon() 
            
            elif team1_action == Action.SPECIAL:
                team1.return_pokemon(team1_poke)
                team1.special()
                team1_poke = team1.retrieve_pokemon()   # best O(1) , worst O(n)
            
            elif team1_action == Action.HEAL:
                if team1.times_healed >= 3:
                    return 2
                else: 
                    team1_poke.heal()
                    team1.times_healed += 1
            
            # team 2 swaps, specials and heals
            if team2_action == Action.SWAP:
                team2.return_pokemon(team2_poke)
                team2_poke = team2.retrieve_pokemon()
            
            elif team2_action == Action.SPECIAL:
                team2.return_pokemon(team2_poke)
                team2.special()
                team2_poke = team2.retrieve_pokemon()
            
            elif team2_action == Action.HEAL:
                if team2.times_healed >= 3:
                    return 1
                else: 
                    team2_poke.heal()
                    team2.times_healed += 1

            # handle attacks 
            if team1_action == Action.ATTACK and team2_action == Action.ATTACK:
                # Simultaneous attack
                team1_speed = team1_poke.get_speed()
                team2_speed = team2_poke.get_speed()
                
                # if poke has paralysis speed is halved
                if team1_poke.status_effect == "paralysis":
                    team1_speed = team1_speed // 2
                if team2_poke.status_effect == "paralysis":
                    team2_speed = team2_speed // 2
                
                # determines which poke attacks first
                if team1_speed >= team2_speed:
                    team1_attacks_first = True
                elif team1_speed < team2_speed:
                    team1_attacks_first = False
                
                # if team 1 attacks first
                if team1_attacks_first:
                    team1_poke.attack(team2_poke)           # O(comp) where comp is cost of comparison between status effects
                    
                    if self.verbosity >= 2:
                        print("Team 1's", team1_poke.get_poke_name(), "attacked")
                    
                    if not team2_poke.is_fainted() or team1_speed == team2_speed:
                        team2_poke.attack(team1_poke) # O(1)
                        if self.verbosity >= 2:
                            print("Team 2's", team2_poke.get_poke_name(), "attacked")

                
                # Otherwise team 2 attacks first 
                elif not team1_attacks_first:
                    team2_poke.attack(team1_poke)
                    
                    if self.verbosity >= 2:
                        print("Team 2's", team2_poke.get_poke_name(), "attacked")
                    
                    if not team1_poke.is_fainted():
                        team1_poke.attack(team2_poke)
                        
                        if self.verbosity >= 2:
                            print("Team 1's", team1_poke.get_poke_name(), "attacked")

            # team 1 attacks only
            elif team1_action == Action.ATTACK:
                team1_poke.attack(team2_poke)
            
                if self.verbosity >= 2:
                    print("Team 1's", team1_poke.get_poke_name(), "attacked")

            # team 2 attacks only
            elif team2_action == Action.ATTACK:
                team2_poke.attack(team1_poke)

                if self.verbosity >= 2:
                    print("Team 2's", team2_poke.get_poke_name(), "attacked")

            # if both still alive lose 1 HP 
            if not team1_poke.is_fainted() and not team2_poke.is_fainted():
                team1_poke.lose_hp(1)
                team2_poke.lose_hp(1)
                
                # if pokemon has not fainted and can evolve, they evolve
                if not team1_poke.is_fainted() and team1_poke.should_evolve():
                    team1_poke = team1_poke.get_evolved_version()
                if not team2_poke.is_fainted() and team2_poke.should_evolve():
                    team2_poke = team2_poke.get_evolved_version()
                
            # if one has fainted and the other is alive, alive pokemon levels up
            # team1 alive, team 2 dead
            if not team1_poke.is_fainted() and team2_poke.is_fainted():
                team1_poke.level_up()
                if team1_poke.should_evolve():
                    team1_poke = team1_poke.get_evolved_version()
                    if self.verbosity >= 2:
                        print("Team 1's poke evolved into a", team1_poke.get_poke_name())
            
            # team2 alive, team1 dead
            elif not team2_poke.is_fainted() and team1_poke.is_fainted():
                team2_poke.level_up()
                if team2_poke.should_evolve():
                    team2_poke = team2_poke.get_evolved_version()
                    if self.verbosity >= 2:
                        print("Team 2's poke evolved into a", team2_poke.get_poke_name())
            
            # Return pokemon if fainted, then retrieve from team
            if team1_poke.is_fainted():
                team1.return_pokemon(team1_poke)
                if self.verbosity >= 2:
                    print(f"Team 1 Pokemon: {team1_poke} just fainted")
                team1_poke = team1.retrieve_pokemon()
                if self.verbosity >= 2:
                    print(f"Team 1 Pokemon: {team1_poke} was retrieved")

            if team2_poke.is_fainted():
                team2.return_pokemon(team2_poke)
                if self.verbosity >= 2:
                    print(f"Team 2 Pokemon: {team2_poke} just fainted")
                team2_poke = team2.retrieve_pokemon()
                if self.verbosity >= 2:
                    print(f"Team 2 Pokemon: {team2_poke} was retrieved")

            # draw
            if team1_poke == None and team2_poke == None:
                return 0
            # team 2 wins when team 1 has no poke left
            elif team1_poke == None:
                team2.return_pokemon(team2_poke)            # best O(1), worst O(logn)
                return 2
            # team 1 wins when team 2 has no poke left
            elif team2_poke == None:
                team1.return_pokemon(team1_poke)
                return 1


