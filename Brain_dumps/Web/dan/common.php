<?php
	date_default_timezone_set("Australia/Sydney");
	
	// $domain = "//" . $_SERVER['SERVER_NAME'];

	$domain = 'http://testxss.ap-northeast-1.elasticbeanstalk.com';
	
	//Variables
	$htmlHeaders = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="general.css">
		<link href="//fonts.googleapis.com/css?family=Raleway" rel="stylesheet" type="text/css">
		<link href="//fonts.googleapis.com/css?family=Roboto:900,400italic,400" rel="stylesheet" type="text/css">
		<link href="//fonts.googleapis.com/css?family=Kalam:300" rel="stylesheet" type="text/css">
		<link rel="stylesheet" type="text/css" href="//silverpoint.net.au/experiences/suppliers/pure.css">
		<script type="text/javascript" src="//code.jquery.com/jquery-1.11.1.min.js"></script>
		
		<!--Menu-->
		<link class="export-remove" rel="stylesheet" type="text/css" href="' . $domain . '/Libraries/SlideMenu/css/default.css" />
		<link rel="stylesheet" type="text/css" href="' . $domain . '/Libraries/SlideMenu/css/component.css" />
		<script src="' . $domain . '/Libraries/SlideMenu/js/modernizr.custom.js"></script>
		
		<!--Sweetalert-->
		<script src="' . $domain . '/sweetalert/dist/sweetalert.min.js"></script> 
		<link rel="stylesheet" type="text/css" href="' . $domain . '/sweetalert/dist/sweetalert.css">
		
		<!--Loading-->
		<script type="text/javascript" src="' . $domain . '/Libraries/Small-jQuery-Overlay/loading.js"></script>
		<link type="text/css" rel="stylesheet" href="' . $domain . '/Libraries/Small-jQuery-Overlay/loading.css" />';
		
	$jsMenu = '<!-- Classie - class helper functions by @desandro https://github.com/desandro/classie -->
		<script src="' . $domain . '/Libraries/SlideMenu/js/classie.js"></script>
		<script>
			var menuLeft = document.getElementById( "side-menu" ),
            		body = document.body;
			$(".navLeft").click(function()
			{
				classie.toggle( this, "active" );
				classie.toggle( menuLeft, "cbp-spmenu-open" );
				showOverlay();
			});
			
			function showOverlay()
			{
				var docHeight = $(document).height();
				$("<div id=\'overlay\'></div>").hide().appendTo(document.body).fadeIn(300);
			   	$("#overlay")
			      		.height(docHeight)
			    	$("#overlay").click(function()
			    	{
			    		classie.toggle( this, "active" );
					classie.toggle( menuLeft, "cbp-spmenu-open" );
			    		$("#overlay").fadeOut(300, function() 
			    		{
			    			$(this).remove();
			    		});
			    	});
			}
		</script>';
	
	//Functions
	function dbconnect()
	{
		return mysqli_connect("aa12bi54h2ojgj7.cz35zpndbftl.ap-northeast-1.rds.amazonaws.com","admin","d033e22ae348aeb5660fc2140aec35850c4da997","testxss");
	}
	
	function dbquery($con, $query)
	{
		return mysqli_query($con, $query);
	}
	
	function sessionManager()
	{
		session_start();
		$con = dbconnect();
		$userID = $_SESSION["user-id"];
	
		//Session Checking
		if($_SESSION["logged-in"] != "TRUE" || $userID == NULL)
		{
			// session_destroy();
			// $url = "index.html?loc=" . basename($_SERVER['PHP_SELF']);
			// header("Location: $url");
			// die();
			$_SESSION["logged-in"] = "TRUE";
		}
		if(userTimetableCount($con, $userID) <= 0)
		{
			$url = "setup.php";
			header("Location: $url");
			die();
		}
		mysqli_close($con);
	}
	
	function userTimetableCount($con, $userID, $index = 0)
	{
		$userID_clean = mysqli_real_escape_string($con, $userID);
		if($userID != $userID_clean)
		{
			return FALSE;
		}
		$query = "SELECT `TimetableID` FROM `StudentTimetables` WHERE `StudentID` = '$userID_clean' ORDER BY `TimeAdded` DESC LIMIT $index, 1";
		$result = mysqli_query($con, $query);
		$row = mysqli_fetch_assoc($result);
		$_SESSION["timetable"] = $row["TimetableID"];
		setTimetableColours($con, $row["TimetableID"]);
		setInstitutionStyling($row["TimetableID"]);
		return mysqli_num_rows($result);
	}
	
	function getTimetableIDfromIndex($con, $userID, $index)
	{
		$userID_clean = mysqli_real_escape_string($con, $userID);
		$index_clean = mysqli_real_escape_string($con, $index);
		if($userID != $userID_clean || $index_clean != $index)
		{
			return FALSE;
		}
		$query = "SELECT `TimetableID` FROM `StudentTimetables` WHERE `StudentID` = '$userID_clean' ORDER BY `TimeAdded` DESC LIMIT $index_clean, 1";
		$result = mysqli_query($con, $query);
		$row = mysqli_fetch_assoc($result);
		return $row["TimetableID"];
	}
	
	function getTimetable($con, $timetableID)
	{
		$timetableID_clean = mysqli_real_escape_string($con, $timetableID);
		if($timetableID != $timetableID_clean)
		{
			return FALSE;
		}
		$query = "SELECT * FROM `StudentTimetables` WHERE `TimetableID` = '$timetableID_clean'";
		$result = mysqli_query($con, $query);
		$row = mysqli_fetch_assoc($result);
		
		$colours = json_decode($row["ColourScheme"], true);
		if($colours == NULL || count($colours) == 0)
		{
			$colours = array("#B31212", "#F89C38", "#F3D230", "#338033", "#1479CC", "#754A94", "#B0B0B0", "#99402E", "#C2DEF2", "#F7F294");
		}
		$_SESSION["colour-scheme"] = $colours;
		
		$data = array("classes" => $row["ClassArray"], "subjects" => $row["SubjectArray"], "name" => $row["TimetableName"]);
		return $data;
	}
	
	function setTimetableColours($con, $timetableID)
	{
		$timetableID_clean = mysqli_real_escape_string($con, $timetableID);
		if($timetableID != $timetableID_clean)
		{
			return FALSE;
		}
		$query = "SELECT `ColourScheme` FROM `StudentTimetables` WHERE `TimetableID` = '$timetableID_clean'";
		$result = mysqli_query($con, $query);
		$row = mysqli_fetch_assoc($result);
		$colours = json_decode($row["ColourScheme"], true);
		if($colours == NULL || count($colours) == 0)
		{
			$colours = array("#B31212", "#F89C38", "#F3D230", "#338033", "#1479CC", "#754A94", "#B0B0B0", "#99402E", "#C2DEF2", "#F7F294");
		}
		$_SESSION["colour-scheme"] = $colours;
		return $colours;
	}
	
	function setInstitutionStyling($timetableID)
	{
		//Get institution ID
		$con = dbconnect();
		$timetableID_clean = mysqli_real_escape_string($con, $timetableID);
		$query = "SELECT `Institution` FROM `StudentTimetables` WHERE `TimetableID` = '$timetableID_clean'";
		$result = dbquery($con, $query);
		$result = mysqli_fetch_assoc($result);
		$institution = $result["Institution"];

		//Default ID
		if($institution === NULL)
		{
			$institution = -1;
		}
		
		//Get institution data
		$query = "SELECT * FROM `Institutions` WHERE `ID` = '$institution'";
		$result = dbquery($con, $query);
		$result = mysqli_fetch_assoc($result);
		
		//Save to session
		$_SESSION["institution"] = $institution;
		$_SESSION["institution_icon"] = $result["Icon"];
		$_SESSION["institution_background"] = $result["Background"];
		mysqli_close($con);
	}
	
	function setBackground()
	{
		$url = $_SESSION["institution_background"];
		$backgroundImage = $_SESSION["institution_background"] != NULL ? "<div class='background-image' style='background-image: url($url);'></div>" : "<div class='background-image'></div>";
		echo $backgroundImage;
	}
	
	function jsArrayPrint($array)
	{
		if(count($array) > 0)
		{
			$string = '[';
			
			foreach($array as $item)
			{
				$string .= '"' . $item . '", ';
			}
			substr($string, 0, -2);
			
			$string .= ']';
			return $string;
		}
		return null;
	}
	
	function requireSubjectData()
	{
		$con = dbconnect();
		$userID = $_SESSION["user-id"];
		$userID_clean = mysqli_real_escape_string($con, $userID);
		$query = "SELECT `SubjectArray` FROM `StudentTimetables` WHERE `StudentID` = '$userID_clean' ORDER BY `TimeAdded` DESC LIMIT 0, 1";
		$result = dbquery($con, $query);
		$result = mysqli_fetch_assoc($result);
		$subjectArray = json_decode($result["SubjectArray"], TRUE);
		$subjects = array_keys($subjectArray);
		$_SESSION["subjects"] = $subjects;
		mysqli_close($con);
	}
	
	// function addNavigation($title)
	// {
		// $con = dbconnect();
		// $institution = $_SESSION["institution"];
		// $query = "SELECT * FROM `Institutions` WHERE `ID` = '$institution'";
		// $result = dbquery($con, $query);
		// $result = mysqli_fetch_assoc($result);
		
		// echo '
		// <button style="position: absolute; top: 10px; left: 10px;" class="navLeft pure-button pure-button-primary desktop-navigation">&#9776;</button>
		// <nav class="cbp-spmenu cbp-spmenu-vertical cbp-spmenu-left" id="side-menu">
		// 	<h3>Menu</h3>
		// 	<a href="index.php">My Timetable</a>
		// 	<a href="assignments.php">Assignments</a>
		// 	<a href="groups.php">Groups</a>
		// 	<a href="download.php">Download Timetable</a>';
			
		// if($result["CourseDataAvailable"] == "TRUE")
		// {
		// 	echo '
		// 		<a href="courseInfo.php">Course Info</a>
		// 		<a href="courseTimetable.php">Course Timetables</a>
		// 	';
		// }
		
		// echo '
		// 	<a href="ratings.php">Course Feedback</a>
		// 	<a href="profile.php">Profile</a>
		// </nav>
		// <div id="header" class="mobile-navigation shadow" style="display: none;">
		// 	<button style="position: absolute; top: 25px; left: 10px;" class="navLeft pure-button pure-button-primary">&#9776;</button>					
		// 	<h1 style="font-size: 14px;">' . $title . '</h1> 
		// </div>
		// <h1 class="cent desktop-navigation">' . $title . '</h1>';
	// 	mysqli_close($con);
	// }
?>