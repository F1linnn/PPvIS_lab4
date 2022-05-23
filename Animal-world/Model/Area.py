import os.path
from typing import List, Tuple, Optional, Union, Any
from Model.Cell import Cell
from Model.Animal import Animal
from Model.Plant import Plant
from Utility.parsers.dom_writer import XmlWriter
from Utility.parsers.sax_reader import XmlReader
import random
import pandas as pd

NUMBER_OF_COLUMNS = 4
NUMBER_OF_ROWS = 4


class Area:
    _len: int
    _width: int
    _last_id: int
    _area: list[list[Cell]]
    _log_inhab: str
    
    def __init__(self, area: list[list[Cell]], last_id) -> None:
        self._area = area
        self._len = NUMBER_OF_ROWS
        self._width = NUMBER_OF_COLUMNS
        self._log_inhab = ""
        self._last_id = last_id
        for area_row in area:
            if len(area_row) != self._width:
                raise "Area should be rectangular size"

    def move_choise(self) -> None:
        for cell_line in self._area:
            for cell in cell_line:
                for animal_in_cell in cell.get_animals_in_cell():
                    move_choise = animal_in_cell.move_choise()
                    if move_choise == 'I cant move':
                        continue
                    if move_choise == 'Dead':
                        self._log_inhab += animal_in_cell.get_animal_type() + ' Is dead |'
                        cell.delete_animal(animal_in_cell)
                    if move_choise == 'Find eat':
                        self.find_eat(cell, animal_in_cell)
                        continue
                    if move_choise == 'Find partner':
                        if not self.find_partner(cell, animal_in_cell):
                            neighbors_cells = self.get_neighbors_cells(cell, animal_in_cell.get_speed())
                            self.move_between_cells(animal_in_cell, cell,
                                                    neighbors_cells[random.randint(0, len(neighbors_cells) - 1)])
                            animal_in_cell.set_move_or_no(False)
        self.all_animal_can_move()

    def find_eat_herbivore(self, herbivore: Animal, cell_with_herbivore: Cell) -> None:
        if cell_with_herbivore.get_plant_on_cell():
            self.eat_plant(herbivore, cell_with_herbivore, cell_with_herbivore)
            return
        cells_for_move = self.get_neighbors_cells(cell_with_herbivore, herbivore.get_speed())
        for to_this_cell in cells_for_move:
            if to_this_cell.get_plant_on_cell() and to_this_cell.amount_inhabitant() < 4:
                self.move_between_cells(herbivore, cell_with_herbivore, to_this_cell)
                herbivore.set_move_or_no(False)
                self.eat_plant(herbivore, to_this_cell, to_this_cell)
                return
        self.move_between_cells(herbivore, cell_with_herbivore,
                                cells_for_move[random.randint(0, len(cells_for_move) - 1)])
        herbivore.set_move_or_no(False)
        return

    def find_eat_predator(self, predator: Animal, cell_predator: Cell) -> None:
        if cell_predator.find_herbivore() is not None:
            self.kill_animal(predator, cell_predator.find_herbivore(), cell_predator)
            return
        cell_neighbors = self.get_neighbors_cells(cell_predator, predator.get_speed())
        for cell_eat in cell_neighbors:
            if cell_eat.find_herbivore() and cell_eat.amount_inhabitant() < 4:
                self.move_between_cells(predator, cell_predator, cell_eat)
                predator.set_move_or_no(False)
                self.kill_animal(predator, cell_eat.find_herbivore(), cell_eat)
                return

    def find_eat(self, cell_animal: Cell, animal: Animal) -> None:
        if animal.get_animal_type() in ['Bison', 'Rabbit', 'Deer']:
            self.find_eat_herbivore(animal, cell_animal)
        else:
            self.find_eat_predator(animal, cell_animal)

    def find_partner(self, cell_animal: Cell, animal: Animal) -> bool:
        neighbors_cells = [cell_animal] + self.get_neighbors_cells(cell_animal, animal.get_speed())
        for cell in neighbors_cells:
            if cell.is_animal_another_sex(animal) and cell.amount_inhabitant() <= 3:
                if not cell == cell_animal:
                    self.move_between_cells(animal, cell_animal, cell)
                    animal.set_move_or_no(False)
                self.reproduction_animals(cell, animal)
                self._log_inhab += f'{animal.get_animal_type()} {animal.get_animal_id()} with animal {cell.is_animal_another_sex(animal).get_animal_type()} {cell.is_animal_another_sex(animal).get_animal_id()} spawn baby {animal.get_animal_type()} {self._last_id} |'
                return True
        return False

    def get_neighbors_cells(self, cell: Cell, move_speed: int):
        line_index = cell.get_line_index()
        column_index = cell.get_column_index()
        result = []
        while move_speed:
            if column_index - move_speed >= 0:
                result.append(self._area[column_index - move_speed][line_index])

            if column_index + move_speed < self._width:
                result.append(self._area[column_index + move_speed][line_index])

            if line_index - move_speed >= 0:
                result.append(self._area[column_index][line_index - move_speed])

            if line_index + move_speed < self._len:
                result.append(self._area[column_index][line_index + move_speed])

            move_speed -= 1

        return result

    def move_between_cells(self, animal: Animal, first_cell: Cell, second_sell: Cell) -> bool:
        if first_cell == second_sell:
            return True
        else:
            second_sell.add_animal_to_cell(animal)
            first_cell.delete_animal(animal)
            self._log_inhab += animal.get_animal_type() + f'{animal.get_animal_id()} --> Cell({second_sell.get_column_index()},{second_sell.get_line_index()}) | '
            return True

    def reproduction_plant(self, cell_plant: Cell):
        if not cell_plant.get_plant_on_cell() or cell_plant.get_plant_on_cell().is_new_plant():
            return
        neighbors_cells = self.get_neighbors_cells(cell_plant, 1)
        for cell in neighbors_cells:
            if cell.get_plant_on_cell() and cell.get_plant_on_cell().get_hp() < cell.get_plant_on_cell().get_max_hp():
                cell.get_plant_on_cell().set_hp(cell.get_plant_on_cell().get_max_hp())
                self._log_inhab += f' Pl-{cell_plant.get_plant_on_cell().get_id()} heal plant {cell.get_plant_on_cell().get_id()} | '
            elif cell.amount_inhabitant() < 4 and not cell.get_plant_on_cell():
                self._last_id += 1
                cell.add_plant_to_cell(self._last_id)
                self._log_inhab += f' Pl- {cell_plant.get_plant_on_cell().get_id()} spawn plant {cell.get_plant_on_cell().get_id()} | '
                return

    @property
    def generate_sex(self) -> str:
        if random.randint(0, 1) == 1:
            return 'm'
        else:
            return 'f'
    
    def reproduction_animals(self, cell_with_animals: Cell, animal_type: Animal):
        type_a = animal_type.get_animal_type()
        self._last_id += 1
        new_animal = Animal(type_a, self.generate_sex, self._last_id, False)
        cell_with_animals.add_animal_to_cell(new_animal)

    def start_reproduction_all_plants(self):
        for cell_line in self._area:
            for cell in cell_line:
                self.reproduction_plant(cell)
        for cell_line in self._area:
            for cell in cell_line:
                if cell.get_plant_on_cell():
                    cell.get_plant_on_cell().set_new_plant(False)

    def check_all_hp_in_world(self) -> None:
        for cell_line in self._area:
            for cell in cell_line:
                cell.next_step()

    @staticmethod
    def get_random_nearest_cell(nearest_cells: list[Cell]):
        return nearest_cells[random.randint(0, len(nearest_cells) - 1)]

    def all_animal_can_move(self) -> None:
        for cell_line in self._area:
            for cell in cell_line:
                for animal in cell.get_animals_in_cell():
                    animal.set_move_or_no(True)

    def eat_plant(self, animal: Animal, cell_with_animal: Cell, cell_with_plant: Cell):
        max_satiety = animal.get_max_satiety()
        satiety = animal.get_satiety()
        plant_hp = cell_with_plant.get_plant_on_cell().get_hp()

        if max_satiety - satiety < plant_hp:
            animal.set_satiety(max_satiety + 1)
            cell_with_plant.get_plant_on_cell().set_hp(plant_hp - (max_satiety - satiety))
            self._log_inhab += animal.get_animal_type() + f'{animal.get_animal_id()} eaten some Pl-{cell_with_plant.get_plant_on_cell().get_id()} |'
            return
        else:
            animal.set_satiety(satiety + plant_hp)
            cell_with_plant.get_plant_on_cell().set_hp(0)
            self._log_inhab += animal.get_animal_type() + f'{animal.get_animal_id()} eaten full Pl-{cell_with_plant.get_plant_on_cell().get_id()} |'

    def kill_animal(self, predator: Animal, herbivore: Animal, cell_herbivore: Cell) -> None:
        if predator.get_speed() < herbivore.get_speed() and random.randint(0, 1) == 1:
            self._log_inhab += predator.get_animal_type() + f'{predator.get_animal_id()} cant catch {herbivore.get_animal_type()} {herbivore.get_animal_id()} | '
            return
        satiety = predator.get_satiety()
        hp_herbivore = herbivore.get_satiety()
        predator.set_satiety(satiety + hp_herbivore)
        self._log_inhab += predator.get_animal_type() + f'{predator.get_animal_id()} kill and eat {herbivore.get_animal_type()} {herbivore.get_animal_id()} |'
        cell_herbivore.delete_animal(herbivore)
    

    def transform_area_into_matrix_form(self) -> list[list[list[str]]]:
        matrix_form = []
        for raw_index in range(self._len):
            row_temp = []
            for column_index in range(self._width):
                str_temp = []
                for str_index in range(4):
                    str_temp.append(self._area[raw_index][column_index].info(full_type=True)[str_index])
                row_temp.append(str_temp)
            matrix_form.append(row_temp)
        return matrix_form

    def display_area(self) -> None:
        for raw_index in range(self._len):
            for str_index in range(4):
                str_temp = ''
                for column_index in range(self._width):
                    str_temp += self._area[raw_index][column_index].info(
                    )[str_index] + '      '
                print(str_temp)
            print('\n')
        # split log with \n
        for index in range(len(self._log_inhab) // 170):
            self._log_inhab = self._log_inhab[:(index + 1) * 170] + "\n" + self._log_inhab[(index + 1) * 170:]
        print('___________LOG____________\n', self._log_inhab)

    def next_step(self, gui=False) -> str:
        self._log_inhab = ''
        self.move_choise()
        self.start_reproduction_all_plants()
        self.check_all_hp_in_world()
        if not gui:
            self.display_area()
        if gui:
            return self._log_inhab

    def get_length(self) -> int:
        return self._len

    def get_width(self) -> int:
        return self._width

    def menu(self):
        key = 1
        while key:
            print("\n \n List of possible choices: \n \
                           1 - move to the next step.  \n \
                           2 - create new plant.  \n \
                           3 - create new animal. \n \
                           4 - exit and save. \n \
                           5 - exit and doesn't save \n\
                       ")
            key = int(input("Key value:"))
            if key == 1:
                self.next_step()
            elif key == 2:
                self.create_plant()
            elif key == 3:
                self.create_animal()
            elif key == 4:
                path = input("Type name of the file: ")
                self.save_in_file(path)
                exit()
            elif key == 5:
                exit()
            else:
                print("Uncorrect key value. Try again.")

    def create_plant(self):
        row_index = int(input('Row index:'))
        line_index = int(input('Line index:'))
        if row_index >= self._width or line_index >= self._len:
            print("Line index or Row index error!")
            return

        cell = self._area[row_index][line_index]
        if cell.get_plant_on_cell() is not None:
            print("This cell have a plant!")
            return
        self._last_id += 1
        cell.add_plant_to_cell(self._last_id)
        print('Plant added to cell!')
        self.display_area()

    def create_animal_gui(self, animal_type, row_index, column_index) -> bool:
        sex = self.generate_sex
        print(sex)
        cell = self._area[row_index][column_index]
        if animal_type == "Plant":
            has_place = cell.add_plant_to_cell(self._last_id + 1)
            if has_place:
                self._last_id += 1
            return has_place
        else:
            animal = Animal(animal_type, sex, self._last_id + 1)
            has_place = cell.add_animal_to_cell(animal)
            if has_place:
                self._last_id += 1
            return has_place

    def create_animal(self):
        row_index = int(input('Row index:'))
        line_index = int(input('Line index:'))
        if row_index >= self._width or line_index >= self._len:
            print("Line index or Row index error!")
            return

        animal_type = str(input("Input type of animal (Bison,Deer,Wolf,Rabbit,Lion):"))
        if animal_type not in ['Bison', 'Deer', 'Rabbit', 'Lion', 'Wolf']:
            print("Uncorrect type animal!")
            return
        sex = str(input("Input animal sex male - m or female - f :"))
        if sex not in ['f', 'm']:
            print("Uncorrect sex!")
            return
        cell = self._area[row_index][line_index]
        if cell.amount_inhabitant() == 4:
            print("Max inhabitants on plant(4/4")
            return
        
        animal = Animal(animal_type, sex, self._last_id, True)
        self._last_id += 1
        cell.add_animal_to_cell(animal)
        print("Animal was added!")
        self.display_area()

    def save_in_file(self, path):
        ides = []
        animal_types = []
        row_indices = []
        column_indices = []
        sex = []
        for cell_row in self._area:
            for cell in cell_row:
                row_index = cell.get_line_index()
                column_index = cell.get_column_index()
                if cell.get_plant_on_cell():
                    ides.append(cell.get_plant_on_cell().get_id())
                    animal_types.append('Plant')
                    row_indices.append(row_index)
                    column_indices.append(column_index)
                    sex.append('none')
                for animal in cell.get_animals_in_cell():
                    ides.append(animal.get_animal_id())
                    animal_types.append(animal.get_animal_type())
                    row_indices.append(row_index)
                    column_indices.append(column_index)
                    animal_sex = animal.get_sex()
                    animal_sex = 'female' if animal_sex == 'f' else 'male'
                    sex.append(animal_sex)
        write = XmlWriter(path)
        data_dict = {}
        for element_index in range(len(ides)):
            data_dict["id"] = str(ides[element_index])
            data_dict["type"] = animal_types[element_index]
            data_dict["row_index"] = str(row_indices[element_index])
            data_dict["column_index"] = str(column_indices[element_index])
            data_dict["sex"] = sex[element_index]
            write.create_animals(data_dict)
        write.create_xml_file()


    @staticmethod
    def transform_df_into_inh_list(df: pd.DataFrame) -> tuple[list[Animal], Optional[Plant]]:
        output = []
        plant = None
        for ind, row in df.iterrows():
            type = row.Animal_type
            animal_sex = 'm' if row.Sex == 'male' else 'f'
            if type == 'Plant':
                plant = Plant(id_number=row.id)
            else:
                animal = Animal(type, animal_sex, animal_id=row.id)
                output.append(animal)
        return output, plant


def create_area_from_database(file_name: str) -> Area:
    length = NUMBER_OF_ROWS
    width = NUMBER_OF_COLUMNS
    reader = XmlReader()
    reader.parser.setContentHandler(reader)
    try:
        reader.parser.parse(f"XML/{file_name}")
    except ValueError:
        print("File not found")
        return None
    data = reader.table_data
    all_cells = []
    cell_inh_data = pd.DataFrame(
        data=data,
        columns=[
            'id', 'Animal_type', 'Cell_row_index', 'Cell_column_index', 'Sex'
        ],
    )
    id = cell_inh_data.id.max()
    if cell_inh_data.shape[0] == 0:
        id = 0
    for row_index in range(length):
        cell_row = []
        for column_index in range(width):
            selected_inh_data = cell_inh_data.query(
                "Cell_row_index == @row_index & Cell_column_index == @column_index"
            )
            inhabitant_list, plant = Area.transform_df_into_inh_list(
                selected_inh_data)
            cell_row.append(
                Cell(row_index, column_index, plant, inhabitant_list))
        all_cells.append(cell_row)
    return Area(all_cells, id)
