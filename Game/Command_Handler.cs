namespace Game{
    public static class Command_Handler{
        private delegate void Command_Action(string[] args);
        private static Dictionary<string, Command_Action> command_dict = new Dictionary<string, Command_Action>(){
            {"greet", greet}
        };

        public static void parse_command(string[] args){
            if(args.Length == 0){
                throw new ArgumentException("0 arguments given. At least one expected");
            }
            command_dict[args[0]](args.Skip(1).ToArray());  
        }

        private static void greet(string[] args){
            Console.Out.WriteLine("test");
        }


    }
}