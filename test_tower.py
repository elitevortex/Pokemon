__author__ = "Maria Garcia de la Banda for the base"+"XXXXX student for"

import unittest
from pokemon import Gastly, Haunter, Gengar, Eevee, Bulbasaur, Venusaur, Squirtle, Charmander, Charizard, Blastoise
from poke_team import PokeTeam, Criterion, Action
from random_gen import RandomGen
from battle import Battle
from tower import BattleTower

class TestTower(unittest.TestCase):
    """ test class for testing BattleTower in tower.py """

    def test_init(self):
        '''tests the intialisiation of a battle tower'''
        b = BattleTower("h")
        
        self.assertEqual(type(b.battle), Battle)
        self.assertEqual(b.my_team, None)
        self.assertEqual(b.tower_teams, None)


    def test_set_my_team(self):
        '''tests ability to set tower fighting team'''
        b = BattleTower()
        self.assertRaises(AssertionError, lambda: b.set_my_team(10))

        pt = PokeTeam("lamp", [1,2,1,0,1], 0, PokeTeam.AI.USER_INPUT)
        b.set_my_team(pt)

        self.assertEqual(b.my_team.team_name, "lamp")
        self.assertEqual(b.my_team.team_numbers, [1,2,1,0,1])
        self.assertEqual(b.my_team.battle_mode, 0)
        self.assertEqual(b.my_team.ai_type, PokeTeam.AI.USER_INPUT)

        
    def test_generate_teams(self):
        ''' tests random generation of tower teams '''
        b = BattleTower()
        b.generate_teams(3)
        # Check length
        self.assertTrue(len(b.tower_teams) == 3)
        for team in b.tower_teams:      
            # Check battle_mode
            self.assertTrue(team[0].battle_mode == 1 or team[0].battle_mode == 0)    
            # Check lives
            self.assertTrue(team[1] >= 2 and team[1] <= 10) 

        b1 = BattleTower()
        b1.generate_teams(10)
        # Check length
        self.assertTrue(len(b1.tower_teams) == 10)
        # for all teams
            # Check battle mode is 0 or 1
        for team in b1.tower_teams:      
            self.assertTrue(team[0].battle_mode == 1 or team[0].battle_mode == 0)    # Checks battle mode
            self.assertTrue(team[1] >= 2 and team[1] <= 10) # Checks lives

        b2 = BattleTower()
        # Check negative number of teams
        self.assertRaises(AssertionError, lambda: b2.generate_teams(-1))
        # Check incorrect input type
        self.assertRaises(AssertionError, lambda: b2.generate_teams("Hello"))
        

    def test_next(self):
        """ testing the battle tower iterator """
        RandomGen.set_seed(6457)

        bt = BattleTower()
        # subtest 1
        bt.set_my_team(PokeTeam.random_team("Sagitarius", 0, team_size=5))
        bt.generate_teams(5)

        it = iter(bt)
        expected = [(1, 3), (1, 5), (2, 2)]

        for i in range(3):
            res, my, tower, lives = next(it)
            self.assertEqual((res, lives), expected[i])

        # subtest 2
        bt.set_my_team(PokeTeam.random_team("Gemini", 1, team_size=5))
        bt.generate_teams(5)

        it = iter(bt)
        expected = [(1, 1), (2, 6)]

        for i in range(2):
            res, my, tower, lives = next(it)
            self.assertEqual((res, lives), expected[i])
            self.assertEqual(my.team_name, "Gemini")

        # subtest 3
        bt.set_my_team(PokeTeam.random_team("Leo", 2, team_size=5))
        bt.generate_teams(5)
        
        it = iter(bt)
        expected = [(2, 10)]

        for i in range(1):
            res, my, tower, lives = next(it)
            self.assertEqual((res, lives), expected[i])
        

    def test_dupes_given(self):
        """ testing whether the dupes were removed with the provided data """
        RandomGen.set_seed(29183712400123)

        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jackson", 0, team_size=6))
        bt.generate_teams(10)
        # Team numbers before:
        # [0, 4, 1, 0, 0], 6
        # [1, 0, 2, 0, 0], 5
        # [1, 1, 0, 1, 0], 8
        # [1, 2, 1, 1, 0], 10
        # [0, 0, 2, 1, 1], 8
        # [1, 1, 3, 0, 0], 4
        # [0, 2, 0, 1, 0], 5
        # [1, 0, 0, 4, 0], 3
        # [1, 1, 1, 0, 2], 7
        # [0, 1, 1, 1, 0], 9
        it = iter(bt)
        it.avoid_duplicates()
        # Team numbers after:
        # [1, 1, 0, 1, 0], 8
        # [0, 1, 1, 1, 0], 9
        self.assertEqual(len(it.tower_teams), 2)
        self.assertEqual(it.tower_teams[0][0].team_numbers, [1, 1, 0, 1, 0])
        self.assertEqual(it.tower_teams[1][0].team_numbers, [0, 1, 1, 1, 0])
        self.assertEqual(it.tower_teams[0][1], 8)
        self.assertEqual(it.tower_teams[1][1], 9)

    def test_dupes_again(self):
        """ another test for avoid duplicates method """
        RandomGen.set_seed(541)
        tm = PokeTeam.random_team("hello",1,5)
        tower = BattleTower()
        tower.set_my_team(tm)
        tower.generate_teams(6)

        it = iter(tower)
        it.avoid_duplicates()
       
        # before 
        # [0, 1, 1, 1, 0], 5
        # [2, 0, 1, 0, 0], 4
        # [0, 4, 1, 0, 1], 7
        # [0, 0, 2, 1, 1], 9
        # [1, 1, 0, 2, 2], 10
        # [0, 1, 2, 0, 0], 5
        # after
        # [0, 1, 1, 1, 0], 5
        self.assertEqual(len(it.tower_teams), 1)
        self.assertEqual(it.tower_teams[0][0].team_numbers, [0, 1, 1, 1, 0])
        self.assertEqual(it.tower_teams[0][1], 5)

    def test_all_dupes(self):
        """ test for when all teams are duplicates """
        RandomGen.set_seed(5476)
        tm = PokeTeam.random_team("hello",1,5)
        tower = BattleTower()
        tower.set_my_team(tm)
        tower.generate_teams(6)

        it = iter(tower)
        it.avoid_duplicates()

        # before:
        # [1, 1, 0, 0, 2], 6
        # [1, 1, 0, 3, 0], 9
        # [0, 1, 2, 2, 0], 6
        # [0, 2, 0, 0, 2], 10
        # [0, 2, 0, 1, 0], 2
        # [3, 0, 0, 0, 0], 4
        # all are dupes so all must be removed

        self.assertEqual(len(it.tower_teams), 0)

    def test_sort_by_lives(self):
        """ testing sort by lives method """
        # 1054 only
        RandomGen.set_seed(1234)
    
        bt = BattleTower(Battle(verbosity=0))
        # first subtest
        bt.set_my_team(PokeTeam.random_team("Sagitarius", 0, team_size=5))
        bt.generate_teams(5)

        it = iter(bt)
        # lives generated: 7, 4, 10, 7, 10
        it.sort_by_lives()

        expected_lives = [4,7,7,10,10]
        for i in range(5):
            self.assertEqual(it.tower_teams[i][1], expected_lives[i])

        # second subtest
        bt.generate_teams(7)
        it = iter(bt)
        # lives generated: 6, 7, 9, 10, 2, 10, 6

        it.sort_by_lives()

        expected_lives = [2,6,6,7,9,10,10]
        for i in range(5):
            self.assertEqual(it.tower_teams[i][1], expected_lives[i])

        # third subtest
        bt.generate_teams(11)
        it = iter(bt)
        # lives generated: 8, 9, 3, 10, 10, 2, 7, 8, 6, 5, 6

        it.sort_by_lives()

        expected_lives = [2,3,5,6,6,7,8,8,9,10,10]
        for i in range(11):
            self.assertEqual(it.tower_teams[i][1], expected_lives[i])



if __name__=="__main__":
    unittest.main()