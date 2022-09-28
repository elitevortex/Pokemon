__author__ = "Scaffold by Jackson Goerner, Code by Felicty, Virani, Dylan, and Edward"

import unittest
from pokemon import Gastly, Haunter, Gengar, Eevee, Bulbasaur, Venusaur, Squirtle, Charmander, Charizard, Blastoise
from poke_team import PokeTeam, Criterion, Action
from battle import Battle
from random_gen import RandomGen

class TestBattle(unittest.TestCase):
    """ test class for testing PokeTeam in battle.py """

    def test_always_attack(self):
        """ testing a basic battle """
        RandomGen.set_seed(3332)
        team1 = PokeTeam("gold", [1,0,0,0,0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("silver", [1,0,0,0,0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        
        # draw - same starting teams
        bat = Battle()
        self.assertEqual(bat.battle(team1, team2), 0)
        self.assertTrue(team1.is_empty())
        self.assertTrue(team2.is_empty())

    def test_battle(self):
        '''SWAP_ON_SUPER_EFFECTIVE battle test'''
        RandomGen.set_seed(67)
        team1 = PokeTeam("wowow", [1,1,0,1,2], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        team2 = PokeTeam("bruhh", [1,0,1,2,1], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)

        # team 1 win
        bat = Battle()
        self.assertEqual(bat.battle(team1, team2), 1)
        self.assertTrue(team2.is_empty())
        
    def test_another_battle(self):
        """ testing another battle """
        RandomGen.set_seed(2780)
        team1 = PokeTeam("yay", [1,0,2,0,1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("eww", [1,1,1,1,1], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        
        # team 2 wins
        bat = Battle()
        self.assertEqual(bat.battle(team1, team2), 2)
        self.assertTrue(team1.is_empty())
    
    def test_random(self):
        """ testing a battle with random actions chosen """

        RandomGen.set_seed(8978)
        team1 = PokeTeam("milktea", [1,0,0,0,0], 0, PokeTeam.AI.RANDOM)
        team2 = PokeTeam("cailaatay", [1,0,2,0,0], 0, PokeTeam.AI.RANDOM)
        
        # team 2 wins
        bat = Battle()
        self.assertEqual(bat.battle(team1, team2), 2)
        self.assertTrue(team1.is_empty())


if __name__=="__main__":
    unittest.main()