import java.util.ArrayList;
import java.util.Scanner;

class Expense {
    String category;
    double amount;
    String date;

    Expense(String category, double amount, String date) {
        this.category = category;
        this.amount = amount;
        this.date = date;
    }
}

public class ExpenseTracker {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Expense> expenses = new ArrayList<>();
        int choice;

        do {
            System.out.println("\n💰 Expense Tracker");
            System.out.println("1. Add Expense");
            System.out.println("2. View All Expenses");
            System.out.println("3. Monthly Summary");
            System.out.println("4. Exit");
            System.out.print("Choose an option: ");
            choice = sc.nextInt();
            sc.nextLine(); // consume newline

            switch (choice) {
                case 1:
                    System.out.print("Enter category: ");
                    String category = sc.nextLine();
                    System.out.print("Enter amount: ");
                    double amount = sc.nextDouble();
                    sc.nextLine();
                    System.out.print("Enter date (YYYY-MM-DD): ");
                    String date = sc.nextLine();
                    expenses.add(new Expense(category, amount, date));
                    System.out.println("✅ Expense added successfully!");
                    break;

                case 2:
                    System.out.println("\n📊 All Expenses:");
                    if (expenses.isEmpty()) {
                        System.out.println("No expenses recorded yet.");
                    } else {
                        for (Expense e : expenses) {
                            System.out.println("📅 Date: " + e.date + " | 🏷️ Category: " + e.category + " | 💸 Amount: ₹" + e.amount);
                        }
                    }
                    break;

                case 3:
                    double total = 0;
                    for (Expense e : expenses) {
                        total += e.amount;
                    }
                    System.out.println("\n📆 Total Monthly Expenses: ₹" + total);
                    break;

                case 4:
                    System.out.println("👋 Exiting... Thank you for using Expense Tracker!");
                    break;

                default:
                    System.out.println("❌ Invalid choice! Please try again.");
            }
        } while (choice != 4);

        sc.close();
    }
}
