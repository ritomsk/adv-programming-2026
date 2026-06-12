import java.util.ArrayList;
import java.util.List;

class Account {
    private String accountNumber;
    private String ownerName;
    private double balance;

    public Account(String accountNumber, String ownerName) {
        this(accountNumber, ownerName, 0.0);
    }

    public Account(String accountNumber, String ownerName, double balance) {
        if (balance < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative");
        }
        this.accountNumber = accountNumber;
        this.ownerName = ownerName;
        this.balance = balance;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public void setAccountNumber(String accountNumber) {
        this.accountNumber = accountNumber;
    }

    public String getOwnerName() {
        return ownerName;
    }

    public void setOwnerName(String ownerName) {
        this.ownerName = ownerName;
    }

    public double getBalance() {
        return balance;
    }

    protected void setBalance(double balance) {
        this.balance = balance;
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive");
        }
        this.balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive");
        }
        if (amount > balance) {
            throw new IllegalArgumentException("Insufficient balance");
        }
        this.balance -= amount;
    }

    public void display() {
        System.out.printf("Account: %s | Owner: %s | Balance: $%.2f%n", accountNumber, ownerName, balance);
    }
}

class SavingsAccount extends Account {
    private double interestRate;

    public SavingsAccount(String accountNumber, String ownerName, double balance, double interestRate) {
        super(accountNumber, ownerName, balance);
        if (interestRate < 0) {
            throw new IllegalArgumentException("Interest rate cannot be negative");
        }
        this.interestRate = interestRate;
    }

    public double getInterestRate() {
        return interestRate;
    }

    public void setInterestRate(double interestRate) {
        if (interestRate < 0) {
            throw new IllegalArgumentException("Interest rate cannot be negative");
        }
        this.interestRate = interestRate;
    }

    @Override
    public void display() {
        super.display();
        System.out.printf("Account Type: Savings | Interest Rate: %.2f%% | Estimated Interest: $%.2f%n", 
                interestRate, getBalance() * (interestRate / 100));
    }
}

class CurrentAccount extends Account {
    private double overdraftLimit;

    public CurrentAccount(String accountNumber, String ownerName, double balance, double overdraftLimit) {
        super(accountNumber, ownerName, balance);
        if (overdraftLimit < 0) {
            throw new IllegalArgumentException("Overdraft limit cannot be negative");
        }
        this.overdraftLimit = overdraftLimit;
    }

    public double getOverdraftLimit() {
        return overdraftLimit;
    }

    public void setOverdraftLimit(double overdraftLimit) {
        if (overdraftLimit < 0) {
            throw new IllegalArgumentException("Overdraft limit cannot be negative");
        }
        this.overdraftLimit = overdraftLimit;
    }

    @Override
    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive");
        }
        if (amount > getBalance() + overdraftLimit) {
            throw new IllegalArgumentException("Overdraft limit exceeded");
        }
        setBalance(getBalance() - amount);
    }

    @Override
    public void display() {
        super.display();
        System.out.printf("Account Type: Current | Overdraft Limit: $%.2f%n", overdraftLimit);
    }
}

public class BankingSystem {
    public static void main(String[] args) {
        List<Account> accounts = new ArrayList<>();

        accounts.add(new SavingsAccount("SA-1001", "Alice", 1000.00, 4.5));
        accounts.add(new CurrentAccount("CA-2001", "Bob", 500.00, 300.00));
        accounts.add(new Account("BA-3001", "Charlie"));

        for (Account acc : accounts) {
            try {
                acc.deposit(200.00);
            } catch (IllegalArgumentException e) {
                System.out.println("Deposit Error for " + acc.getOwnerName() + ": " + e.getMessage());
            }

            try {
                acc.withdraw(800.00);
            } catch (IllegalArgumentException e) {
                System.out.println("Withdrawal Error for " + acc.getOwnerName() + ": " + e.getMessage());
            }
        }

        System.out.println("\n--- Final Account States ---");
        for (Account acc : accounts) {
            acc.display();
            System.out.println("--------------------------------------------------");
        }
    }
}