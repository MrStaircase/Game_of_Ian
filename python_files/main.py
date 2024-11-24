import sys

def distance(from_position: tuple[int, int], to_position: tuple[int, int]) -> int:
    return abs(from_position[0] - to_position[0]) + abs(from_position[1] - to_position[1])

class Entity:
    def __init__(self, character: str = " ", hp: int = 0):
        self.hp: int = hp
        self.character: str = character

    def __str__(self) -> str:
        return self.character + ", hp: " + str(self.hp)
    
    def get_hp(self) -> int:
        return self.hp

    def deal_damage(self, raw_damage: int, armor_pen: int = 0) -> None:
        assert raw_damage >= 0, "Cannot receive negative damage"
        final_damage: int = max(raw_damage - (self.get_armor() - armor_pen), 0) + armor_pen
        self.hp = max(self.hp - final_damage, 0)
    
    def attack(self, target: "Entity", distance: int) -> None:
        pass

    def get_armor(self) -> int:
        pass

class Enemy(Entity):
    def __init__(self, character:str = "E", hp: int = 0, damage: int = 1, armor: int = 0):
        super().__init__(character=character, hp=hp)
        self.damage: int = damage
        self.armor: int = armor
    
    def __str__(self) -> str:
        return f"enemy: {super().__str__()}, damage: {self.damage}, armor: {self.armor}"
    
    def attack(self, target: Entity, distance: int) -> None:
        assert isinstance(target, Entity), "Target must be an entity"
        target.deal_damage(self.damage)
    
    def get_armor(self) -> int:
        return self.armor

class Playable_Character(Entity):
    def __init__(self, character: str = "P", hp: int = 0, role: str = "fighter"):
        super().__init__(character=character, hp=hp)
        self.role: str = role
        self.items: list[Item] = []
        self.selected_weapon: Weapon = Weapon()
        self.selected_armor: Armor = Armor()

    def __str__(self) -> str:
        return f"playable_character: {super().__str__()}, selected {self.selected_weapon}, selected {self.selected_armor}"
    
    def add_item(self, item: "Item") -> None:
        self.items.append(item)

    def get_items(self) -> list["Item"]:
        return [str(item) for item in self.items]

    def select_weapon(self, weapon: "Weapon") -> None:
        self.selected_weapon = weapon

    def select_armor(self, armor: "Armor") -> None:
        self.selected_armor = armor

    def equip_item(self, index: int) -> None:
        assert -1 <= index < len(self.items), f"Must select an item index within the range {-1} and {len(self.items) - 1}"
        if index == -1:
            self.select_weapon(Weapon())
            self.select_armor(Armor())
            return
        item: Item = self.items[index]
        if isinstance(item, Weapon):
            self.select_weapon(item)
        elif isinstance(item, Armor):
            self.select_armor(item)

    def attack(self, target: Entity, distance: int) -> None:
        assert isinstance(target, Entity), "Target must be an entity"
        range: int
        damage: int
        damage, range = self.selected_weapon.get_stats()
        assert distance <= range, "Target out of range"
        target.deal_damage(damage)

    def get_armor(self) -> int:
        return self.selected_armor.get_stats()

class Item:
    def __init__(self, name = "item"):
        self.name: str = name

    def __str__(self) -> str:
        return self.name

class Weapon(Item):
    def __init__(self, name="none", damage = 1, range = 1):
        assert range >= 0, "Weapons range must be non-negative"
        super().__init__(name)
        self.damage: int = damage
        self.range: int = range
    
    def __str__(self):
        return f"weapon: {{{super().__str__()}, damage: {self.damage}, range: {self.range}}}"

    def get_stats(self) -> tuple[int, int]:
        return self.damage, self.range

class Armor(Item):
    def __init__(self, name="none", armor_rating = 0):
        super().__init__(name)
        self.armor_rating: int = armor_rating
    
    def __str__(self) -> str:
        return f"armor: {{{super().__str__()}, armor rating: {self.armor_rating}}}"

    def get_stats(self) -> int:
        return self.armor_rating

