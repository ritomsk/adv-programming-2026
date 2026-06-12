import { useState } from "react";
import './Dashboard.css';

interface Student {
    id: number;
    name: string;
    enrolledCourses: Set<string>;
    gpa: number;
}

const initialStudentsArray: Student[] = [
    {
        id: 1,
        name: "Alice",
        enrolledCourses: new Set(["Math", "Physics", "Chemistry"]),
        gpa: 3.8
    },
    {
        id: 2,
        name: "Bob",
        enrolledCourses: new Set(["Computer Science", "Math"]),
        gpa: 3.9
    },
    {
        id: 3,
        name: "Charlie",
        enrolledCourses: new Set(["History", "Literature"]),
        gpa: 3.2
    }
];

const initialStudentsMap = new Map<number, Student>(
    initialStudentsArray.map(student => [student.id, student])
);

export default function Dashboard() {
    const [studentsMap, setStudentsMap] = useState<Map<number, Student>>(initialStudentsMap);
    
    const [isSorted, setIsSorted] = useState(false);
    const [activeSearch, setActiveSearch] = useState("");
    const [name, setName] = useState("");
    const [gpa, setGpa] = useState("");
    const [courses, setCourses] = useState("");
    const [removeId, setRemoveId] = useState("");
    const [searchQuery, setSearchQuery] = useState("");

    const [isOpenAdd, setIsOpenAdd] = useState(false);
    const [isOpenRemove, setIsOpenRemove] = useState(false);
    const [isOpenSearch, setIsOpenSearch] = useState(false);

    const handleAddSubmit = () => {
        if (!name.trim() || !gpa) return; 

        const studentsArray = Array.from(studentsMap.values());
        const newId = studentsArray.reduce((maxId, student) => Math.max(maxId, student.id), 0) + 1;
        
        const courseArray = courses.split(',').map(c => c.trim()).filter(c => c !== "");
        const courseSet = new Set(courseArray); 
        
        const newStudent: Student = {
            id: newId,
            name: name,
            enrolledCourses: courseSet,
            gpa: parseFloat(gpa)
        };

        setStudentsMap(new Map([...studentsMap, [newId, newStudent]]));
        
        setIsOpenAdd(false);
        setName(""); 
        setGpa(""); 
        setCourses(""); 
    };

    const handleRemoveSubmit = () => {
        if (!removeId) return;
        const targetId = parseInt(removeId);

        const filteredEntries = Array.from(studentsMap.entries()).filter(([id]) => id !== targetId);
        
        setStudentsMap(new Map([...filteredEntries]));
        
        setIsOpenRemove(false);
        setRemoveId("");
    };

    const handleSearchSubmit = () => {
        setActiveSearch(searchQuery);
        setIsOpenSearch(false);
        setSearchQuery("");
    };

    const handleUniqueCourses = () => {
        const allCoursesSet = Array.from(studentsMap.values()).reduce((acc, student) => {
            return new Set([...acc, ...student.enrolledCourses]);
        }, new Set<string>());

        alert(`Unique Courses across all students:\n${Array.from(allCoursesSet).join(', ')}`);
    };

    let displayedStudents = Array.from(studentsMap.values());

    if (activeSearch) {
        displayedStudents = displayedStudents.filter(student =>
            Array.from(student.enrolledCourses).some(course =>
                course.toLowerCase().includes(activeSearch.toLowerCase())
            )
        );
    }

    if (isSorted) {
        displayedStudents = [...displayedStudents].sort((a, b) => b.gpa - a.gpa);
    }

    return (
        <div className="dashboard-wrapper">
            <h1>Course Enrollment Dashboard</h1>
            
            <div className="display-students">
                <div className="display-nav">
                    <button onClick={() => setIsOpenAdd(true)}>Add new student</button>
                    <button onClick={() => setIsOpenRemove(true)}>Remove student</button>
                    <button onClick={() => setIsSorted(!isSorted)}>
                        {isSorted ? "Unsort" : "Sort (GPA desc)"}
                    </button>
                    <button onClick={handleUniqueCourses}>Unique Courses</button>
                    <button onClick={() => setIsOpenSearch(true)}>Search by course</button>
                    {activeSearch && (
                        <button className="clear-btn" onClick={() => setActiveSearch("")}>Clear Search</button>
                    )}
                </div>

                {activeSearch && <h3>Showing students enrolled in: "{activeSearch}"</h3>}

                <div className="students-container">
                    {displayedStudents.map((student) => (
                        <div className="student-box" key={student.id}>
                            <div className="student-header">
                                <strong>{student.name}</strong>
                                <span className="student-id">ID: {student.id}</span>
                            </div>
                            <div><strong>GPA:</strong> {student.gpa}</div>
                            <div><strong>Courses:</strong> {Array.from(student.enrolledCourses).join(', ')}</div>
                        </div>
                    ))}
                    {displayedStudents.length === 0 && <p>No students found.</p>}
                </div>
            </div>

            {isOpenAdd && (
                <div className='add-popup'>
                    <div className="add-container">
                        <h2>Add Student</h2>
                        <div className="form-group">
                            <label htmlFor="name">Name</label>
                            <input type="text" name="name" value={name} onChange={(e) => setName(e.target.value)} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="gpa">GPA</label>
                            <input type="number" step="0.1" name="gpa" value={gpa} onChange={(e) => setGpa(e.target.value)} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="courses">Enrolled Courses (comma separated)</label>
                            <input type="text" name="courses" value={courses} placeholder="e.g. Math, History" onChange={(e) => setCourses(e.target.value)} />
                        </div>
                        <div className="modal-actions">
                            <button onClick={handleAddSubmit}>Save</button>
                            <button onClick={() => setIsOpenAdd(false)}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

            {isOpenRemove && (
                <div className="remove-popup">
                    <div className="remove-container">
                        <h2>Remove Student</h2>
                        <div className="form-group">
                            <label htmlFor="userId">Enter ID to remove</label>
                            <input type="number" name="userId" value={removeId} onChange={(e) => setRemoveId(e.target.value)} />
                        </div>
                        <div className="modal-actions">
                            <button className="danger-btn" onClick={handleRemoveSubmit}>Remove</button>
                            <button onClick={() => setIsOpenRemove(false)}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

            {isOpenSearch && (
                <div className="search-popup">
                    <div className="search-container">
                        <h2>Search Course</h2>
                        <div className="form-group">
                            <label htmlFor="course">Enter Course Name</label>
                            <input type="text" name="course" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                        </div>
                        <div className="modal-actions">
                            <button onClick={handleSearchSubmit}>Search</button>
                            <button onClick={() => setIsOpenSearch(false)}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}