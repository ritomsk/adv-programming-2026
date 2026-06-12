import java.util.*;

public class ArrayListBookSearch {
    public static void main(String[] args) {
        ArrayList<String> books = new ArrayList<>();
        Scanner sc = new Scanner(System.in);

        books.add(e: "The Dance of Dragons");
        books.add(e: "The Lean Startup");
        books.add(e: "Harry Potter and the Dealthy Hallows");
        books.add(e: "A song of ice and fire");
        books.add(e: "The blue ocean strategy");
        

        System.out.println(x: "Enter the word toe search");
        String searchWord = sc.nextLine();

        boolean found = false;

        for(String book : books) {
            if (book.toLowerCase().contains(searchWord.toLowerCase())) {
                System.out.println("Found" + book);
                found = true;
            }
        }

        if (!found) {
            System.out.println("No book title found having the word you entered!");
        }

        sc.close();
        
    }
}