namespace Game{
    public abstract class Entity(int hp, char character){
        public int hp { get; private set; } = hp;
        public char character { get; private set; } = character;

        public override string ToString(){
            return "";
        }
        
        public void deal_damage(int raw_damage, int armor_pen){
            hp = 0;
        }

        public abstract void attack(Entity target, int distance);
    }

    public sealed class Ally(int hp, char character) : Entity(hp, character) {
        public string role {get; private set;} = "fighter";
        public List<Item> items {get; private set;} = [new Weapon(), new Armor()];
        public Weapon selected_weapon {get; private set;} = new Weapon();
        public Armor selected_armor {get; private set;} = new Armor();

        public override string ToString(){
            return "";
        }

        public void add_item(Item item){
            items.Add(item);
        }

        public void equip_item(int index){
            if(index >= items.Count || index < items.Count){
                throw new IndexOutOfRangeException("item chosen out of range");
            }
            else if(items[index] is Weapon weapon){
                selected_weapon = weapon;
            }
            else if(items[index] is Armor armor){
                selected_armor = armor;
            }
        }

        public override void attack(Entity target, int distance){

        }

        public int get_armor(){
            return 0;
        }
    }

    public sealed class Enemy(int hp, char character, int damage, int armor) : Entity (hp, character){
        public int damage {get; private set;} = damage;
        public int armor {get; private set;} = armor;

        public override string ToString(){
            return "";
        }
        public override void attack(Entity target, int distance){

        }
    }
}