public class NumberReverser {

    public static int reverseNumber(int number) {
        int reversed = 0; // Initialize a variable to store the reversed number

        // Loop until the original number becomes 0
        while (number != 0) {
            int digit = number % 10; // Get the last digit of the number
            reversed = reversed * 10 + digit; // Append the digit to the reversed number
            number /= 10; // Remove the last digit from the original number
        }
        return reversed; // Return the reversed number
    }

    public static void main(String[] args) {
        int originalNumber = 12345; // Example number
        int reversedNumber = reverseNumber(originalNumber); // Call the reverseNumber method

        System.out.println("Original Number: " + originalNumber);
        System.out.println("Reversed Number: " + reversedNumber); // Print the reversed number
    }
}
