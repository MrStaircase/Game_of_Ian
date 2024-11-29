namespace Game{
    public static class Command_Handler{
        private delegate void Game_Command(Game_Inventory game_inventory, string[] args);
        private delegate void Board_Command(Board board, string[] args);
        private static Dictionary<string, Game_Command> game_command_dict = new(){
            {"create", Game_Commands.create_command},
            {"entities", Game_Commands.entities_command},
            {"items", Game_Commands.items_command},
            {"give", Game_Commands.give_command},
            {"equip", Game_Commands.equip_command}
        };

        private static Dictionary<string, Board_Command> board_command_dict = new(){
            
        };

        public static void parse_command(Board board, Game_Inventory game_inventory, string[] args){
            if(args.Length == 0) throw new ArgumentException("empty command");
            if(game_command_dict.ContainsKey(args[0].ToLower())){
                game_command_dict[args[0].ToLower()](game_inventory, args.Skip(1).ToArray());
            }
            else if(board_command_dict.ContainsKey(args[0].ToLower())){
                board_command_dict[args[0].ToLower()](board, args.Skip(1).ToArray());
            }
            else throw new ArgumentException($"command unknown: {args[0]}");
        }
    }

    public static class Game_Commands{
        private delegate void Game_Command(Game_Inventory game_inventory, string[] args);
        private static Dictionary<string, Game_Command> game_command_dict = new(){
            {"entity", Create_Commands.create_entity_command},
            {"item", Create_Commands.create_item_command}
        };
        public static void create_command(Game_Inventory game_inventory, string[] args){
            if(args.Length == 0) throw new ArgumentException($"create command: expected at least 1 argument ({args.Length} were given)");
            game_command_dict[args[0].ToLower()](game_inventory, args.Skip(1).ToArray());
        }

        public static void entities_command(Game_Inventory game_inventory, string[] args){
            game_inventory.print_all_entities();
        }

        public static void items_command(Game_Inventory game_inventory, string[] args){
            if(args.Length == 0) game_inventory.print_all_items();
            else if(args.Length == 1) {
                if(!int.TryParse(args[0], out int entity_id)) throw new ArgumentException($"items: entity_id is not an integer ({args[0]})");
                if(game_inventory.entities[entity_id] is Ally ally){
                    Console.Out.WriteLine($"items of {ally.character}:");
                    for (int i = 0; i < ally.items.Count; i++){
                        Console.Out.WriteLine($"\t{i}: {{ {ally.items[i]} }}");   
                    }
                }
                else throw new ArgumentException($"items: entity is not an Ally ({args[0]})");
            }
            else throw new ArgumentException($"items: command expected 0 or 1 arguments ({args.Length} were given)");
        }
        
        public static void give_command(Game_Inventory game_inventory, string[] args){
            if(args.Length != 2) throw new ArgumentException($"give: command expected 2 arguments ({args.Length} were given)");
            if(!int.TryParse(args[0], out int entity_id)) throw new ArgumentException($"give: entity_id is not an integer ({args[0]})");
            if(!int.TryParse(args[1], out int item_id)) throw new ArgumentException($"give: item_id is not an integer ({args[1]})");
            if(game_inventory.entities[entity_id] is Ally ally){
                ally.add_item(game_inventory.items[item_id]);
            }
            else throw new ArgumentException($"give: entity is not an Ally ({args[0]})");
        }
        
        public static void equip_command(Game_Inventory game_inventory, string[] args){
            if(args.Length != 2) throw new ArgumentException($"equip: command expected 2 arguments ({args.Length} were given)");
            if(!int.TryParse(args[0], out int entity_id)) throw new ArgumentException($"equip: entity_id is not an integer ({args[0]})");
            if(!int.TryParse(args[1], out int item_index)) throw new ArgumentException($"equip: item_index is not an integer ({args[1]})");
            if(game_inventory.entities[entity_id] is Ally ally){
                ally.equip_item(item_index);
            }
            else throw new ArgumentException($"equip: entity is not an Ally ({args[0]})");
        }
    }
    //TODO:
    public static class Board_Commands{
        public static void _command(Board board, string[] args){

        }
    }

    public static class Create_Commands{
        private delegate void Create_Command(Game_Inventory game_inventory, string[] args);
        private static Dictionary<string, Create_Command> create_command_dict = new(){
            {"ally", Create_Entity_Commands.create_entity_ally_command},
            {"enemy", Create_Entity_Commands.create_entity_enemy_command},
            {"weapon", Create_Item_Commands.create_item_weapon_command},
            {"armor", Create_Item_Commands.create_item_armor_command}
        };

        public static void create_entity_command(Game_Inventory game_inventory, string[] args){
            if(args.Length == 0) throw new ArgumentException($"create entity command: expected at least 1 argument ({args.Length} were given)");
            create_command_dict[args[0].ToLower()](game_inventory, args.Skip(1).ToArray());
        }

        public static void create_item_command(Game_Inventory game_inventory, string[] args){
            if(args.Length == 0) throw new ArgumentException($"create item command: expected at least 1 argument ({args.Length} were given)");
            create_command_dict[args[0].ToLower()](game_inventory, args.Skip(1).ToArray());
        }
    }

    public static class Create_Entity_Commands{
        public static void create_entity_ally_command(Game_Inventory game_inventory, string[] args){
            if(args.Length != 2) throw new ArgumentException($"create entity ally: command expected 2 arguments ({args.Length} were given)");
            if(!char.TryParse(args[0], out char character)) throw new ArgumentException($"create entity ally: character is not a char ({args[0]})");
            if(!int.TryParse(args[1], out int hp)) throw new ArgumentException($"create entity ally: hp is not an integer ({args[1]})");
            Ally ally = new(character, hp);
            game_inventory.add(ally);
        }

        public static void create_entity_enemy_command(Game_Inventory game_inventory, string[] args){
            if(args.Length != 4) throw new ArgumentException($"create entity enemy: command expected 4 arguments ({args.Length} were given)");
            if(!char.TryParse(args[0], out char character)) throw new ArgumentException($"create entity enemy: character is not a char ({args[0]})");
            if(!int.TryParse(args[1], out int hp)) throw new ArgumentException($"create entity enemy: hp is not an integer ({args[1]})");
            if(!int.TryParse(args[2], out int damage)) throw new ArgumentException($"create entity enemy: damage is not an integer ({args[2]})");
            if(!int.TryParse(args[3], out int armor)) throw new ArgumentException($"create entity enemy: armor is not an integer ({args[3]})");
            Enemy enemy = new(character, hp, damage, armor);
            game_inventory.add(enemy);
        }
    }

    public static class Create_Item_Commands{
        public static void create_item_weapon_command(Game_Inventory game_inventory, string[] args){
            if(args.Length != 3) throw new ArgumentException($"create item weapon: command expected 3 arguments ({args.Length} were given)");
            if(args[0].Length == 0) throw new ArgumentException($"create item weapon: name is longer empty ({args[0]})");
            if(!int.TryParse(args[1], out int damage)) throw new ArgumentException($"create item weapon: damage is not an integer ({args[1]})");
            if(!int.TryParse(args[2], out int range)) throw new ArgumentException($"create item weapon: range is not an integer ({args[2]})");
            Weapon weapon = new(args[0], damage, range);
            game_inventory.add(weapon);
        }

        public static void create_item_armor_command(Game_Inventory game_inventory, string[] args){
            if(args.Length != 2) throw new ArgumentException($"create item armor: command expected 2 arguments ({args.Length} were given)");
            if(args[0].Length == 0) throw new ArgumentException($"create item armor: name is longer empty ({args[0]})");
            if(!int.TryParse(args[1], out int rating)) throw new ArgumentException($"create item armor: rating is not an integer ({args[1]})");
            Armor armor = new(args[0], rating);
            game_inventory.add(armor);
        }
    }
}