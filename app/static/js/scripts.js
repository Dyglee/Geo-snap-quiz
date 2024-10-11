function showForm(formType) {
    const loginForm = document.getElementById('login-form-container');
    const signupForm = document.getElementById('signup-form-container');

    if (formType === 'login') {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
    } else if (formType === 'signup') {
        signupForm.style.display = 'block';
        loginForm.style.display = 'none';
    }
}

function validateSignupForm() {
    const email = document.getElementById('signup-email').value;
    const confirmEmail = document.getElementById('confirm-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (email !== confirmEmail) {
        alert('Emails do not match!');
        return false;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return false;
    }

    return true;  // Allow form submission if validation passes
}

document.addEventListener("DOMContentLoaded", function() {
    const startQuizBtn = document.getElementById("start-quiz-btn");
    const startQuizSection = document.getElementById("start-quiz-section");
    const quizSection = document.getElementById("quiz-section");
    const quizImage = document.getElementById("quiz-image");
    const quizOptionsContainer = document.getElementById("quiz-options");

    // Quiz tracking variables
    let score = 0;
    let questionNumber = 0;
    const totalQuestions = 20;

    // Event listener to start the quiz
    startQuizBtn.addEventListener("click", function() {
        startQuizSection.style.display = "none";  // Hide start button section
        quizSection.style.display = "block";      // Show quiz section
        loadNextQuestion();                       // Load the first question
    });

    // Function to fetch and display the next question
    function loadNextQuestion() {
        if (questionNumber < totalQuestions) {
            // Fetch new quiz question from the server
            fetch("/get_question")
                .then(response => response.json())
                .then(data => {
                    // Display the new image and options
                    quizImage.src = data.image_path;  // Directly assign the correct image path
                    quizOptionsContainer.innerHTML = '';  // Clear previous options

                    data.quiz_options.forEach(option => {
                        const optionButton = document.createElement('button');
                        optionButton.textContent = option;
                        optionButton.classList.add('option-btn');
                        optionButton.addEventListener('click', function() {
                            checkAnswer(option, data.correct_country);
                        });
                        quizOptionsContainer.appendChild(optionButton);
                    });
                });
        } else {
            // End the quiz and show the score
            endQuiz();
        }
    }

    // Function to check the answer and update the score
    function checkAnswer(selectedCountry, correctCountry) {
        if (selectedCountry === correctCountry) {
            score++;  // Increase score for correct answer
        }

        questionNumber++;  // Move to the next question

        // Load the next question or end the quiz
        loadNextQuestion();
    }

    // Function to end the quiz and display the final score
    function endQuiz() {
        quizSection.innerHTML = `<h2>Quiz Complete!</h2>
                                 <p>Your final score is ${score} out of ${totalQuestions}.</p>
                                 <button onclick="window.location.href='/quiz';" class="start-over-btn">Play Again</button>`;
    }
});