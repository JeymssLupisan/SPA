function confirmBooking(event) {
    event.preventDefault(); // Prevent the form from submitting immediately

    // Get the date input value
    const dateInput = document.getElementById('date');
    const selectedDate = dateInput.value; // Get the selected date

    // Check if the date is filled
    if (!selectedDate) {
        alert('Please select a date before confirming your booking.'); // Alert the user
        return; // Exit the function if date is empty
    }

    // Show the confirmation modal if the date is filled
    document.getElementById('confirmationModal').style.display = 'flex';
}

// If user clicks 'Yes', submit the form
document.getElementById('confirmYes').onclick = function() {
    document.getElementById('bookingForm').submit(); // Submit the form
}

// If user clicks 'No', close the modal
document.getElementById('confirmNo').onclick = function() {
    document.getElementById('confirmationModal').style.display = 'none'; // Hide the modal
}

// Add event listener to the confirm button
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.button').onclick = confirmBooking; // Attach the confirmBooking function
});
