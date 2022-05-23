class Plant():
    max_hp: int
    id: int
    new_plant: bool
    hp: int

    def __init__(self, id_number, new_plant: bool = False):
        self.max_hp = 8
        self.id = id_number
        self.new_plant = new_plant
        self.hp = self.max_hp

    def set_hp(self, hp: int):
        self.hp = hp if hp > 0 else 0

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def set_id(self, id_pl: int):
        self.id = id_pl

    def get_id(self):
        return self.id

    def set_new_plant(self, value: bool):
        self.new_plant = value

    def info(self, full_info_or_not) -> str:
        if full_info_or_not:
            info_plant = 'Plant №{} hp:{}'.format(self.id, self.hp)
        else:
            info_plant = 'Pl№{} hp:{}'.format(self.id, self.hp)
        return info_plant

    def is_new_plant(self) -> bool:
        return self.new_plant

    def next_step(self) -> bool:
        if self.hp > 1:
            self.hp -= 1
            return True
        else:
            return False
