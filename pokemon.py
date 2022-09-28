""" 
Individual pokemon class definitions, implementing abstract methods from pokemon_base

Unless otherwise stated, best/worst case complexity for each method in each pokemon_base child is O(1)
"""

__author__ = "Scaffold by Jackson Goerner, Code by Felicity, Virani, Dylan, Edward"

from pokemon_base import PokemonBase

class Charizard(PokemonBase):
    """ A Charizard class
    evolves from: Charmander
    """
    BASE_LEVEL = 3
    def __init__(self, level:int = BASE_LEVEL, hp_dif:int = 0):
        """ initialising the Charizard to base values 
        args:
            level (int) - the level of the pokemon 
            hp_dif (int) - the difference between the poke's hp and it's max hp, defaulted to 0
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level) - hp_dif, PokemonBase.PokeType.FIRE)

    # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Charizard"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 12 + 1 * level

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 10 + 2 * self.level
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 9 + 1 * self.level
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 4

    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        defence = self.get_defence()

        if damage > defence:
            self.lose_hp(damage * 2)
        else:
            self.lose_hp(damage)


class Charmander(PokemonBase):
    """ A Charmander class
    evolves to: Charmander
    """   
    BASE_LEVEL = 1
    def __init__(self, level: int = BASE_LEVEL):
        """ initialising the Charmander to base values
        args:
            level (int) - the level of the pokemon 
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level), PokemonBase.PokeType.FIRE)

    # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Charmander"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 8 + 1*level

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 6 + 1 * self.level
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 7 + 1 * self.level
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 4

    # other methods
    def should_evolve(self) -> bool:
        """
        Returns whether Pokemon should evolve
        Level must be equal to or greater than level of Pokemon it will evolve into
        """
        return self.level >= Charizard.BASE_LEVEL

    def can_evolve(self) -> bool:
        """ Returns whether Pokemon has ability to evolve """
        return True

    def get_evolved_version(self) -> PokemonBase:
        """Evolves current Pokemon, instantiates evolved PokemonBase"""

        evolved_poke = Charizard(self.level, self.get_max_hp(self.level) - self.hp)
        evolved_poke.initial_index = self.initial_index
        evolved_poke.status_effect = self.status_effect
        return evolved_poke

    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        defence = self.get_defence()

        if damage > defence:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

