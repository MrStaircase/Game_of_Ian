class Entity:
    def __init__(self, character = " ", hp = 0, position=(0, 0)):
        self.hp = hp
        self.position = position
        self.character = character

    def __str__(self):
        return self.character
    
    def get_position(self):
        return self.position
    
    def get_hp(self):
        return self.hp

    def gain_damage(self, damage):
        assert(isinstance(damage, int))
        assert(damage >= 0)
        self.hp = max(self.hp - damage, 0)

    def change_position(self, x, y):
        self.position = (x, y)
    
    def attack(self, target, range, damage):
        assert(isinstance(target, Entity))
        assert(isinstance(range, int))
        assert(isinstance(damage, int))
        if abs(self.get_position()[0] - target.get_position()[0]) + abs(self.get_position()[1] - target.get_position()[1]) <= range:
            target.gain_damage(damage)
        else:
            print("out of range")

class Enemy(Entity):
    def __init__(self, character= "E", hp = 0, position=(0, 0)):
        super().__init__(character=character, hp=hp, position=position)
    
    def __str__(self):
        return super().__str__()

class Playable_Character(Entity):
    def __init__(self, character= "P", hp = 0, role = "fighter", position=(0, 0)):
        super().__init__(character=character, hp=hp, position=position)
        self.role = role

    def __str__(self):
        return super().__str__()

class Item:
    def __init__(self, name = "item"):
        self.name = name

class Weapon(Item):
    def __init__(self, name="item", damage = 0, range = 0):
        assert(range >= 0)
        super().__init__(name)
        self.damage = damage
        self.range = range

class Board:
    def __init__(self, size = 9):
        assert(isinstance(size, int))
        assert(size > 0)
        self.size = size
        self.enemies = []
        self.playable_characters = []
        self.position_dict = {}
        for enemy in self.enemies:
            self.position_dict[enemy.position] = enemy
        for playable_character in self.playable_characters:
            self.position_dict[playable_character.position] = playable_character

    def place_entity(self, entity):
        assert(isinstance(entity, Entity))
        self.position_dict[entity.position] = entity
        if(isinstance(entity, Enemy)):
            self.enemies.append(entity)
        elif(isinstance(entity, Playable_Character)):
            self.playable_characters.append(entity)

    def print_board(self):
        output = ""
        for i in range(self.size):
            for j in range(self.size):
                output += self.position_dict[(i, j)].character + " | " if (i, j) in self.position_dict.keys() else "  | "
            output = output[:-2] + "\n- + - + - + - + - + - + - + - + -\n"
        output = output[:-(self.size*4)]
        print(output)
    
    def get_info(self, query_request):
        assert(isinstance(query_request, tuple))
        assert(len(query_request) == 2)
        assert(isinstance(query_request[0], str))
        assert(isinstance(query_request[1], tuple))
        assert(isinstance(query_request[1][0], int))
        assert(isinstance(query_request[1][1], int))
        assert(query_request[1] in self.position_dict.keys())
        if query_request[0] == "hp":
            return self.position_dict[query_request[1]].get_hp()
    
    def board_command(self, command):
        assert(isinstance(command, tuple))
        assert(len(command) == 3)
        assert(isinstance(command[0], str))
        assert(isinstance(command[1], tuple))
        assert(isinstance(command[1][0], int))
        assert(isinstance(command[1][1], int))
        assert(isinstance(command[2], tuple))
        assert(isinstance(command[2][0], int))
        assert(isinstance(command[2][1], int))
        assert(command[1] in self.position_dict.keys())
        if command[0] == "move":
            assert(command[2] not in self.position_dict.keys())
            entity = self.position_dict.pop(command[1])
            entity.position = command[2]
            self.position_dict[command[2]] = entity

class game:
    def get_xy_input():
        temp_input = input()
        return temp_input.split(" ")[0], int(temp_input.split(" ")[1]), int(temp_input.split(" ")[2])


def test(x : int) -> str:
    return str(x)+"1"

def main():
    board = Board(size=9)
    board.place_entity(Playable_Character(character="1", hp=5, position=(1, 3)))
    board.place_entity(Playable_Character(character="2", hp=7, position=(4, 5)))
    board.place_entity(Enemy(character="9", hp=3))
    board.place_entity(Enemy(character="8", hp=2, position=(8, 8)))
    board.print_board()
    print(board.get_info(("hp", (8, 8))))
    board.board_command(("move", (1, 3), (4, 6)))
    board.print_board()


main()
