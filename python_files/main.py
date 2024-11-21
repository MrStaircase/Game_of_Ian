class Entity:
    def __init__(self, character: str = " ", hp: int = 0):
        self.hp: int = hp
        self.character: str = character

    def __str__(self) -> str:
        return self.character + ", hp: " + str(self.hp)
    
    def get_hp(self) -> int:
        return self.hp

    def gain_damage(self, damage: int) -> None:
        assert damage >= 0, "Cannot receive negative damage"
        self.hp = max(self.hp - damage, 0)
    
    def attack(self, target, damage: int) -> None:
        assert isinstance(target, Entity), "Target must be an entity"
        target.gain_damage(damage)

class Enemy(Entity):
    def __init__(self, character= "E", hp = 0):
        super().__init__(character=character, hp=hp)
    
    def __str__(self) -> str:
        return "enemy: " + super().__str__()

class Playable_Character(Entity):
    def __init__(self, character= "P", hp = 0, role = "fighter"):
        super().__init__(character=character, hp=hp)
        self.role: str = role

    def __str__(self) -> str:
        return "playable_character: " + super().__str__()

class Item:
    def __init__(self, name = "item"):
        self.name: str = name

class Weapon(Item):
    def __init__(self, name="item", damage = 0, range = 0):
        assert(range >= 0)
        super().__init__(name)
        self.damage: int = damage
        self.range: int = range

class Board:
    def __init__(self, size:int  = 9):
        assert size > 0, "Board must be of a positive size"
        self.size: int = size
        self.position_dict: dict[tuple[int, int], Entity] = {}

    def print_board(self) -> None:
        output: str = ""
        for i in range(self.size):
            for j in range(self.size):
                output += self.position_dict[(i, j)].character + " | " if (i, j) in self.position_dict.keys() else "  | "
            output = output[:-2] + "\n- + - + - + - + - + - + - + - + -\n"
        output = output[:-(self.size*4)]
        print(output)
    
    def get_info(self, position: tuple[int, int]) -> str:
        if position in self.position_dict.keys():
            return self.position_dict[position]
        else:
            return "empty space"
    
    def move_entity(self, from_position: tuple[int, int], to_position: tuple[int, int]) -> None:
        assert from_position in self.position_dict.keys(), "Cannot move from an empty space"
        assert to_position not in self.position_dict.keys(), "Cannot move to a non-empty space"
        self.position_dict[to_position] = self.position_dict.pop(from_position)
        
    def place_entity(self, entity: Entity, position: tuple[int, int]) -> None:
        assert(position not in self.position_dict.keys()), "Cannot place entity on a non-empty space"
        self.position_dict[position] = entity

class Command_Parser:
    def move_command(board: Board, command_arguments: list[str]) -> None:
        assert len(command_arguments) == 4, f"move command expected 4 arguments ({len(command_arguments)} were given)"
        from_position: tuple[int, int] = (int(command_arguments[0]), int(command_arguments[1]))
        to_position: tuple[int, int] = (int(command_arguments[2]), int(command_arguments[3]))
        board.move_entity(from_position, to_position)
        board.print_board()

    def place_command(board: Board, command_arguments: list[str]) -> None:
        assert len(command_arguments) == 5, f"place command expected 5 arguments ({len(command_arguments)} were given)"
        entity_type: str = command_arguments[0]
        entity_character: str = command_arguments[1]
        entity_hp: int = int(command_arguments[2])
        position: tuple[int, int] = (int(command_arguments[3]), int(command_arguments[4]))
        entity: Entity
        if entity_type == "player":
            entity = Playable_Character(entity_character, entity_hp)
        elif entity_type == "enemy":
            entity = Enemy(entity_character, entity_hp)
        else:
            assert False, "unknowned place entity type"
        board.place_entity(entity, position)
        board.print_board()

    def info_command(board: Board, command_arguments: list[str]) -> None:
        assert len(command_arguments) == 2, f"hp command expected 2 arguments ({len(command_arguments)} were given)"
        position: tuple[int, int] = (int(command_arguments[0]), int(command_arguments[1]))    
        print(board.get_info(position))

    def pass_command(board: Board, command: str) -> None:
        if command == "":
            return
        command_arguments: list[str] = [item for item in command.split(" ") if item != ""]
        command_type: str = command_arguments[0].lower()
        if command_type == "move":
            Command_Parser.move_command(board, command_arguments[1:])
        elif command_type == "place":
            Command_Parser.place_command(board, command_arguments[1:])
        elif command_type == "?":
            Command_Parser.info_command(board, command_arguments[1:])
        else:
            assert False, "unknowned command"

def main():
    board: Board = Board(size=9)
    board.print_board()
    input_str: str = ""
    while input_str != "stop":
        try:
            Command_Parser.pass_command(board, input_str)
        except AssertionError as e:
            print(e)
        input_str = input()

main()
