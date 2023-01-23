public class operator {
    public static void main(String[] args){
        int x = 20;
        int y = 30;
        boolean bool = x < y || (x = x + 15) > y;
        System.out.println("bool = " + bool);
        System.out.println("x = " + x);
    }
}
