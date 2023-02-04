import java.util.ArrayList;
public class example_3 {

    public static void main(String[] args) {
        ArrayList pitches = new ArrayList();
        pitches.add("홍길동");
        pitches.add("김철수");
        pitches.add("이철수");

        System.out.println(pitches.contains("홍길동"));
        System.out.println(pitches.contains("홍철수"));

}

}
