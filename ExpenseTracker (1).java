package miniproject;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Scanner;

class Expense {
    private LocalDate date;
    private String description;
    private double amount;
    private LocalTime time;

    public Expense(LocalDate date, LocalTime time, String description, double amount) {
        this.date = date;
        this.time = time;
        this.description = description;
        this.amount = amount;
    }

    public LocalTime getTime() {
        return time;
    }

    public LocalDate getDate() {
        return date;
    }

    public String getDescription() {
        return description;
    }

    public double getAmount() {
        return amount;
    }
}

public class ExpenseTracker {
    ArrayList<Expense> expenses = new ArrayList<>();
    double totalExpenses = 0.0;
    double monthlySavings = 0.0;
    double yearlySavings = 0.0;
    static double monthlyIncome = 0.0;
    static double yearlyIncome = 0.0;

    public void setMonthlyIncome(double monthlyIncome) {
        this.monthlyIncome = monthlyIncome;
        yearlyIncome = monthlyIncome * 12;
        updateSavings();
        System.out.println("Monthly Income set successfully.");
    }

    double minimumExpense = 100.0; // Default minimum Expense

    public void setMinimumExpense(double minimumExpense) {
        this.minimumExpense = minimumExpense;
        System.out.println("Minimum balance set to: " + minimumExpense);
    }

    public void addExpense(String description, double amount) {
        LocalTime currentTime = LocalTime.now();
        LocalDate currentDate = LocalDate.now();
        double newTotalExpenses = totalExpenses + amount;
        double remainingamount = monthlyIncome - newTotalExpenses;
        expenses.add(new Expense(currentDate, currentTime, description, amount));
        totalExpenses = newTotalExpenses;
        updateSavings();
        System.out.println("\nExpense added successfully.\n");
        if (remainingamount < minimumExpense) {
            System.out.println("Adding this expense would go below the minimum balance.");
        }
    }

    public void viewExpenses() {
        System.out.println("\n+----------------------+-------------+----------------+------------+");
        System.out.format("| %-64s |%n", "EXPENSE LIST");
        System.out.println("+----------------------+-------------+----------------+------------+");
        System.out.format("| %-20s | %-11s | %14s | %10s |%n", "DATE", "TIME", "DESCRIPTION", "AMOUNT");
        System.out.println("+----------------------+-------------+----------------+------------+");
        DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm");
        for (Expense expense : expenses) {
            System.out.format("| %-20s | %-11s | %-14s | %10.2f |%n", expense.getDate(), expense.getTime().format(timeFormatter), expense.getDescription(), expense.getAmount());
        }
        System.out.println("+----------------------+-------------+----------------+------------+");
        System.out.format("| %-34s | %27f |%n", "Total Expenses:", totalExpenses);
        System.out.format("| %-34s | %27f |%n", "Total Expenses for the Day:", getTotalExpensesForDay());
        System.out.format("| %-34s | %27f |%n", "Total Expenses for the Week:", getTotalExpensesForWeek());
        System.out.format("| %-34s | %27f |%n", "Total Expenses for the Month:", getTotalExpensesForMonth());
        System.out.println("+----------------------+-------------+----------------+------------+\n");
    }

    public void deleteExpense(String descriptionToDelete) {
        for (Expense expense : expenses) {
            if (expense.getDescription().equalsIgnoreCase(descriptionToDelete)) {
                totalExpenses -= expense.getAmount();
                expenses.remove(expense);
                updateSavings();
                System.out.println("\nExpense deleted successfully.\n");
                return;
            }
        }
        System.out.println("\nExpense with description '" + descriptionToDelete + "' not found.\n");
    }

    private void updateSavings() {
        monthlySavings = monthlyIncome - getTotalExpensesForMonth();
        yearlySavings = yearlyIncome - getTotalExpensesForYear(LocalDate.now().getYear());
    }

    public double getTotalExpensesForDay() {
        LocalDate currentDate = LocalDate.now();
        double total = 0.0;
        for (Expense expense : expenses) {
            if (expense.getDate().isEqual(currentDate)) {
                total += expense.getAmount();
            }
        }
        return total;
    }

    public double getTotalExpensesForWeek() {
        LocalDate currentDate = LocalDate.now();
        LocalDate weekStart = currentDate.minusDays(currentDate.getDayOfWeek().getValue() - 1);
        LocalDate weekEnd = weekStart.plusDays(6);
        double total = 0.0;
        for (Expense expense : expenses) {
            LocalDate expenseDate = expense.getDate();
            if (!expenseDate.isBefore(weekStart) && !expenseDate.isAfter(weekEnd)) {
                total += expense.getAmount();
            }
        }
        return total;
    }