class Venusaur(PokemonBase):
    """ A Venusaur class
    evolves from: Bulbasaur
    """
    BASE_LEVEL = 2
    def __init__(self, level: int = BASE_LEVEL, hp_dif: int = 0):
        """ initialising the Venusaur to base values
        
        args:
            level (int) - the level of the pokemon 
            hp_dif (int) - the difference between the poke's hp and it's max hp
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level) - hp_dif, PokemonBase.PokeType.GRASS)

    # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Venusaur"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 20 + level // 2

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 5
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 3 + (self.level // 2)
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 10

    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        defence = self.get_defence()

        if damage > defence + 5:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

class Bulbasaur(PokemonBase):
    """ A Bulbasaur class
    evolves to: Venusaur
    """
    BASE_LEVEL = 1
    def __init__(self, level: int = BASE_LEVEL):
        """ initialising the Bulbasaur to base values
        args:
            level (int) - the level of the pokemon 
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level), PokemonBase.PokeType.GRASS)

    # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Bulbasaur"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 12 + 1 * level

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 5
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 7 + (self.level // 2)
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 5

    def should_evolve(self) -> bool:
        """
        Returns whether Pokemon should evolve
        Level must be equal to or greater than level of Pokemon it will evolve into
        """
        return self.level >= Venusaur.BASE_LEVEL

    def can_evolve(self) -> bool:
        """Returns whether Pokemon has ability to evolve"""
        return True

    def get_evolved_version(self) -> PokemonBase:
        """Evolves current Pokemon, instantiates evolved PokemonBase"""
        
        evolved_poke = Venusaur(self.level, self.get_max_hp(self.level) - self.hp)
        evolved_poke.initial_index = self.initial_index
        evolved_poke.status_effect = self.status_effect
        return evolved_poke
        

    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        defence = self.get_defence()

        if damage > (defence + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage // 2)



class Blastoise(PokemonBase):
    """ A Blastoise class
    evolves from: Squirtle
    """
    BASE_LEVEL = 3
    def __init__(self, level: int = BASE_LEVEL, hp_dif: int = 0):
        """ initialising the Blastoise to base values 
        args:
            level (int) - the level of the pokemon 
            hp_dif (int) - the difference between the poke's hp and it's max hp
    
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level) - hp_dif, PokemonBase.PokeType.WATER)
    
     # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Blastoise"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 15 + 2 * level

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 8 + (self.level // 2)
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 10
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 8 + 1 * self.level
    
    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        defence = self.get_defence()

        if damage > 2*defence:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

class Squirtle(PokemonBase):
    """ A Squirtle class
    evolves to: Blastoise
    """
    BASE_LEVEL = 1
    def __init__(self, level: int = BASE_LEVEL):
        """ initialising the Squirtle to base values 
        args:
            level (int) - the level of the pokemon 
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level), PokemonBase.PokeType.WATER)
     
     # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Squirtle"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 9 + 2 * level

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 4 + (self.level // 2)
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 7
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 6 + self.level

    def should_evolve(self) -> bool:
        """
        Returns whether Pokemon should evolve
        Level must be equal to or greater than level of Pokemon it will evolve into
        """
        return self.level >= Blastoise.BASE_LEVEL

    def can_evolve(self) -> bool:
        """Returns whether Pokemon has ability to evolve"""
        return True

    def get_evolved_version(self) -> PokemonBase:
        """Evolves current Pokemon, instantiates evolved PokemonBase"""
        
        evolved_poke = Blastoise(self.level, self.get_max_hp(self.level) - self.hp)
        evolved_poke.initial_index = self.initial_index
        evolved_poke.status_effect = self.status_effect
        return evolved_poke
    
    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        defence = self.get_defence()

        if damage > 2*defence:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

class Gengar(PokemonBase):
    """ A Gengar class
    evolves from: Haunter
    """
    BASE_LEVEL = 3
    def __init__(self, level: int = BASE_LEVEL, hp_dif: int = 0):
        """ initialising the Gengar to base values 
        args:
            level (int) - the level of the pokemon 
            hp_dif (int) - the difference between the poke's hp and it's max hp
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level) - hp_dif, PokemonBase.PokeType.GHOST)
        # evolves from Haunter

     # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Gengar"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 12 + (level//2)

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 18
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 12
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 3

    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        
        self.lose_hp(damage)

class Haunter(PokemonBase):
    """ A Haunter class
    evolves to: Gengar
    evolves from: Gastly
    """
    BASE_LEVEL = 1
    def __init__(self, level:int = BASE_LEVEL, hp_dif: int = 0):
        """ initialising the Haunter to base values 
        args:
            level (int) - the level of the pokemon 
            hp_dif (int) - the difference between the poke's hp and it's max hp, defaulted to 0
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level) - hp_dif, PokemonBase.PokeType.GHOST)

     # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Haunter"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 9 + (level//2)

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 8
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 6
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 6

    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        
        self.lose_hp(damage)

    # other methods  
    def should_evolve(self) -> bool:
        """
        Returns whether Pokemon should evolve
        Level must be equal to or greater than level of Pokemon it will evolve into
        """
        return self.level >= Gengar.BASE_LEVEL

    def can_evolve(self) -> bool:
        """Returns whether Pokemon has ability to evolve"""
        return True

    def get_evolved_version(self) -> PokemonBase:
        """Evolves current Pokemon, instantiates evolved PokemonBase"""

        evolved_poke = Gengar(self.level, self.get_max_hp(self.level) - self.hp)
        evolved_poke.initial_index = self.initial_index
        evolved_poke.status_effect = self.status_effect
        return evolved_poke

class Gastly(PokemonBase):
    """ A Gastly class
    evolves to: Gengar
    """
    BASE_LEVEL = 1
    def __init__(self, level:int = BASE_LEVEL):
        """ initialising the Ghastly to base values 
        args:
            level (int) - the level of the pokemon 
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level), PokemonBase.PokeType.GHOST)


     # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Gastly"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 6 + (level // 2)

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 4
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 2
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 8

    # other methods  
    def should_evolve(self) -> bool:
        """
        Returns whether Pokemon should evolve
        Level must be equal to or greater than level of Pokemon it will evolve into
        """
        return self.level >= Haunter.BASE_LEVEL

    def can_evolve(self) -> bool:
        """Returns whether Pokemon has ability to evolve"""
        return True

    def get_evolved_version(self) -> PokemonBase:
        """Evolves current Pokemon, instantiates evolved PokemonBase"""
        evolved_poke =  Haunter(self.level, self.get_max_hp(self.level) - self.hp)
        evolved_poke.initial_index = self.initial_index
        evolved_poke.status_effect = self.status_effect
        return evolved_poke
    
    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        self.lose_hp(damage)

class Eevee(PokemonBase):
    """ An Eevee class"""
    BASE_LEVEL = 1
    def __init__(self, level:int = BASE_LEVEL):
        """ initialising the Eevee to base values 
        args:
            level (int) - the level of the pokemon 
        """
        PokemonBase.__init__(self, level, self.get_max_hp(level), PokemonBase.PokeType.NORMAL)
        
     # getter methods
    def get_poke_name(self):
        """ Returns name of pokemon"""
        return "Eevee"

    def get_max_hp(self, level):
        """ calculates the max hp based on the current level """
        return 10

    def get_attack_damage(self):
        """ calculates the attack value based on the current level """
        return 6 + self.level
    
    def get_speed(self):
        """ calculates the speed value based on the current level """
        return 7 + self.level
    
    def get_defence(self):
        """ calculates the defence value based on the current level """
        return 4 + self.level

    # other methods       
    def defend(self, damage:int) -> None:
        """ takes in damage as a parameter and then calculates how much hp is lost """
        defence = self.get_defence()

        if damage >= defence:
            self.lose_hp(damage)


 