namespace Game{
    public abstract class Entity{
        public char character { get; private set; }
        public int hp { get; private set; }

        public abstract int armor {get;}

        public Entity(char character, int hp){
            this.character = character;
            this.hp = hp;
        }

        public override string ToString(){
            return $"{character}, hp: {hp}";
        }
        
        public void deal_damage(int raw_damage, int armor_pen){
            int final_damage = Math.Max(raw_damage - (armor - armor_pen), 0) + armor_pen;
            hp = Math.Max(hp - final_damage, 0);
        }

        public abstract void attack(Entity target, int distance);
    }

    public sealed class Enemy : Entity{
        public int damage {get; private set;}
        private int _armor {get; set;}
        public override int armor {get => _armor;}

        public Enemy(char character, int hp, int damage, int armor) : base(character, hp){
            this.damage = damage;
            this._armor = armor;
        }

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

    public sealed class Ally : Entity{
        public override int armor {get => selected_armor.rating;}
        public string role {get; private set;} = "fighter";
        public List<Item> items {get; private set;} = new(){ new Weapon(), new Armor() };
        public Weapon selected_weapon {get; private set;} = new Weapon();
        public Armor selected_armor {get; private set;} = new Armor();

        public Ally(char character, int hp) : base(character, hp) { }

        public override string ToString(){
            return $"ally: {base.ToString()}, selected {selected_weapon}, selected {selected_armor}";
        }

        public void add_item(Item item){
            items.Add(item);
        }

        public void equip_item(int index){
            if(index >= items.Count || index < 0){
                throw new IndexOutOfRangeException($"item chosen ({index}) out of range ({items.Count})");
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