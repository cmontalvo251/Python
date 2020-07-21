////VARIABLES TO CHANGE EVERYWEEK
var DATE = 'August 17th, 2020'
var weeknumber = 1;

/////COURSE SPECIFIC ITEMS
var numStudents = 26; 
var name_of_course = 'Instrumentation (ME316)'
var URL = 'INSERT URL HERE'

//Subject of email
var subject = name_of_course + ' Class Attendance Week of ' + DATE;
//Preamble of email.
var preamble = 'You are receiving an automated message from Google Apps Scripts run by Dr Montalvo. \n \n';
//Yes or no
var yes = 'Congratulations. You are elligible to attend class face to face this week. Make sure to wear your party mask. If you would not like to attend no action is required on your part. '
var no = 'Unfortunately you must remain home this week so that class attendance stays at 15 students. '
//End Rant
var endrant = 'Make sure to consult the spreadsheet on attendance to see when you can and cannot attend class: ' + URL

var numWeeks = 15;
var startRow = 4;

///Ok here is my main function loop
function loop() {
  //Get the active spreadhseet. Note this grabs the first sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Attendance");
  
  //?Grab the data range for students - startRow and start Column, number of rows and columns
  var dataRange = sheet.getRange(startRow, 2, numStudents+1, numWeeks+2);
  // Fetch values for each row in the Range.
  var data = dataRange.getValues();
  //Now let's loop through every row
  for (var i = 0; i < data.length; ++i) {
    var row = data[i];
    var name = row[0]; // First Column
    var emailAddress = row[1]; // Second Column
    var yesno = row[weeknumber+1];
    if (yesno == 'yes') {
      var message = yes;
    } else {
      var message = no;
    }
    var dear = 'Hey ' + name + ', \n \n';
    var out_message = dear + preamble + message + endrant;
    //Send Email
    if (i == 0) {
      MailApp.sendEmail(emailAddress, subject, out_message);  
    }
    sheet.getRange(startRow + i, numWeeks+4).setValue('Message Sent');
    // Make sure the cell is updated right away in case the script is interrupted
    SpreadsheetApp.flush(); 
  }
}


