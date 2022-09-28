''' PokemonBase ADT and PokeType implementation
    Defines a generic PokemonBase with expected/needed methods shared by all Pokemon,
    as well as implemented the PokeType class
'''

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from enum import IntEnum
from random_gen import RandomGen
T = TypeVar('T')

__author__ = "Scaffold by Jackson Goerner, Code by Felicty, Virani, Dylan, and Edward"

class PokemonBase(ABC, Generic[T]):
    """ A base class for all pokemon
    
    Attributes:
        level (int): level of pokemon
        hp (int): current hp of pokemon
        poke_type (PokeType): poke type of pokemon
        initial_index (int): index of poke in the intial ordering of a poke team (used in battle modes 2 & 3)
        status_effect (string or None): the present status effect on the pokemon
 
    Complexity:
        unless otherwise stated, all methods in this class and child classes have a complexity of O(1)
    """

    class PokeType(IntEnum):
        ''' A class which enmurates each possible type,
            allowing access based on ATTACK_MULTIPLIERS
        '''
        FIRE = 0
        GRASS = 1
        WATER = 2
        GHOST = 3
        NORMAL = 4

    ATTACK_MULTIPLIERS = [
        [1, 2, 0.5, 1, 1],          # fire attacking
        [0.5, 1, 2, 1, 1],          # grass attacking
        [2, 0.5, 1, 1, 1],          # water attacking
        [1.25, 1.25, 1.25, 2, 0],   # ghost attacking
        [1.25, 1.25, 1.25, 0, 1]    # normal attacking
    ]
    # eg PokemonBase.ATTACK_MULTIPLIERS[PokemonBase.PokeTypes.WATER][PokemonBase.PokeTypes.GRASS] = 0.5 (row 3 column 2)

    STATUS_EFFECTS = ["burn", "poison", "paralysis", "sleep", "confuse"]
    # eg PokemonBase.STATUS_EFFECTS[PokemonBase.PokeTypes.FIRE] = "Burn"    

    POKEDEX_ORDER = ["Charmander", "Charizard", "Bulbasaur", "Venusaur", "Squirtle",
                        "Blastoise", "Gastly", "Haunter", "Gengar", "Eevee"]


    def __init__(self, level: int, hp: int, poke_type) -> None:
        """ Initialisation 
        :pre: that level and hp are non-negative integers and poke_type is a PokeType
        """
        assert type(level) == int and level >= 1
        self.level = level
        
        assert type(hp) == int and hp > 0
        self.hp = hp
        
        assert type(poke_type) == PokemonBase.PokeType, "poke type is not a valid type"
        self.poke_type = poke_type

        self.status_effect = "free"
        self.initial_index = None

    def is_fainted(self) -> bool:
        """
        Returns boolean, whether pokemon is fainted or not
        Cond: if health below or equal to 0
        """
        hp = self.hp
        return hp <= 0

    def level_up(self) -> None:
        """ Levels up Pokemon and readjusts Pokemon's hp accordingly"""
        self.level += 1
        self.hp = self.get_max_hp(self.level) - (self.get_max_hp(self.level - 1) - self.hp)

    # getter methods
    
    def get_level(self) -> int:
        """ Returns level of pokemon """
        return self.level

    def get_hp(self) -> int:
        """ Returns hp of pokemon"""
        return self.hp

    @abstractmethod
    def get_speed(self) -> int:
        """ Returns speed of pokemon """
        pass

    @abstractmethod
    def get_attack_damage(self) -> int:
        """ Returns attack damage """
        pass

    @abstractmethod
    def get_defence(self) -> int:
        """ Returns the pokemon's defence stat """
        pass

    @abstractmethod
    def get_max_hp(self, level) -> int:
        """ returns the pokemon's max hp """
        pass

    def lose_hp(self, lost_hp: int) -> None:
        """ Reinitialises new hp after damage """
        assert type(lost_hp) == int and lost_hp >= 0

        self.hp -= lost_hp

    @abstractmethod
    def defend(self, damage: int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        pass

    def attack(self, other: PokemonBase) -> None:
        """ Performs attack on another PokemonBase instance 
        :pre: assumes that neither pokemon has fainted
        """
        
        #Step 1: Status effects on attack damage / redirecting attacks
        if self.status_effect == "sleep":       # O(1) - constant length strings
            return
        if self.status_effect == "confuse":     # O(1) 
            if RandomGen.random_chance(0.5):    
                other = self

        #Step 2: Do the attack
        attack_damage = int(self.get_attack_damage() * self.ATTACK_MULTIPLIERS[self.poke_type][other.poke_type])
        if self.status_effect == "burn":
            attack_damage = attack_damage // 2        
        other.defend(attack_damage)

        #Step 3: Losing hp to status effects
        if self.status_effect == "burn":
            self.lose_hp(1)
        
        elif self.status_effect == "poison":
            self.lose_hp(3)
        
        #Step 4: Possibly applying status effects
        if RandomGen.random_chance(0.2):
            other.status_effect = self.STATUS_EFFECTS[self.poke_type]


    @abstractmethod
    def get_poke_name(self) -> str:
        """ Returns name of Pokemon """
        pass
    def __str__(self) -> str:
        """ Returns a string representation of the pokemon """
        return f"LV. {self.level} {self.get_poke_name()}: {self.hp} HP"

    def should_evolve(self) -> bool:
        """ Returns if Pokemon should evolve based on their level, False by default """
        return False

    def can_evolve(self) -> bool:
        """ Returns if pokemon can evolve based on their level, False by default """
        return False

    def get_evolved_version(self) -> PokemonBase:
        """Returns evolved instance of Pokemon, 
        is overridden in each pokemon class if the pokemon can evolve
        raises an error if not overridden
        """
        raise Exception("This pokemon cannot evolve")

    def get_pokedex_index(self) -> int:
        ''' Returns the reverse index of the pokemon with respect to the POKEDEX_ORDER'''
        return len(PokemonBase.POKEDEX_ORDER) - PokemonBase.POKEDEX_ORDER.index(self.get_poke_name())

    def heal(self):
        '''sets hp of pokemon back to max hp'''
        self.hp = self.get_max_hp(self.level)
        self.status_effect = "free"
    
   

