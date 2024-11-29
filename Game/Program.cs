namespace Game{
    public class Program{
        private static Board board {get;} = new(9);
        private static Game_Inventory game_inventory {get;} = new();

        public static void run_std_input(){
            string? command;
            while((command = Console.In.ReadLine()) != null){
                try{
                    Command_Handler.parse_command(board, game_inventory, command.Split(" "));
                }
                catch(Exception e){
                    Console.Out.WriteLine($"{e.Message} <{command}>");
                }
            }
        }

        public static void run_file(string file_name){
            using StreamReader reader = new(file_name);
            string? command;
            while ((command = reader.ReadLine()) != null){
                try{
                    Command_Handler.parse_command(board, game_inventory, command.Split(" "));
                }
                catch (Exception e){
                    Console.Out.WriteLine($"{e.Message} <{command}>");
                }
            }
        }

        public static void Main(string[] args){
            if(args.Length == 0){
                run_std_input();
            }
            else if(args.Length == 1){
                run_file(args[0]);
            }
        }
    }
}