    public double getTotalExpensesForMonth() {
        LocalDate currentDate = LocalDate.now();
        double total = 0.0;
        for (Expense expense : expenses) {
            if (expense.getDate().getMonthValue() == currentDate.getMonthValue()) {
                total += expense.getAmount();
            }
        }
        return total;
    }

    public double getTotalExpensesForMonth(int yearToCalculate, int monthToCalculate) {
        double total = 0.0;
        for (Expense expense : expenses) {
            LocalDate expenseDate = expense.getDate();
            if (expenseDate.getYear() == yearToCalculate && expenseDate.getMonthValue() == monthToCalculate) {
                total += expense.getAmount();
            }
        }
        return total;
    }

    public double getTotalExpensesForYear(int yearToCalculate) {
        double total = 0.0;
        for (Expense expense : expenses) {
            if (expense.getDate().getYear() == yearToCalculate) {
                total += expense.getAmount();
            }
        }
        return total;
    }

    public void suggestInvestmentOpportunity() {
        double percentageToInvest = 0.20; // 20% of savings
        double amountToInvest = monthlySavings * percentageToInvest;
        if (amountToInvest >= 5000) {
            System.out.println("You have a substantial savings amount. Consider investing in stocks or mutual funds for potential higher returns.");
        } else if (amountToInvest >= 1000) {
            System.out.println("With your savings, you can consider opening a high-yield savings account for better interest rates.");
        } else {
            System.out.println("You don't have enough savings to consider investing at the moment.");
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ExpenseTracker e = new ExpenseTracker();
        int choice = 1;
        do {
            System.out.println("Expense Tracker Menu:");
            System.out.println("\n1. Set Minimum Balance");
            System.out.println("2. Add Income");
            System.out.println("3. Add an expense");
            System.out.println("4. View expenses");
            System.out.println("5. Delete an expense");
            System.out.println("6. View a Specific Month/Year Expense");
            System.out.println("7. View Savings of Month and Year");
            System.out.println("8. See Investment Options");
            System.out.println("9. Exit");
            System.out.print("\nEnter your choice: ");
            choice = scanner.nextInt();
            switch (choice) {
                case 1:
                    System.out.print("Enter the Minimum Balance: ");
                    double minBalance = scanner.nextDouble();
                    e.setMinimumExpense(minBalance);
                    break;
                case 2:
                    System.out.print("Enter your Monthly income: ");
                    double in = scanner.nextDouble();
                    e.setMonthlyIncome(in);
                    break;
                case 3:
                    System.out.print("Enter Expense Description: ");
                    String description = scanner.next();
                    System.out.print("Enter Expense amount: ");
                    double amount = scanner.nextDouble();
                    e.addExpense(description, amount);
                    break;
                case 4:
                    e.viewExpenses();
                    break;
                case 5:
                    System.out.print("Enter the Description of the Expense to Delete: ");
                    String descriptionToDelete = scanner.next();
                    e.deleteExpense(descriptionToDelete);
                    break;
                case 6:
                    System.out.println("Enter choice:");
                    System.out.println("\n1. View a Specific Month Expense");
                    System.out.println("2. View a Specific Year Expense");
                    int ch = scanner.nextInt();
                    if (ch == 1) {
                        System.out.println("Enter the Specific Month to View Expense:");
                        int mon = scanner.nextInt();
                        System.out.println("Enter the Specific Year to View Expense:");
                        int year = scanner.nextInt();
                        System.out.format("| %-34s | %27f |%n", "Total Expenses  ", e.getTotalExpensesForMonth(year, mon));
                    } else if (ch == 2) {
                        System.out.println("Enter the Specific Year to View Expense:");
                        int year = scanner.nextInt();
                        System.out.format("| %-34s | %27f |%n", "Total Expenses  ", e.getTotalExpensesForYear(year));
                    } else {
                        System.out.println("Invalid choice. Please select a valid option.");
                    }
                    break;
                case 7:
                    System.out.format("| %-34s | %27f |%n", "Total Monthly Savings:", e.monthlySavings);
                    System.out.format("| %-34s | %27f |%n", "Total Yearly Savings:", e.yearlySavings);
                    break;
                case 8:
                    e.suggestInvestmentOpportunity();
                case 9:
                    System.out.println("Thank you!!");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid choice. Please select a valid option.");
            }
        } while (choice != 8);
    }
}