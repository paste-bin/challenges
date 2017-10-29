<?php	
	/* This file returns the average rating for a course, and can also return recent comments
	Developed: Saturday 5th September 2015 by Daniel Walsh - Walsh Media Design Services 
	Input Format: GET (course, comments), SESSION (user-id)
	Output Format: JSON */
	
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
	$userID = (isset($_SESSION["user-id"])) ? $_SESSION["user-id"] : NULL;
	$institution = (isset($_SESSION["institution"])) ? $_SESSION["institution"] : NULL;
	$courseCode = (isset($_POST["course"])) ? $_POST["course"] : NULL;
	// if($userID == NULL)
	// {
	// 	exitWithError("Unauthorised Request, please login");
	// }
	// if($courseCode == NULL)
	// {
	// 	exitWithError("Invalid Course Code (required)");
	// }
	$courseCode_clean = mysqli_real_escape_string($con, $courseCode);
	// $courseCode_clean = $courseCode;
	// if($courseCode_clean != $courseCode)
	// {
	// 	exitWithError("Illegal characters in request");
	// }
	// $institution_clean = mysqli_real_escape_string($con, $institution);
	// if($institution_clean != $institution)
	// {
	// 	exitWithError("Illegal characters in request");
	// }
	
	//Get Average Rating
	$query = "SELECT AVG(`Rating`) FROM `CourseRatings` AS Rating WHERE `CourseCode`='$courseCode_clean'";
	$result = queryDatabaseWithStatement($query, $con);
	$result = mysqli_fetch_row($result);
	$average = $result[0];
	
	//Get Comments
	$commentList = array();
	$query = "SELECT `Rating`, `Comment` FROM `CourseRatings` WHERE  `CourseCode`='$courseCode_clean'";
	$result = queryDatabaseWithStatement($query, $con);
	while($row = mysqli_fetch_assoc($result))
	{
		$commentItem = array("Rating" => $row["Rating"], "Comment" => $row["Comment"]);
		array_push($commentList, $commentItem);
	}
	mysqli_close($con);
	
	//Success
	echo json_encode(array("STATUS" => "Success", "RATING" => $average, "COMMENTS" => $commentList));
	
	
	//Functions
	function exitWithError($error)
	{
		echo json_encode(array("STATUS" => "Error", "MESSAGE" => $error));
		exit();
	}
?>