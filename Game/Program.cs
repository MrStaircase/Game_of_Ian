namespace Game{
    public class Program{
        public static void Main(string[] args){
            var ally_1 = new Ally(10, 'P');
            Console.Out.WriteLine(ally_1.hp);
            var item_1 = new Weapon("sword", 1, 1);
            Console.Out.WriteLine(item_1.name);
            Command_Handler.parse_command(["greet"]);
        }
    }
}