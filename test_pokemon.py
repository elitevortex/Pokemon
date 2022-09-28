__author__ = "Scaffold by Jackson Goerner, Code by Felicty, Virani, Dylan, and Edward"

import unittest
from pokemon import Gastly, Haunter, Gengar, Eevee, Bulbasaur, Venusaur, Squirtle, Charmander, Charizard, Blastoise
from random_gen import RandomGen

class TestPokemon(unittest.TestCase):
    """ test class for testing the pokemon in pokemon.py and the pokemon base in pokemon_base """

    def test_gastly_stats(self):
        """ test for the Gastly's stats and leveling up """
        g = Gastly()
        self.assertEqual(g.get_hp(), 6)
        self.assertEqual(g.get_level(), 1)
        self.assertEqual(g.get_attack_damage(), 4)
        self.assertEqual(g.get_speed(), 2)
        self.assertEqual(g.get_defence(), 8)
        self.assertEqual(g.can_evolve(), True)
        self.assertEqual(g.should_evolve(), True)
        g.level_up()
        g.level_up()
        g.level_up()
        self.assertEqual(g.get_hp(), 8)
        self.assertEqual(g.get_level(), 4)
        self.assertEqual(g.get_attack_damage(), 4)
        self.assertEqual(g.get_speed(), 2)
        self.assertEqual(g.get_defence(), 8)
        
        g.lose_hp(5)
        self.assertEqual(str(g), "LV. 4 Gastly: 3 HP")

        g.heal()
        self.assertEqual(str(g), "LV. 4 Gastly: 8 HP")

    def test_haunter_stats(self):
        """ test for Haunter's stats and levelling up """
        h = Haunter()
        self.assertEqual(h.get_hp(), 9)
        self.assertEqual(h.get_level(), 1)
        self.assertEqual(h.get_attack_damage(), 8)
        self.assertEqual(h.get_speed(), 6)
        self.assertEqual(h.get_defence(), 6)
        self.assertEqual(h.can_evolve(), True)
        self.assertEqual(h.should_evolve(), False)
        h.level_up()
        h.level_up()
        self.assertEqual(h.get_hp(), 10)
        self.assertEqual(h.get_level(), 3)
        self.assertEqual(h.get_attack_damage(), 8)
        
        h.lose_hp(5)
        self.assertEqual(str(h), "LV. 3 Haunter: 5 HP")

        h.heal()
        self.assertEqual(str(h), "LV. 3 Haunter: 10 HP")

    def test_gengar_stats(self):
        """ test for the Gengar stats and leveling up """
        ge = Gengar()
        self.assertEqual(ge.get_hp(), 13)
        self.assertEqual(ge.get_level(), 3)
        self.assertEqual(ge.get_attack_damage(), 18)
        self.assertEqual(ge.get_speed(), 12)
        self.assertEqual(ge.get_defence(), 3)
        self.assertEqual(ge.can_evolve(), False)
        self.assertEqual(ge.should_evolve(), False)
        ge.level_up()
        ge.level_up()
        ge.level_up()
        self.assertEqual(ge.get_hp(), 15)
        self.assertEqual(ge.get_level(), 6)
        self.assertEqual(ge.get_attack_damage(), 18)
        self.assertEqual(ge.get_speed(), 12)
        self.assertEqual(ge.get_defence(), 3)
        
        ge.lose_hp(5)
        self.assertEqual(str(ge), "LV. 6 Gengar: 10 HP")

        ge.heal()
        self.assertEqual(str(ge), "LV. 6 Gengar: 15 HP")

    def test_attacking_g_vs_h(self):
        """ testing the attack method """
        RandomGen.set_seed(0)
        g = Gastly()
        h = Haunter()

        g.attack(h)
        self.assertEqual(g.get_hp(), 6)
        self.assertEqual(h.get_hp(), 1)
        self.assertEqual(h.status_effect, "sleep")

    def test_sleep(self):
        """ tests sleep status effect """
        e = Eevee()
        b = Bulbasaur()

        e.status_effect = "sleep"
        
        self.assertEqual(b.get_hp(), 13)
        e.attack(b)
        self.assertEqual(b.get_hp(), 13)

    def test_confusion(self):
        """Tests confusion status effect"""
        RandomGen.set_seed(0)
        ge = Gengar()
        h = Haunter()
        
        ge.status_effect = "confuse"
        
        self.assertEqual(ge.get_hp(), 13)
        ge.attack(h)
        self.assertLess(ge.get_hp(), 13)
        
        
    def test_burn(self):
        """"Tests burn status effect"""
        v = Venusaur()
        s = Squirtle()

        v.status_effect = "burn"
        self.assertEqual(v.get_hp(), 21)
        self.assertEqual(s.get_hp(), 11)
        
        v.attack(s)
        self.assertEqual(v.get_hp(), 20)
        self.assertEqual(s.get_hp(), 9)
    
    def test_poison(self):
        """Tests poison status effect """
        charm = Charmander()
        chariz = Charizard()

        chariz.status_effect = "poison"

        self.assertEqual(charm.get_hp(), 9)
        self.assertEqual(chariz.get_hp(), 15)

        chariz.attack(charm)

        self.assertEqual(charm.get_hp(), -7)
        self.assertEqual(chariz.get_hp(), 12)
        self.assertTrue(charm.is_fainted())
        

    def test_defence_1(self):
        """ tests blastoise's defence calculations"""
        b = Blastoise()

        self.assertEqual(b.get_hp(), 21)
        b.defend(6)
        self.assertEqual(b.get_hp(), 18)

        b.defend(24)
        self.assertEqual(b.get_hp(), -6) 

        self.assertTrue(b.is_fainted())


    def test_defence_2(self):
        """ tests Eevee's defence calculations"""
        e = Eevee()

        self.assertEqual(e.get_hp(), 10)
        e.defend(3)
        self.assertEqual(e.get_hp(), 10)

        e.defend(15)
        self.assertEqual(e.get_hp(), -5) 

        self.assertTrue(e.is_fainted())

    def test_defence_3(self):
        """ tests Squirtle's defence calculations"""
        s = Squirtle()

        self.assertEqual(s.get_hp(), 11)
        s.defend(6)
        self.assertEqual(s.get_hp(), 8)

        s.defend(23)
        self.assertEqual(s.get_hp(), -15) 

        self.assertTrue(s.is_fainted())

    def test_validation(self):
        """ tests validation of PokemonBase init """
        
        self.assertRaises(AssertionError, lambda: Haunter(-1, 0))
        self.assertRaises(AssertionError, lambda: Haunter(4, 60))
    

  
if __name__=="__main__":
    unittest.main()