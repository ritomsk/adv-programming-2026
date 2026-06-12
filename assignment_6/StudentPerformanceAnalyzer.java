import java.util.*;
import java.util.stream.Collectors;

class Student {
    private int id;
    private String name;
    private List<String> courses;
    private Map<String, Integer> scores;
    private double averageScore;

    public Student(int id, String name, List<String> courses, Map<String, Integer> scores) {
        this.id = id;
        this.name = name;
        this.courses = new ArrayList<>(courses);
        this.scores = new HashMap<>(scores);
        this.averageScore = calculateAverageScore();
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public List<String> getCourses() { return courses; }
    public Map<String, Integer> getScores() { return scores; }
    public double getAverageScore() { return averageScore; }

    private double calculateAverageScore() {
        if (courses == null || courses.isEmpty()) return 0.0;
        
        return courses.stream()
                .mapToInt(course -> scores.getOrDefault(course, 0))
                .average()
                .orElse(0.0);
    }

    @Override
    public String toString() {
        return String.format("Student{id=%d, name='%s', avgScore=%.2f}", id, name, averageScore);
    }
}

public class StudentPerformanceAnalyzer {

    public static List<Student> getTopNStudents(List<Student> students, int n) {
        return students.stream()
                .sorted(Comparator.comparingDouble(Student::getAverageScore).reversed())
                .limit(n)
                .collect(Collectors.toCollection(ArrayList::new));
    }

    public static Map<String, Double> getAverageScorePerCourse(List<Student> students) {
        Map<String, double[]> courseStats = new HashMap<>();

        for (Student student : students) {
            for (String course : student.getCourses()) {
                courseStats.putIfAbsent(course, new double[]{0.0, 0.0});
                
                double[] stats = courseStats.get(course);
                stats[0] += student.getScores().getOrDefault(course, 0);
                stats[1] += 1;
            }
        }

        
        Map<String, Double> courseAverages = new HashMap<>();
        for (Map.Entry<String, double[]> entry : courseStats.entrySet()) {
            double totalScore = entry.getValue()[0];
            double count = entry.getValue()[1];
            courseAverages.put(entry.getKey(), totalScore / count);
        }

        return courseAverages;
    }

    public static Set<String> getAllUniqueCourses(List<Student> students) {
        return students.stream()
                .flatMap(s -> s.getCourses().stream())
                .collect(Collectors.toCollection(HashSet::new));
    }

    private static List<Student> generateStudents(int n) {
        List<Student> students = new ArrayList<>();
        Random random = new Random();
        String[] allCourses = {"Math", "Physics", "Chemistry", "Biology", "History", "Literature", "Computer Science"};

        for (int i = 1; i <= n; i++) {
            int numCourses = random.nextInt(4) + 2;
            List<String> studentCourses = new ArrayList<>();
            Map<String, Integer> studentScores = new HashMap<>();
            
            List<String> availableCourses = new ArrayList<>(Arrays.asList(allCourses));
            Collections.shuffle(availableCourses, random);

            for (int j = 0; j < numCourses; j++) {
                String course = availableCourses.get(j);
                studentCourses.add(course);
                studentScores.put(course, random.nextInt(41) + 60);
            }

            students.add(new Student(i, "Student_" + i, studentCourses, studentScores));
        }
        return students;
    }

    public static void main(String[] args) {
        int[] sampleSizes = {10, 100, 1000, 10000};

        for (int n : sampleSizes) {
            System.out.println("Sampling for n = " + n);
            List<Student> students = generateStudents(n);

            long startTime = System.nanoTime();
            getTopNStudents(students, Math.min(5, n));
            long endTime = System.nanoTime();
            System.out.printf("Top N Students Time: %.4f ms%n", (endTime - startTime) / 1_000_000.0);

            startTime = System.nanoTime();
            getAverageScorePerCourse(students);
            endTime = System.nanoTime();
            System.out.printf("Average Score Per Course Time: %.4f ms%n", (endTime - startTime) / 1_000_000.0);

            startTime = System.nanoTime();
            getAllUniqueCourses(students);
            endTime = System.nanoTime();
            System.out.printf("Unique Courses Time: %.4f ms%n%n", (endTime - startTime) / 1_000_000.0);
        }
    }
}