class Board:
    def __init__(self, size:int  = 9):
        assert size > 0, "Board must be of a positive size"
        self.size: int = size
        self.position_dict: dict[tuple[int, int], Entity] = {}

    def print_board(self) -> None:
        output: list[str] = []
        row_separator: str = " ".join((["-", "+"] * self.size)[:-1])
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i, j) in self.position_dict:
                    row.append(self.position_dict[(i, j)].character)
                else:
                    row.append(" ")
                row.append("|")
            output.append(" ".join(row[:-1]))
            output.append(row_separator)
        print("\n".join(output[:-1]))
    
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

    def attack(self, attacker_position: tuple[int, int], target_position: tuple[int, int]) -> None:
        assert(attacker_position in self.position_dict.keys()), "Attacker position must contain an entity"
        assert(target_position in self.position_dict.keys()), "Target position must contain an entity"
        self.position_dict[attacker_position].attack(self.position_dict[target_position], distance(attacker_position, target_position))

class Board_Command_Parser:
    def move_command(board: Board, command_arguments: list[str]) -> None:
        assert len(command_arguments) == 4 or len(command_arguments) == 0,\
            f"move command expected 0 or 4 arguments ({len(command_arguments)} were given)"
        from_position: tuple[int, int] = (0, 0)
        to_position: tuple[int, int] = (0, 0)
        if len(command_arguments) == 0:
            from_position = Input_Arguemnts.get_position("Please enter the position to move from:")
            to_position = Input_Arguemnts.get_position("Please enter the position to move to:")
        if len(command_arguments) == 4:
            from_position = (int(command_arguments[0]), int(command_arguments[1]))
            to_position = (int(command_arguments[2]), int(command_arguments[3]))
        board.move_entity(from_position, to_position)

    def place_command(board: Board, command_arguments: list[str]) -> None:
        assert len(command_arguments) == 3 or len(command_arguments) == 0,\
            f"place command expected 0 or 3 arguments ({len(command_arguments)} were given)"
        entity_id: int = 0
        position: tuple[int, int] = (0, 0)
        if len(command_arguments) == 0:
            entity_id = Input_Arguemnts.get_int("Please enter the entity id to place:")
            position = Input_Arguemnts.get_position("Please enter the position to place in:")
        if len(command_arguments) == 3:
            entity_id = int(command_arguments[0])
            position = (int(command_arguments[1]), int(command_arguments[2]))
        board.place_entity(Game_Inventory.get_entity(entity_id), position)

    def info_command(board: Board, command_arguments: list[str]) -> None:
        assert len(command_arguments) == 2 or len(command_arguments) == 0,\
            f"? command expected 0 or 2 arguments ({len(command_arguments)} were given)"
        position: tuple[int, int] = (0, 0)
        if len(command_arguments) == 0:
            position = Input_Arguemnts.get_position("Please enter the position for which you want the information:")
        if len(command_arguments) == 2:
            position = (int(command_arguments[0]), int(command_arguments[1]))    
        print(board.get_info(position))

    def attack_command(board: Board, command_arguments: list[str]) -> None:
        assert len(command_arguments) == 4 or len(command_arguments) == 0,\
              f"attack command expected 0 or 4 arguments ({len(command_arguments)} were given)"
        attacker_position: tuple[int, int] = (0, 0)
        target_position: tuple[int, int] = (0, 0)
        if len(command_arguments) == 0:
            attacker_position = Input_Arguemnts.get_position("Please enter the position from which to attack:")
            target_position = Input_Arguemnts.get_position("Please enter the position to which to attack:")
        if len(command_arguments) == 4:
            attacker_position = (int(command_arguments[0]), int(command_arguments[1]))
            target_position = (int(command_arguments[2]), int(command_arguments[3]))
        board.attack(attacker_position, target_position)

    def print_command(board: Board, command_arguments: list[str]) -> None:
        board.print_board()

