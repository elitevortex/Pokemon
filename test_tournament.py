__author__ = "Scaffold by Jackson Goerner, Code by Felicty, Virani, Dylan, and Edward"

import unittest
from pokemon import Gastly, Haunter, Gengar, Eevee, Bulbasaur, Venusaur, Squirtle, Charmander, Charizard, Blastoise
from poke_team import PokeTeam, Criterion, Action
from random_gen import RandomGen
from tournament import Tournament
from battle import Battle


class TestTournament(unittest.TestCase):
    """ test class for testing Tournament in tournament.py """

    def test_is_valid(self):
        """ testing the is_valid_tournament function """
        t = Tournament()
        # testing valid strings
        self.assertTrue(t.is_valid_tournament("a b +"))
        self.assertTrue(t.is_valid_tournament("a b + c +"))
        self.assertTrue(t.is_valid_tournament("a b + c d e + + +"))
        self.assertTrue(t.is_valid_tournament("Monfils Berrettini + Shapovalov Nadal + + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +"))
        
        # testing invalid strings
        self.assertFalse(t.is_valid_tournament("a b + +"))
        self.assertFalse(t.is_valid_tournament("a b"))
        self.assertFalse(t.is_valid_tournament("+"))
        self.assertFalse(t.is_valid_tournament(""))
        self.assertFalse(t.is_valid_tournament("a b + c d e + +"))
        self.assertFalse(t.is_valid_tournament("+ a b + c d e + +"))
        self.assertFalse(t.is_valid_tournament("a b - c d - -"))

    def test_is_balanced(self):
        """ testing the is_balanced_tournament method"""
        t = Tournament()
        # testing valid strings
        self.assertTrue(t.is_balanced_tournament("a b +"))
        self.assertTrue(t.is_balanced_tournament("a b + c d + +"))
        self.assertTrue(t.is_balanced_tournament("a b + c d + + e f + g h + + +"))

        # testing invalid strings
        self.assertFalse(t.is_balanced_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"))
        self.assertFalse(t.is_balanced_tournament("a b + c +"))
        self.assertFalse(t.is_balanced_tournament("+"))
        self.assertFalse(t.is_balanced_tournament("a b + c + + + +"))
        
    def test_set_battle_mode(self):
        """ tests the set_battle_mode method """
        t = Tournament()
        # Check battle mode 0
        t.set_battle_mode(0)
        t.start_tournament("Monfils Berrettini + Shapovalov Nadal + + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +") 

        # Serve and check battle mode across all teams in the tournament
        for _ in range(len(t.tourn_queue)):
            current_item = t.tourn_queue.serve()
            if current_item  != "+":
                self.assertTrue(current_item.battle_mode == 0)
        
        # Check battle mode 1
        t.set_battle_mode(1)
        t.start_tournament("Monfils Berrettini + Shapovalov Nadal + + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +")
        for _ in range(len(t.tourn_queue)):
            current_item = t.tourn_queue.serve()
            if current_item != "+":
                self.assertTrue(current_item.battle_mode == 1)
        
        # Check invalid battlemode (negative and above 3)
        self.assertRaises(AssertionError, lambda: t.set_battle_mode(-1))
        self.assertRaises(AssertionError, lambda: t.set_battle_mode(4))
        
    
    def test_start_tournament_basic(self):
        """ testing basic tournament setup """
        t = Tournament()
        t.set_battle_mode(0)

        self.assertRaises(ValueError, lambda: t.start_tournament("a b"))
        t.start_tournament("a b +")

        expected_types = [PokeTeam, PokeTeam, str]
        expected_names = ["a", "b"]

        for i in range(len(t.tourn_queue)):
            item = t.tourn_queue.serve()
            self.assertEqual(type(item), expected_types[i])
            if type(item) == PokeTeam:
                self.assertEqual(item.team_name, expected_names[i])
                self.assertEqual(item.battle_mode, 0)
            else:
                self.assertEqual(item, "+")

    def test_start_tourn_complex(self):
        """ tests a more complex tournament string """
        t = Tournament()
        t.set_battle_mode(1) 
        t.start_tournament("a b + c d e + + +")

        expected_types = [PokeTeam, PokeTeam, str, PokeTeam, PokeTeam, PokeTeam, str, str, str]
        expected_names = ["a", "b", "", "c", "d", "e"]

        for i in range(len(t.tourn_queue)):
            item = t.tourn_queue.serve()
            self.assertEqual(type(item), expected_types[i])
            if type(item) == PokeTeam:
                self.assertEqual(item.team_name, expected_names[i])
                self.assertEqual(item.battle_mode, 1)
            else:
                self.assertEqual(item, "+")
                
    
    def test_advance_tournament(self):
        """ tests the advance_tournament method """
        RandomGen.set_seed(123)
        t = Tournament()
        t.set_battle_mode(1)

        self.assertTrue(t.is_valid_tournament("Money Health + Protein Weather + + Pork Sashimi + Apple Samsung + + +"))
        t.start_tournament("Money Health + Protein Weather + + Pork Sashimi + +")
        
        expected_names = ['Money', 'Health', '+', 'Protein', 'Weather', '+', '+', 'Pork', 'Sashimi', '+', '+']
        
        for i in range(len(t.tourn_queue)):
            item = t.tourn_queue.serve()
            if type(item) == PokeTeam:
                self.assertEqual(item.team_name, expected_names[i])
            else:
                self.assertEqual(item, expected_names[i])

        t.start_tournament("Money Health + Protein Weather + + Pork Sashimi + +")

        team1, team2, res = t.advance_tournament()  # Money vs Health
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith('Money'))
        self.assertTrue(str(team2).startswith('Health'))

        team1, team2, res = t.advance_tournament()  # Protein vs Weather
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith('Protein'))
        self.assertTrue(str(team2).startswith('Weather'))

        team1, team2, res = t.advance_tournament()  # Money vs Weather
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith('Money'))
        self.assertTrue(str(team2).startswith('Weather'))
        

        team1, team2, res = t.advance_tournament()  # Pork vs Sashimi
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith('Pork'))
        self.assertTrue(str(team2).startswith('Sashimi'))

        team1, team2, res = t.advance_tournament()  # Weather vs Pork
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith('Weather'))
        self.assertTrue(str(team2).startswith('Pork'))

        # Checking None is returned when no games remaining
        res = t.advance_tournament()
        self.assertTrue(res == None)
    
    def test_linked_list_with_metas(self):
        RandomGen.set_seed(999)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        t.start_tournament("Dayum Okay + Chill Bruh + Queen Purr + + + Sammy Chau + +")

        # Dayum [1, 0, 2, 3, 0]
        # Okay [0, 2, 0, 0, 3]
        # Chill [0, 2, 0, 1, 0]
        # Bruh [0, 3, 1, 0, 1]
        # Queen [1, 0, 1, 2, 0]
        # Purr [1, 1, 0, 1, 0]
        # Sammy [0, 0, 1, 2, 0]
        # Chau  [1, 0, 3, 2, 0]
        
        l = t.linked_list_with_metas()

        expected = [['GRASS', 'NORMAL'], [], ['NORMAL'], [], [], [], []]
        for i in range(len(l)):
            self.assertEqual(l[i][2], expected[i])

    def test_another_meta(self):
        """ another test for linked_list_with_metas """
        # subtest 1
        RandomGen.set_seed(999)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("a b + c d + +")
        l = t.linked_list_with_metas()

        expected = [['NORMAL'], [], []]
        for i in range(len(l)):
            self.assertEqual(l[i][2], expected[i])
    
    def test_another_meta_2(self):
        """ yet another test for linked_list_with_metas """
        RandomGen.set_seed(93)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("a b + c d + + e f + +")
        l = t.linked_list_with_metas()

        expected = [[], [], ['FIRE'], [], []]
        for i in range(len(l)):
            self.assertEqual(l[i][2], expected[i])

    def test_flip_tournament(self):
        """ testing the flip_tournament method """
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")
        l = t.linked_list_of_games()
        
        expected = [("Roark", "Candice"), ("Candice", "Volkner"), ("Roark", "Fantina"), ("Maylene", "Fantina"), ("Fantina", "Byron"), ("Maylene", "Crasher_Wake"), ("Roark", "Gardenia")]

        # check that the linked list of games gives the expected output
        for i in range(len(l)):
            self.assertEqual(l[i][0].team_name, expected[i][0])
            self.assertEqual(l[i][1].team_name, expected[i][1])

        t.flip_tournament(l, l[2][0], l[2][1]) # flip at ("Roark", "Fantina")

        expected = [("Roark", "Candice"), ("Candice", "Volkner"), ("Fantina", "Roark"), ("Roark", "Gardenia"), ("Maylene", "Fantina"), ("Fantina", "Byron"), ("Maylene", "Crasher_Wake")]

        # check that the list flipped itself as expected
        for i in range(len(l)):
            self.assertEqual(l[i][0].team_name, expected[i][0])
            self.assertEqual(l[i][1].team_name, expected[i][1])

    def test_another_flip_tourn(self):
        RandomGen.set_seed(246)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("a b + c d + +")
        l = t.linked_list_of_games()
        
        # check that the list is as expected
        before = [("b", "d"), ("c", "d"), ("a", "b")]
        for i in range(len(l)):
            self.assertEqual(l[i][0].team_name, before[i][0])
            self.assertEqual(l[i][1].team_name, before[i][1])

        t.flip_tournament(l, l[0][0], l[0][1]) # flip at ("b", "d")

        after = [("d", "b"), ("a", "b"), ("c", "d")]
        # check that the list flipped itself as expected
        for i in range(len(l)):
            self.assertEqual(l[i][0].team_name, after[i][0])
            self.assertEqual(l[i][1].team_name, after[i][1])
        
        # check flipping it back
        t.flip_tournament(l, l[0][0], l[0][1])
        for i in range(len(l)):
            self.assertEqual(l[i][0].team_name, before[i][0])
            self.assertEqual(l[i][1].team_name, before[i][1])


if __name__=="__main__":
    unittest.main()