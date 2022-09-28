__author__ = "Scaffold by Jackson Goerner, Code by Felicty, Virani, Dylan, and Edward"

import unittest
from pokemon import Gastly, Haunter, Gengar, Eevee, Bulbasaur, Venusaur, Squirtle, Charmander, Charizard, Blastoise
from poke_team import PokeTeam, Criterion, Action
from random_gen import RandomGen
from stack_adt import ArrayStack

class TestPokeTeam(unittest.TestCase):
    """ test class for testing PokeTeam in poke_team.py """
    
    def test_choose_battle_option(self):
        """ test for choose_battle_option method """
        pt1 = PokeTeam("violet", [1,1,1,2,0], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.HP)
        pt2 = PokeTeam("lilac", [0,2,2,0,1], 3, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, Criterion.DEF, 10)
        pt3 = PokeTeam("eddie", [1,0,2,1,2], 2, PokeTeam.AI.RANDOM, Criterion.LV)
        
        self.assertEqual(str(pt1), "violet (2): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Charmander: 9 HP, LV. 1 Gastly: 6 HP, LV. 1 Gastly: 6 HP]")
        self.assertEqual(str(pt2), "lilac (3): [LV. 1 Squirtle: 11 HP, LV. 1 Squirtle: 11 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP]")
        self.assertEqual(str(pt3), "eddie (2): [LV. 1 Charmander: 9 HP, LV. 1 Squirtle: 11 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP]")

        poke1 = pt1.retrieve_pokemon()
        self.assertIsInstance(poke1, Bulbasaur)

        poke2 = pt2.retrieve_pokemon()
        self.assertIsInstance(poke2, Squirtle)

        poke3 = pt3.retrieve_pokemon()
        self.assertIsInstance(poke3, Charmander)

        RandomGen.set_seed(123)
        self.assertEqual(pt1.choose_battle_option(poke1, poke2), Action.ATTACK)
        self.assertEqual(pt2.choose_battle_option(poke2, poke1), Action.SWAP)
        self.assertEqual(pt3.choose_battle_option(poke3, poke1), Action.HEAL)

    def test_retrieve_return_poke(self):
        """ test returning and retrieving poke from a team """
        pt0 = PokeTeam("Fiesta", [1,2,0,2,1], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        pt1 = PokeTeam("WekiMeki", [1,1,1,1,1], 1, PokeTeam.AI.ALWAYS_ATTACK)
        pt2 = PokeTeam("Samsung", [1,1,2,0,2], 2, PokeTeam.AI.USER_INPUT, Criterion.SPD)
        pt3 = PokeTeam("Slay", [1,1,2,0,1], 3, PokeTeam.AI.RANDOM, Criterion.HP, 15)
        
        self.assertEqual(str(pt0), "Fiesta (0): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Gastly: 6 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")
        self.assertEqual(str(pt1), "WekiMeki (1): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")
        self.assertEqual(str(pt2), "Samsung (2): [LV. 1 Charmander: 9 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Squirtle: 11 HP]")
        self.assertEqual(str(pt3), "Slay (3): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Squirtle: 11 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]")
        
        poke0 = pt0.retrieve_pokemon()
        poke1 = pt1.retrieve_pokemon()
        poke2 = pt2.retrieve_pokemon()
        poke3 = pt3.retrieve_pokemon()

        self.assertIsInstance(poke0, Charmander)
        self.assertIsInstance(poke1, Charmander)
        self.assertIsInstance(poke2, Charmander)
        self.assertIsInstance(poke3, Bulbasaur)

        pt0.return_pokemon(poke0)
        pt1.return_pokemon(poke1)
        pt2.return_pokemon(poke2)
        pt3.return_pokemon(poke3)

        self.assertEqual(str(pt0), "Fiesta (0): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Gastly: 6 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")
        self.assertEqual(str(pt1), "WekiMeki (1): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]")
        self.assertEqual(str(pt2), "Samsung (2): [LV. 1 Charmander: 9 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Squirtle: 11 HP]")
        self.assertEqual(str(pt3), "Slay (3): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Squirtle: 11 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]")

    # Test battle mode 0
    def test_battle_mode_0(self):
        """ test for battle mode 0 """
        # Create team for testing
        test_team = PokeTeam("viranieats!!!!!", [1,2,0,2,1], 0, PokeTeam.AI.RANDOM)
        pt_string = str(test_team)
        expected_types = [Charmander, Bulbasaur, Bulbasaur, Gastly, Gastly, Eevee]

        # testing that the same poke is retrieved when returned (if not fainted)
        p = test_team.retrieve_pokemon()
        test_team.return_pokemon(p)
        self.assertEqual(type(p), type(test_team.retrieve_pokemon()))
        test_team.return_pokemon(p)

        # testing retrieval
        temp_stack = ArrayStack(6)
        for i in range(len(test_team.poke_team)):
            poke = test_team.retrieve_pokemon()
            self.assertIsInstance(poke, expected_types[i])
            temp_stack.push(poke)
        
        for _ in range(len(temp_stack)):
            test_team.return_pokemon(temp_stack.pop())

        # testing that the team is the same order once all have be retrieved and returned
        self.assertEqual(str(test_team), pt_string)

        # testing special
        test_team.special()
        expected_types = [Eevee, Bulbasaur, Bulbasaur, Gastly, Gastly, Charmander]
        for i in range(len(test_team.poke_team)):
            self.assertIsInstance(test_team.retrieve_pokemon(), expected_types[i])

    # Test battle_mode 1
    def test_battle_mode_1(self):
        """ test for battle mode 1 """
        test_team = PokeTeam("iris", [1,2,0,2,1], 1, PokeTeam.AI.RANDOM)
        
        pt_string = str(test_team)

        expected_types = [Charmander, Bulbasaur, Bulbasaur, Gastly, Gastly, Eevee]

        # testing retrieval
        for i in range(len(test_team.poke_team)):
            poke = test_team.retrieve_pokemon()
            self.assertIsInstance(poke, expected_types[i])
            test_team.return_pokemon(poke)
        
        # testing that the team is the same order once all have be retrieved and returned
        self.assertEqual(str(test_team), pt_string)

        # testing special
        test_team.special()
        expected_types = [Gastly, Gastly, Eevee, Bulbasaur, Bulbasaur, Charmander]
        for i in range(len(test_team.poke_team)):
            self.assertIsInstance(test_team.retrieve_pokemon(), expected_types[i])
    
    def test_battle_mode_2_ordering(self):
        """ test for ordering of battle mode 2 (a sorted list) """
        # testing sorting by hp
        pt1 = PokeTeam("Salmon", [2,0,1,1,1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.HP)
        self.assertEqual(str(pt1), "Salmon (2): [LV. 1 Squirtle: 11 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP, LV. 1 Charmander: 9 HP, LV. 1 Gastly: 6 HP]")
        
        # testing sorting by level
        pt2 = PokeTeam("Eel", [2,0,1,1,1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.LV)
        self.assertEqual(str(pt2), "Eel (2): [LV. 1 Charmander: 9 HP, LV. 1 Charmander: 9 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")

        # testing sorting by defence
        pt3 = PokeTeam("Dori", [2,0,1,1,1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.DEF)
        self.assertEqual(str(pt3), "Dori (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP, LV. 1 Charmander: 9 HP]")

        # testing sorting by speed
        pt4 = PokeTeam("Nemo", [2,0,1,1,1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.SPD)
        self.assertEqual(str(pt4), "Nemo (2): [LV. 1 Charmander: 9 HP, LV. 1 Charmander: 9 HP, LV. 1 Eevee: 10 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP]")
        

    # Test battle mode 2:
    def test_battle_mode_2(self):
        """ test for battle mode 2 """
        test_team = PokeTeam("not iris", [1,2,0,2,1], 2, PokeTeam.AI.RANDOM, Criterion.HP)
        
        pt_string = str(test_team)

        expected_types = [Bulbasaur, Bulbasaur, Eevee, Charmander, Gastly, Gastly]

        # testing that the same poke is retrieved when returned (if not fainted)
        p = test_team.retrieve_pokemon()
        test_team.return_pokemon(p)
        self.assertEqual(type(p), type(test_team.retrieve_pokemon()))
        test_team.return_pokemon(p)

        # testing retrieval
        temp_stack = ArrayStack(6)
        for i in range(len(test_team.poke_team)):
            poke = test_team.retrieve_pokemon()
            self.assertIsInstance(poke, expected_types[i])
            temp_stack.push(poke)
        
        for _ in range(len(temp_stack)):
            test_team.return_pokemon(temp_stack.pop())
        
        # testing that the team is the same order once all have be retrieved and returned
        self.assertEqual(str(test_team), pt_string)

        # testing special
        test_team.special()
        expected_types = [Gastly, Gastly, Charmander, Eevee, Bulbasaur, Bulbasaur]
        for i in range(len(test_team.poke_team)):
            self.assertIsInstance(test_team.retrieve_pokemon(), expected_types[i])

    # Test battle_mode 3
    def test_battle_mode_3(self):
        """ test for battle mode 3 """
        test_team = PokeTeam("faze clan", [1,2,0,2,1], 3, PokeTeam.AI.RANDOM, Criterion.HP, 10)
        
        pt_string = str(test_team)

        expected_types = [Eevee, Charmander, Bulbasaur, Bulbasaur, Gastly, Gastly]

        # testing that the same poke is retrieved when returned (if not fainted)
        p = test_team.retrieve_pokemon()
        test_team.return_pokemon(p)
        self.assertEqual(type(p), type(test_team.retrieve_pokemon()))
        test_team.return_pokemon(p)

        # testing retrieval
        temp_stack = ArrayStack(6)
        for i in range(len(test_team.poke_team)):
            poke = test_team.retrieve_pokemon()
            self.assertIsInstance(poke, expected_types[i])
            temp_stack.push(poke)
        
        for _ in range(len(temp_stack)):
            test_team.return_pokemon(temp_stack.pop())
    
        # testing that the team is the same order once all have be retrieved and returned
        self.assertEqual(str(test_team), pt_string)

        # testing special
        test_team.special() # should do nothing
        for i in range(len(test_team.poke_team)):
            self.assertIsInstance(test_team.retrieve_pokemon(), expected_types[i])


    def test_regenerate(self):
        """ testing regenerate_team """
        p_1 = PokeTeam("seaside", [0,2,1,1,1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        p_2 = PokeTeam("fish", [1,0,1,1,1], 1, PokeTeam.AI.RANDOM)
        p_3= PokeTeam("chips", [3,0,2,1,0], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, Criterion.DEF)
        p_1_string = str(p_1)
        p_2_string = str(p_2)
        p_3_string = str(p_3)

        self.assertEqual(len(p_1.poke_team), 5)
        self.assertEqual(len(p_2.poke_team), 4)
        self.assertEqual(len(p_3.poke_team), 6)

        for _ in range(5):
            p_1.retrieve_pokemon()

        for _ in range(4):
            p_2.retrieve_pokemon()
        
        for _ in range(3):
            p_3.retrieve_pokemon()
        
        self.assertTrue(p_1.is_empty())
        self.assertTrue(p_2.is_empty())
        self.assertTrue(len(p_3.poke_team), 3)

        p_1.regenerate_team()
        p_2.regenerate_team()
        p_3.regenerate_team()

        self.assertEqual(p_1_string, str(p_1))
        self.assertEqual(p_2_string, str(p_2))
        self.assertEqual(p_3_string, str(p_3))

    
    def test_random_gen(self):
        RandomGen.set_seed(369)
        pt1 = PokeTeam.random_team("lamp", 0, 3)
        pt2 = PokeTeam.random_team("chair", 1, 5, PokeTeam.AI.ALWAYS_ATTACK)
        pt3 = PokeTeam.random_team("table", 2, 4, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        
        # testing team 1 attributes
        self.assertEqual(len(pt1.poke_team), 3)
        self.assertEqual(pt1.battle_mode, 0)
        self.assertEqual(pt1.team_name, "lamp")
        self.assertEqual(pt1.ai_type, PokeTeam.AI.RANDOM)

        # testing team 2 attributes
        self.assertEqual(len(pt2.poke_team), 5)
        self.assertEqual(pt2.battle_mode, 1)
        self.assertEqual(pt2.team_name, "chair")
        self.assertEqual(pt2.ai_type, PokeTeam.AI.ALWAYS_ATTACK)

        # testing team 3 attributes
        self.assertEqual(len(pt3.poke_team), 4)
        self.assertEqual(pt3.battle_mode, 2)
        self.assertEqual(pt3.team_name, "table")
        self.assertEqual(pt3.ai_type, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)

        
    def test_return_fainted_poke(self):
        # Battle mode 0 - stack
        pt1 = PokeTeam("gongcha",[1,2,0,2,1], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        pt2 = PokeTeam("sharetea",[1,2,0,2,1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.SPD)

        # test if length of PokeTeam is equal to 6
        self.assertEqual(len(pt1.poke_team), 6)
        self.assertEqual(len(pt2.poke_team), 6)
        
        # Pop another pokemon off stack
        alive_poke = pt1.poke_team.pop()
        pt1.return_pokemon(alive_poke)
        self.assertEqual(len(pt1.poke_team), 6)
        
        # Pop pokemon off stack
        fainted_poke = pt1.poke_team.pop()
        fainted_poke.lose_hp(fainted_poke.get_max_hp(fainted_poke.get_level()))
        self.assertIsNone(pt1.return_pokemon(fainted_poke))
        self.assertEqual(len(pt1.poke_team), 5)

        # add fainted poke to sorted list
        self.assertTrue(len(pt2.poke_team), 6)
        fainted_poke = pt2.retrieve_pokemon()
        fainted_poke.lose_hp(fainted_poke.get_max_hp(fainted_poke.get_level()))
        pt2.return_pokemon(fainted_poke)
        self.assertTrue(len(pt2.poke_team), 5)
        

if __name__=="__main__":
    unittest.main()