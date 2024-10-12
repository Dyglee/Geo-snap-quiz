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
        startQuizSection.style.display = "none";
        quizSection.style.display = "block";
        resetQuiz();
        loadNextQuestion();
    });

    // Function to fetch and display the next question
    function loadNextQuestion() {
        if (questionNumber < totalQuestions) {
            // Fetch new quiz question from the server
            fetch("/get_question")
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);  // Show error if no more images are available
                    } else {
                        // Display the new image and options
                        quizImage.src = data.image_path;
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
                    }
                })
                .catch(error => console.error('Error fetching question:', error));  // Error handling
        } else {
            // End the quiz after 20 questions
            endQuiz();
        }
    }

    // Function to reset the quiz data on the server
    function resetQuiz() {
        fetch("/reset_quiz", { method: 'POST' })
            .then(response => response.json())
            .then(data => console.log(data.message))  // Handle reset response
            .catch(error => console.error('Error resetting quiz:', error));
    }

    // Function to check the selected answer and update the score
    function checkAnswer(selectedCountry, correctCountry) {
        if (selectedCountry === correctCountry) {
            score++;
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
