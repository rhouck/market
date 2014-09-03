<?php
//If the form is submitted
if(isset($_POST['submit'])) {

	//Check to make sure sure that a valid email address is submitted
	if(trim($_POST['email']) == '')  {
		$hasError = true;
	} else if (!eregi("^[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]{2,4}$", trim($_POST['email']))) {
		$hasError = true;
	} else {
		$email = trim($_POST['email']);
	}

	//If there is no error, send the email
	if(!isset($hasError)) {
		$emailTo = 'avathemesy@gmail.com'; //Put your own email address here
		$body = "Email: $email";
		$headers = 'Website Subscription <'.$emailTo.'>' . "\r\n" . 'Reply-To: ' . $email;
		$subject = 'Website Subscription';

		mail($emailTo, $subject, $body, $headers);
		$emailSent = true;
	}
	
	if(@mail($emailTo,$email,$body)) 
    {   
        $url = 'http://avathemes.com/HTML5/FlatrComingSoon/"';
    echo '<META HTTP-EQUIV=Refresh CONTENT="0; URL='.$url.'">';
    } else {
        echo 'Please check if you have filled all the fields with valid information and try again. Thank you';
	 } 
}
?>
	