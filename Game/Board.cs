namespace Game{
    public class Vector2 : IComparable, IEquatable<Vector2> {
        public int x { get; private set; }
        public int y { get; private set; }

        public Vector2(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public int CompareTo(object? other) {
            if (other == null)
                return 1;
            if (other is not Vector2 other_vector)
                throw new ArgumentException("Object is not a Vector2");

            int xComparison = x.CompareTo(other_vector.x);
            return xComparison == 0 ? y.CompareTo(other_vector.y) : xComparison;
        }

        public override bool Equals(object? obj) {
            if (obj is Vector2 other)
                return Equals(other);
            return false;
        }

        public bool Equals(Vector2? other) {
            if (other is null)
                return false;
            return x == other.x && y == other.y;
        }

        public override int GetHashCode() {
            return HashCode.Combine(x, y);
        }

        public static int operator -(Vector2 vector_from, Vector2 vector_to) {
            return Math.Abs(vector_from.x - vector_to.x) + Math.Abs(vector_from.y - vector_to.y);
        }

        public static bool operator ==(Vector2 left, Vector2 right) {
            return left?.Equals(right) ?? right is null;
        }

        public static bool operator !=(Vector2 left, Vector2 right) {
            return !(left == right);
        }
    }

    public class Board(int size){
        public int size {get;} = size;
        public Dictionary<Vector2, Entity> position_dict {get;} = [];

        public void print_board(){
            string row_separator = "-";
            for (int i = 1; i < size; i++){
                row_separator += " + -";
            }
            string output = "";
            for (int i = 0; i < size; i++){
                string row = "";
                for (int j = 0; j < size; j++){
                    if(j != 0){
                        row += " ";
                    }
                    Vector2 position = new(i, j);
                    if(position_dict.ContainsKey(position)){
                        row += position_dict[position].character;
                    }
                    else{
                        row += " ";
                    }
                    if(j != size - 1){
                        row += " |";
                    }
                }
                if(i != 0){
                    output += row_separator + "\n";
                }
                output += row + "\n";
            }
            Console.Out.Write(output);
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
            writer.WriteLine("entities:");
            foreach (KeyValuePair<int, Entity> entry in entities.ToArray()){
                writer.WriteLine($"\t{entry.Key}: {{ {entry.Value} }}");
            }
        }

        public void print_all_items(TextWriter? writer = null){
            if(writer == null)
                writer = Console.Out;
            writer.WriteLine("items:");
            foreach (KeyValuePair<int, Item> entry in items.ToArray()){
                writer.WriteLine($"\t{entry.Key}: {{ {entry.Value} }}");
            }
        }

        public void print_all(TextWriter writer){
            print_all_entities(writer);
            print_all_items(writer);
        }
    }
}