import java.util.stream.IntStream;

public class Armstrong {
    
    public static boolean isArmstrong(int num) {
        String digits = String.valueOf(num);
        int power = digits.length();
        
        return digits.chars()
            .map(c -> c - '0')
            .map(d -> (int) Math.pow(d, power))
            .sum() == num;
    }
    
    public static void main(String[] args) {
        // Test numbers
        IntStream.of(153, 1253, 371, 9474, 1634)
            .forEach(n -> System.out.printf("%d: %s\n", n, isArmstrong(n)));
        
        // Find all Armstrong numbers up to 10000
        System.out.println("\nArmstrong numbers (1-10000):");
        IntStream.range(1, 10000)
            .filter(Armstrong::isArmstrong)
            .forEach(n -> System.out.print(n + " "));
    }
}
