namespace Game{
    public abstract class Item{
        public string name { get; private set; }

        public Item(string name){
            this.name = name;
        }

        public override string ToString(){
            return name;
        }
    }

    public sealed class Weapon : Item{
        public int damage {get; private set;}
        public int range {get; private set;}

        public Weapon() : this("Fists", 1, 1) { }

        public Weapon(string name, int damage, int range) : base(name){
            this.damage = damage;
            this.range = range;
        }

        public override string ToString(){
            return $"weapon: {{ {base.ToString()}, damage: {damage}, range: {range} }}";
        }
    }

    public sealed class Armor : Item{
        public int rating {get; private set;}

        public Armor() : this ("Naked", 0) { }

        public Armor(string name, int rating): base(name){
            this.rating = rating;
        }

        public override string ToString()
        {
            return $"armor: {{ {base.ToString()}, armor rating: {rating} }}";
        }
    }
}