class Game_Inventory:
    entities: dict[int, Entity] = {}
    items: dict[int, Item] = {}
    
    def add_entity(entity: Entity) -> None:
        assert entity not in Game_Inventory.entities.values(), "Cannot add entity that already exist"
        Game_Inventory.entities[len(Game_Inventory.entities)] = entity

    def add_item(item: Item) -> None:
        assert item not in Game_Inventory.items.values(), "Cannot add item that already exist"
        Game_Inventory.items[len(Game_Inventory.items)] = item

    def get_entity(id: int) -> Entity:
        assert id in Game_Inventory.entities.keys(), "Entity id not found"
        return Game_Inventory.entities[id]
    
    def get_item(id: int) -> Item:
        assert id in Game_Inventory.items.keys(), "Item id not found"
        return Game_Inventory.items[id]

    def get(type:str, id:int) -> Item | Entity:
        if type.lower() == "entity": return Game_Inventory.get_entity(id)
        if type.lower() == "item": return Game_Inventory.get_item(id)

    def print_all_entities() -> None:
        print("Entities:")
        for id, entity in Game_Inventory.entities.items():
            print(f"\tEntity \"{id}\": {{{entity}}}")

    def print_all_items() -> None:
        print("Items:")
        for id, item in Game_Inventory.items.items():
            print(f"\tEntity \"{id}\": {{{item}}}")

    def print_all() -> None:
        Game_Inventory.print_all_entities()
        Game_Inventory.print_all_items()

class Game_Command_Parser:
    def create_command_slow() -> None:
        pass

    def create_command(command_arguments: list[str]) -> None:
        assert len(command_arguments) > 0, f"create command expected at least 1 argument ({len(command_arguments)} were given)"
        create_type: str = command_arguments[0].lower().strip()
        if create_type == "entity":
            assert len(command_arguments) == 4, f"create entity command expected 4 arguments ({len(command_arguments)} were given)"
            entity_type: str = command_arguments[1].lower().strip()
            entity_character: str = command_arguments[2]
            entity_hp: int = int(command_arguments[3])
            entity: Entity
            if entity_type == "player":
                entity = Playable_Character(entity_character, entity_hp)
            elif entity_type == "enemy":
                entity = Enemy(entity_character, entity_hp)
            Game_Inventory.add_entity(entity)
        elif create_type == "item":
            assert len(command_arguments) > 1, f"create item command expected at least 2 arguments ({len(command_arguments)} were given)"
            item_type: str = command_arguments[1].lower().strip()
            item: Item
            if item_type == "weapon":
                assert len(command_arguments) == 5, f"create item weapon command expected 5 arguments ({len(command_arguments)} were given)"
                item_name: str = command_arguments[2]
                item_damage: int = int(command_arguments[3])
                item_range: int = int(command_arguments[4])
                item = Weapon(item_name, item_damage, item_range)
            elif item_type == "armor":
                assert len(command_arguments) == 4, f"create item armor command expected 4 arguments ({len(command_arguments)} were given)"
                item_name: str = command_arguments[2]
                armor_rating: int = int(command_arguments[3])
                item = Armor(item_name, armor_rating)
            Game_Inventory.add_item(item)
        else:
            assert False, "create command: unknown create type"

    def entities_command(command_arguments: list[str]) -> None:
        assert len(command_arguments) == 0, f"entities command expected 0 arguments ({len(command_arguments)} were given)"
        Game_Inventory.print_all_entities()

    def items_command(command_arguments: list[str]) -> None:
        assert len(command_arguments) == 1 or len(command_arguments) == 0,\
              f"items command expected 0 or 1 arguments ({len(command_arguments)} were given)"
        if len(command_arguments) == 0:
            return Game_Inventory.print_all_items()
        entity_id: int = 0
        if len(command_arguments) == 0:
            entity_id = Input_Arguemnts.get_int("Please enter the entity id to which toy want to print the items:")
        if len(command_arguments) == 1:
            entity_id = int(command_arguments[0])
        entity: Entity = Game_Inventory.get_entity(entity_id)
        assert isinstance(entity, Playable_Character), "item command must select a playable character"
        print(entity.get_items())

    def give_command(command_arguments: list[str]) -> None:
        assert len(command_arguments) == 2 or len(command_arguments) == 0, f"give command expected 0 or 2 arguments ({len(command_arguments)} were given)"
        entity_id: int = 0
        item_id: Item = None
        if len(command_arguments) == 0:
            entity_id = Input_Arguemnts.get_int("Please enter the entity id to which you give the item:")
            item_id = Input_Arguemnts.get_int("Please enter the item id which you want to give:")
        if len(command_arguments) == 2:
            entity_id = int(command_arguments[0])
            item_id = int(command_arguments[1])
        entity: Entity = Game_Inventory.get_entity(entity_id)
        assert isinstance(entity, Playable_Character), "give command must select a playable character"
        item: Item = Game_Inventory.get_item(item_id)
        entity.add_item(item)

    def equip_command(command_arguments: list[str]) -> None:
        assert len(command_arguments) == 2 or len(command_arguments) == 0, f"equip command expected 0 or 2 arguments ({len(command_arguments)} were given)"
        entity_id: int = 0
        item_index: int = 0
        if len(command_arguments) == 0:
            entity_id = Input_Arguemnts.get_int("Please enter the entity id to equip:")
            item_index = Input_Arguemnts.get_int("Please enter the item index to equip:")
        if len(command_arguments) == 2:
            entity_id = int(command_arguments[0])
            item_index: int = int(command_arguments[1])
        entity: Entity = Game_Inventory.get_entity(entity_id)
        assert isinstance(entity, Playable_Character), "equip command must select a playable character"
        entity.equip_item(item_index)

