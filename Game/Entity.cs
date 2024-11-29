namespace Game{
    public abstract class Entity(char character, int hp){
        public char character { get; private set; } = character;
        public int hp { get; private set; } = hp;

        public abstract int armor {get;}

        public override string ToString(){
            return $"{character}, hp: {hp}";
        }
        
        public void deal_damage(int raw_damage, int armor_pen){
            int final_damage = Math.Max(raw_damage - (armor - armor_pen), 0) + armor_pen;
            hp = Math.Max(hp - final_damage, 0);
        }

        public abstract void attack(Entity target, int distance);
    }

    public sealed class Enemy(char character, int hp, int damage, int armor) : Entity (character, hp){
        public int damage {get; private set;} = damage;
        private int _armor {get; set;} = armor;
        public override int armor {get => _armor;}

        public override string ToString(){
            return $"enemy: {base.ToString()}, damage: {damage}, armor: {armor}";
        }
        public override void attack(Entity target, int distance){
            if(distance <= 1){
                target.deal_damage(damage, 0);
            }
            else{
                throw new ArgumentException($"enemy cannot reach target with current weapon");
            }
        }
    }

    public sealed class Ally(char character, int hp) : Entity(character, hp) {
        public override int armor {get => selected_armor.rating;}
        public string role {get; private set;} = "fighter";
        public List<Item> items {get; private set;} = [new Weapon(), new Armor()];
        public Weapon selected_weapon {get; private set;} = new Weapon();
        public Armor selected_armor {get; private set;} = new Armor();

        public override string ToString(){
            return $"ally: {base.ToString()}, selected {selected_weapon}, selected {selected_armor}";
        }

        public void add_item(Item item){
            items.Add(item);
        }

        public void equip_item(int index){
            if(index >= items.Count || index < 0){
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
            if(distance <= selected_weapon.range){
                target.deal_damage(selected_weapon.damage, 0);
            }
            else{
                throw new ArgumentException($"ally cannot reach target with current weapon");
            }
        }
    }    
}