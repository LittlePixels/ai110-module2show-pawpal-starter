class Dog:
    def __init__(self, location: str, type_of_food: str, type_of_shampoo: str):
        self.__location = location          # private: where the walk takes place
        self.__type_of_food = type_of_food        # private: what the dog eats
        self.__type_of_shampoo = type_of_shampoo  # private: shampoo used for bathing

    def walk_on_leash(self):
        pass

    def eat_food(self):
        pass

    def bath_in_water(self):
        pass
