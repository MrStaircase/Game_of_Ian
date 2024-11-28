namespace Game{
    public class Vector2(int x, int y): IComparable{
        public int x {get; private set;} = x;
        public int y {get; private set;} = y;

        public int CompareTo(object? other){
            if(other == null)
                return 1;
            if (other is not Vector2 other_vector)
                throw new ArgumentException("Object is not a Vector2");
            if (x.CompareTo(other_vector.x) == 0)
                return y.CompareTo(other_vector.y);
            return x.CompareTo(other_vector.x);
        }

        public static int operator -(Vector2 vector_from, Vector2 vector_to){
            return Math.Abs(vector_from.x - vector_to.x) + Math.Abs(vector_from.y - vector_to.y);
        }
    }

    public class Board(int size){
        public int size {get;} = size;
        public Dictionary<Vector2, Entity> position_dict {get;} = [];

        public void print_board(){

        }

        public void move_entity(Vector2 from_positon, Vector2 to_position){
            position_dict.Add(to_position, position_dict[from_positon]);
            position_dict.Remove(from_positon);
        }

        public void place_entity(Entity entity, Vector2 position){
            position_dict.Add(position, entity);
        }

        public void attack(Vector2 attacker_position, Vector2 target_position){
            position_dict[attacker_position].attack(position_dict[target_position], attacker_position - target_position);
        }
    }

    public class Game_Inventory(){
        public Dictionary<int, Entity> entities {get; private set;} = [];
        public Dictionary<int, Item> items {get; private set;} = [];

        public void add(object obj){
            if(obj is Entity entity)
                entities.Add(entities.Count, entity);
            else if(obj is Item item)
                items.Add(items.Count, item);
            else
                throw new ArgumentException("Object is not an Entity nor Item");
        }

        public void print_all_entities(TextWriter? writer = null){
            if(writer == null)
                writer = Console.Out;
            foreach (Entity entity in entities.Values){
                writer.WriteLine(entity.ToString());
            }
        }

        public void print_all_items(TextWriter? writer = null){
            if(writer == null)
                writer = Console.Out;
            foreach (Item item in items.Values){
                writer.WriteLine(item.ToString());
            }
        }

        public void print_all(TextWriter writer){
            print_all_entities(writer);
            print_all_items(writer);
        }
    }
}