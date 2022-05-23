from Model.Animal import Animal
from Model.Plant import Plant


class Cell:
    __column_index: int
    __line_index: int
    Plant: Plant
    __animals: list[Animal]

    def __init__(self, raw_index: int, column_index: int, plant_on_cell: Plant = None, animals: list[Animal] = []) -> None:
        if len(animals) > 4 or len(animals) == 4 and Plant:
            raise "Ошибка ввода"
        self.__column_index = column_index
        self.__line_index = raw_index
        self.Plant = plant_on_cell
        self.__animals = animals

    def add_animal_to_cell(self, animal: Animal) -> bool:
        can_add = not (len(self.__animals) == 3 and self.get_plant_on_cell()) or len(self.__animals) == 4
        if can_add:
            self.__animals.append(animal)
            return True
        return False

    def is_animal_another_sex(self, animal: Animal):
        animal_type = animal.get_animal_type()
        for animal_in_cell in self.__animals:
            if animal_in_cell.get_animal_type() == animal_type and animal_in_cell.get_sex() != animal.get_sex():
                return animal_in_cell
        return None

    def find_herbivore(self) -> Animal:
        if self.__animals is not None:
            for animal in self.__animals:
                if animal.get_animal_type() in ['Bison', 'Deer', 'Rabbit']:
                    return animal
        return None

    def get_column_index(self) -> int:
        return self.__column_index

    def get_line_index(self) -> int:
        return self.__line_index

    def get_plant_on_cell(self) -> Plant:
        return self.Plant

    def delete_animal(self, animal: Animal) -> None:
        if animal in self.__animals:
            self.__animals.remove(animal)

    def info(self, full_type=False) -> list[str]:
        str_empty_place = "        -       "
        string_describing_cell = []
        if self.get_plant_on_cell():
            string_describing_cell.append("     " + self.Plant.info(full_type) + '     ')
        for animal in self.__animals:
            string_describing_cell.append("    " + animal.info(full_type))
        string_describing_cell += [
            str_empty_place for index in range(4 - len(string_describing_cell))
        ]
        return string_describing_cell

    def get_animals_in_cell(self) -> list[Animal]:
        return self.__animals

    def delete_plant(self) -> None:
        if not self.Plant:
            raise 'Растения в этой клетке не существует'
        self.Plant = None

    def next_step(self):
        if self.Plant and not self.Plant.next_step():
            self.delete_plant()

        animal_will_die = [animal for animal in self.__animals if not animal.next_step()]
        for animal in animal_will_die:
            self.delete_animal(animal)

    def add_plant_to_cell(self, plant_id: int):
        if self.Plant and len(self.__animals) == 4:
            raise "В клетке нету места!"
            return False

        self.Plant = Plant(plant_id, True)
        return True

    def amount_inhabitant(self) -> int:
        is_plant = int(self.Plant is not None)
        return is_plant + len(self.__animals)

