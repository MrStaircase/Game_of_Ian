namespace Game{
    public abstract class Item(string name){
        public string name { get; private set; } = name;

        public override string ToString(){
            return "";
        }
    }

    public sealed class Weapon(string name, int damage, int range) : Item(name){
        public int damage {get; private set;} = damage;
        public int range {get; private set;} = range;

        public Weapon() : this("Fists", 1, 1) { }

        public override string ToString(){
            return "";
        }
    }

    public sealed class Armor(string name, int rating) : Item(name){
        public int rating {get; private set;} = rating;

        public Armor() : this ("Naked", 0) { }
    }
}