class Command_Parser:
    def help_command(command_arguments: list[str]) -> None:
        print("""Available Commands:
              \tattack from_position_x from_position_y to_position_x to_position_x
              \t? position_x position_y
              \tmove from_position_x from_position_y to_position_x to_position_y
              \tplace entity_id position_x position_y
              \tcreate entity type character hp
              \tcreate item type name
              \tentities
              \titems [entity_id]
              \tgive entity_id item_id
              \tequip entity_id item_index
              \tprint
              \thelp""")

    def pass_command(board: Board, command: str) -> None:
        if command.strip() == "":
            return
        command_arguments: list[str] = [item for item in command.split(" ") if item != ""]
        command_type: str = command_arguments[0].lower().strip()
        if command_type == "help":
            Command_Parser.help_command(command_arguments[1:])
        elif command_type == "move":
            Board_Command_Parser.move_command(board, command_arguments[1:])
        elif command_type == "place":
            Board_Command_Parser.place_command(board, command_arguments[1:])
        elif command_type == "?":
            Board_Command_Parser.info_command(board, command_arguments[1:])
        elif command_type == "attack":
            Board_Command_Parser.attack_command(board, command_arguments[1:])
        elif command_type == "print":
            Board_Command_Parser.print_command(board, command_arguments[1:])
        elif command_type == "create":
            Game_Command_Parser.create_command(command_arguments[1:])
        elif command_type == "entities":
            Game_Command_Parser.entities_command(command_arguments[1:])
        elif command_type == "items":
            Game_Command_Parser.items_command(command_arguments[1:])
        elif command_type == "give":
            Game_Command_Parser.give_command(command_arguments[1:])
        elif command_type == "equip":
            Game_Command_Parser.equip_command(command_arguments[1:])
        else:
            assert False, f"unknowned command: {command_type}"

class Input_Arguemnts:
    def get_int(message: str) -> int:
        print(message)
        return int(input())
    def get_position(message: str) -> tuple[int, int]:
        print(message)
        input_str: str = input().lower()
        return (int(input_str[0]), int(input_str[1]))
    def get_string(message: str) -> str:
        print(message)
        return input()
    def get_boolean(message: str) -> bool:
        print(message)
        input_str: str = input().lower()
        return bool(input_str == "yes" or input_str == "y")

def run_file(filename: str):
    board: Board = Board(size=9)
    with open(filename, "r") as file:
        for line in file:
            try:
                Command_Parser.pass_command(board, line)
            except AssertionError as e:
                print(e)

def run_std_in():
    board: Board = Board(size=9)
    board.print_board()
    input_str: str = ""
    while input_str != "stop":
        try:
            Command_Parser.pass_command(board, input_str)
        except AssertionError as e:
            print(e)
        input_str = input()

def main():
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    elif len(sys.argv) == 1:
        run_std_in()
    else:
        print(f"expected 1 or 2 arguements ({len(sys.argv)} were given)")

main()
