document.addEventListener('DOMContentLoaded', function() {
    fetchCourses();
});

function fetchCourses() {
    fetch('/api/courses')
        .then(response => response.json())
        .then(data => {
            const courseList = document.getElementById('course-list');
            data.courses.forEach(course => {
                const courseItem = document.createElement('div');
                courseItem.classList.add('course-item');
                courseItem.innerHTML = `
                    <img src="${course.thumbnail}" alt="${course.title}">
                    <div class="course-title">${course.title}</div>
                `;
                courseList.appendChild(courseItem);
            });
        })
        .catch(error => console.error('Error fetching courses:', error));
}

function startLearning() {
    alert('Start Learning button clicked!');
    // Redirect to the course page or perform other actions
}
