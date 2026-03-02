$(document).ready(function () {
  var inputField = $("#user_input");
  var submitButton = $("#submit");

  // Flag to track if the user input was triggered by voice
  var voiceInput = false;

  // Show submit button when user starts typing
  inputField.on("input", function () {
    if ($(this).val().trim() !== "") {
      submitButton.show();
    } else {
      submitButton.hide();
    }
  });

  var recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  var speechSynthesisInstance;
  var textModeButtonAdded = false; // Flag to track if text mode button is added

  recognition.onresult = function (event) {
    var transcript = event.results[0][0].transcript;
    if (transcript.toLowerCase().includes("jarvis")) {
      $("#user_input").val(""); // Clear the input field after detecting "jarvis"
    } else {
      $("#user_input").val(transcript);
      voiceInput = true; // Set the voice input flag
      $("#submit").click(); // Automatically submit the user's input
    }
  };

  function startListening() {
    recognition.start();
    $("#user_input").hide(); // Hide the text input when voice input is active
    stopSpeaking(); // Stop speaking the previous response
    $("#submit").hide(); // Hide the submit button
    if (!textModeButtonAdded) {
      $("#mic-buttons").append(
        '<button id="text-mode" style="width: 100px">Text Mode</button>'
      ); // Add the button to toggle back to text mode if not already added
      textModeButtonAdded = true; // Set flag to true
    }
  }

  function stopListening() {
    recognition.stop();
    $("#user_input").show(); // Show the text input when voice input is stopped
    stopSpeaking(); // Stop speaking the previous response
    $("#submit").show(); // Show the submit button
    $("#text-mode").remove(); // Remove the button to toggle back to text mode
    textModeButtonAdded = false; // Reset flag
  }

  function speakResponse(response) {
    stopSpeaking(); // Stop speaking the previous response if any
    speechSynthesisInstance = new SpeechSynthesisUtterance();
    speechSynthesisInstance.lang = "en-US";
    speechSynthesisInstance.text = response;
    window.speechSynthesis.speak(speechSynthesisInstance);
  }

  function stopSpeaking() {
    if (speechSynthesisInstance && window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel(); // Cancel the speech synthesis if speaking
    }
  }

  $("#submit").click(function () {
    var user_input = $("#user_input").val();
    $("#user_input").val("");
    $("#conversation").empty(); // Clear previous conversation
    $("#conversation").append("<p>You: " + user_input + "</p>");
    if (user_input.toLowerCase() === "add contact") {
      // Append HTML elements for adding a contact
      var contactHtml =
        '<div class="contact-input"><input type="text" id="contact_name" placeholder="Enter contact name"></input><input type="text" id="phone_number" placeholder="Enter phone number"></input><button id="add-contact-btn">Add Contact</button></div>';
      $("#conversation").append(contactHtml);
    } else if (user_input.toLowerCase().startsWith("send message to")) {
      var parts = user_input.split("send message to ")[1].split(",");
      var contactName = parts[0].trim();
      var message = parts[1].trim();
      // Append sending message message to conversation area
      $("#conversation").append(
        "<p>Jarvis: Sending message to " + contactName + "...</p>"
      );
      // Make AJAX call to send message
      $.ajax({
        type: "POST",
        url: "/send_message",
        data: { contact_name: contactName, message: message },
        success: function (data) {
          if (data.success) {
            $("#conversation").append(
              "<p>Jarvis: Message sent successfully.</p>"
            );
          }
          console.log(data.response); // Display response message in console
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
        },
      });
    } else if (user_input.toLowerCase().includes("call")) {
      var contactName = user_input.split("call ")[1];
      // Append calling message to conversation area
      $("#conversation").append(
        "<p>Jarvis: Calling " + contactName + "...</p>"
      );
      // Make AJAX call to initiate call
      $.ajax({
        type: "POST",
        url: "/make_call",
        data: { contact_name: contactName },
        success: function (data) {
          console.log(data.response); // Display response message in console
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
        },
      });
    } else {
      // Send AJAX request to ChatGPT API
      $.ajax({
        type: "POST",
        url: "/ask",
        data: { user_input: user_input },
        success: function (data) {
          // Handle other responses as before
          if (!voiceInput) {
            $("#conversation").append("<p>Jarvis: " + data.response + "</p>");
          } else {
            $("#conversation").append("<p>Jarvis: " + data.response + "</p>");
            speakResponse(data.response);
            voiceInput = false;
          }
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
        },
      });
    }
  });

  // Handle click event for adding a contact
  $("#conversation").on("click", "#add-contact-btn", function () {
    var contactName = $("#contact_name").val();
    var phoneNumber = $("#phone_number").val();
    // Send AJAX request to add contact
    $.ajax({
      type: "POST",
      url: "/add_contact",
      data: { name: contactName, phone_number: phoneNumber },
      success: function (data) {
        $("#conversation").append("<p>Jarvis: " + data + "</p>");
        $(".contact-input").remove(); // Remove contact input fields after adding the contact
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      },
    });
  });

  $("#mic-voice").click(function () {
    startListening(); // Start listening when mic-voice button is clicked
  });

  $("#mic-buttons").on("click", "#text-mode", function () {
    stopListening(); // Stop listening and toggle back to text mode when text mode button is clicked
  });

  recognition.onend = function () {
    // Don't restart recognition as we want it to start only when the button is clicked
  };

  // Logout button click event
  $("#logout").click(function () {
    window.location.href = "/"; // Redirect to the login page
  });

  function displayPastInteractions(interactions) {
    var formattedInteractions = "";
    for (var i = 0; i < interactions.length; i++) {
      formattedInteractions +=
        "<p>User: " +
        interactions[i].question +
        "</p>" +
        "<p>Jarvis: " +
        interactions[i].answer +
        "</p>";
    }
    return formattedInteractions;
  }
});
