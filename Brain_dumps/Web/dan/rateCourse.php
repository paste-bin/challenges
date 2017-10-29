<?php	
	/* This file submits a course rating to the database table.
	Developed: Saturday 5th September 2015 by Daniel Walsh - Walsh Media Design Services 
	Input Format: POST (rating, comment, course), SESSION (user-id)
	Output Format: JSON 

	Made insecure by pasteBin to be used in the COMP3441 CTF */
	
	session_start();
	require_once("./databaseManager.php");
	error_reporting(0);
	
	//Connect
	$con = connectToDatabaseWithName("timetable");
	if($con->connect_errno > 0)
	{
		exitWithError("Error connecting to timetable database (1)");
	}
	if(!mysqli_set_charset($con, "utf8"))
	{
		exitWithError("Error connecting to timetable database (2)");
	}
	
	//Get and sanitize data
	//lol not any more
	// foreach($_POST as $key => $value)
	// {
	// 	$_POST[$key] = htmlentities($value);
	// }
	$userID = (isset($_SESSION["user-id"])) ? $_SESSION["user-id"] : NULL;
	$userRating = (isset($_POST["rating"])) ? $_POST["rating"] : NULL;
	// $userComment = (isset($_POST["comment"])) ? $_POST["comment"] : NULL;

	$userComment = (isset($_POST["comment"])) ? $_POST["comment"] : NULL;
	$courseCode = (isset($_POST["course"])) ? $_POST["course"] : NULL;
	// if($userID == NULL)
	// {
	// 	exitWithError("Unauthorised Request, please login");
	// }
	// if($userRating == NULL)
	// {
	// 	exitWithError("Invalid Rating (required)");
	// }
	// if($courseCode == NULL)
	// {
	// 	exitWithError("Invalid Course Code (required)");
	// }
	// if(!in_array($courseCode, $_SESSION["subjects"]))
	// {
	// 	exitWithError("You can only rate subjects you are currently enrolled in, make sense?");
	// }
	if(!file_get_contents("http://www.purgomalum.com/service/containsprofanity?text=" . urlencode($userComment)) == "false")
	{
		exitWithError("Lets try and keep it clean shall we...");
	}
	$userID_clean = mysqli_real_escape_string($con, $userID);
	$userRating_clean = mysqli_real_escape_string($con, $userRating);
	// $userComment_clean = mysqli_real_escape_string($con, $userComment);
	$userComment_clean = $userComment;
	$courseCode_clean = mysqli_real_escape_string($con, $courseCode);

	// echo $userComment_clean;

	// if(($userID_clean != $userID) || ($userRating_clean != $userRating) || ($userComment_clean != $userComment) || ($courseCode_clean != $courseCode))
	// {
	// 	exitWithError("Illegal characters in request");
	// }
	
	//Sterile Environment #notanymore
	$institution = $_SESSION["institution"];
	$id = $userID_clean . $institution . $courseCode_clean;
	$query = "REPLACE INTO `CourseRatings` (`ID`, `Institution`, `CourseCode`, `Rating`, `Comment`) VALUES ('$id', '$institution', '$courseCode_clean', '$userRating_clean', '$userComment_clean')";
	queryDatabaseWithStatement($query, $con);
	mysqli_close($con);
	success();
	
	//Functions
	function exitWithError($error)
	{
		echo json_encode(array("STATUS" => "Error", "MESSAGE" => $error));
		exit();
	}
	
	function success()
	{
		echo json_encode(array("STATUS" => "Success", "MESSAGE" => "Success"));
		exit();
	}
?>


