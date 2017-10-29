<?php
	require("common.php");
	// sessionManager();
	
	//Get subjects
	if(!isset($_SESSION["subjects"]))
	{
		$_SESSION["subjects"] = array("subject1", "subject2", "subject3");
	}
?>


<!DOCTYPE html>
<html>
	<head>
		<?php echo $htmlHeaders; ?>
		<link rel="stylesheet" href="//netdna.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css">
		<link href='https://fonts.googleapis.com/css?family=Raleway:100' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" href="ratings.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
		<title>Course Feedback</title>
		<style>
			table
			{
				table-layout: fixed;
				width: 100%;
				text-align: left;
			}
			table, tr, td, th
			{
				border: none;
				overflow:hidden;
			}
			td, th
			{
				padding: 0px 20px;
			}
			th
			{
				background-color: white;
				font-weight: bold;
			}
			td
			{
				height: 35px;
				background-color: rgba(255, 255, 255, 0.5);
				word-wrap:break-word;
			}

			.high1:hover .high2:not([rowspan]) 
			{
				background: rgba(255, 255, 255, 0.35)
			}
			.high1:hover .high2[rowspan]:hover ~ .high2
			{
				background: none;
			}
			
			td a 
			{
    				display:block;
    				width:100%;
			}
			.displayLetter
			{
				font-family: 'Raleway', sans-serif;
			    	font-weight: 100;
			    	font-size: 50px;
			    	color: darkblue;
			    	font-style: italic;
			    	line-height: 60px;
			}
		</style>
	</head>
	<body class="cbp-spmenu-push">
		<?php setBackground() ?>
		<div class="content">
			<div id="main">
				<div id="pageOne" class="panel">
					<p class="cent overview">Share your thoughts on courses, or get ideas for next semester!</p>
				
					<br /><br />
					<div class="cent">
						<div class="actionContainer">
							<a id="share" class="action"><img class="actionIcon" src="http://mytimetable.xyz/university/media/bubble-icon.png" alt="Share Thoughts" href="#"></a>
							<a id="top" class="action"><img class="actionIcon" src="http://mytimetable.xyz/university/media/gold-star.png" alt="Top Courses" href="#"></a>
							<a id="view" class="action"><img class="actionIcon" src="http://mytimetable.xyz/university/media/search-icon.png" alt="Search Feedback" href="#"></a>
							<div style="clear:both;"></div>
						</div>
						<br /><br />
						<span class="actionDescription"></span>
					</div>
				</div>
				
				<div id="pageTwo" class="panel" style="display: none">
					<p class="cent overview">Select one of your enrolled courses below to provide feedback on:</p>
				
					<br /><br />
					<div class="cent">
						<div class="actionContainer">
							<?php
								foreach($_SESSION["subjects"] as $subject)
								{
									echo '<a class="action subject" style="display: table;"><span class="actionIcon" style="display: table-cell; vertical-align: middle; font-weight: bold; color: #008300;">' . $subject . '</span></a>';
								}
							?>
							<div style="clear:both;"></div>
						</div>
						<br /><br />
						<span class="actionDescription"></span>
					</div>
				</div>
				
				<div id="pageThree" class="panel" style="display: none">
					<p class="cent overview">Let other students know what you thought of the course:</p>
					
					<div class="cent">
						<form class="pure-form" action="#">
							<!--Star Rating Css Provided by: http://www.cssscript.com/simple-5-star-rating-system-with-css-and-html-radios/-->
							<div class="stars">
								<input class="star star-5" id="star-5" type="radio"/>
							    	<label class="star star-5" for="star-5"></label>
							    	<input class="star star-4" id="star-4" type="radio"/>
							    	<label class="star star-4" for="star-4"></label>
							    	<input class="star star-3" id="star-3" type="radio"/>
							    	<label class="star star-3" for="star-3"></label>
							    	<input class="star star-2" id="star-2" type="radio"/>
							    	<label class="star star-2" for="star-2"></label>
							    	<input class="star star-1" id="star-1" type="radio"/>
							    	<label class="star star-1" for="star-1"></label>
							</div>
							<fieldset class="pure-group">
				                		<textarea autofocus id="comments" placeholder="Comments (what you thought was great, not so great, what to expect, any pro-tips etc.)..." style="font-size: 16px; display: block; width: 100%; height: 150px; margin: auto;"></textarea>
				                	</fieldset>
				                	<br />
				                	<button class="pure-button button-warning back">Cancel</button>
				                	<button class="pure-button button-success" id="submitRating">Submit</button>
						</form>
					</div>
				</div>
				
				<div id="pageFour" class="panel" style="display: none">
					<p class="cent overview">Search for a course to view its ratings and comments:</p>
					
					<div class="cent">
						<form class="pure-form" action="#">
							<input type="text" id="searchCourseField" placeholder="e.g. MSCI2001">
							<button class="pure-button pure-button-primary" id="searchCourseSubmit">Search</button>
						</form>
						<br /><br />
						<div id="average"></div>
						<br />
						<table id="results"></table>
						<br /><br />
						<button class="pure-button button-warning back">Back</button>
					</div>
				</div>
				<div id="pageFive" class="panel" style="display: none">
					<p class="cent overview">Current top voted courses:</p>
					
					<div class="cent">
						<p>Coming Soon</p>
						<table id="top-courses-list"></table>
						<br /><br />
						<button class="pure-button button-warning back">Back</button>
					</div>
				</div>
			</div>
		</div>
		<?php echo $jsMenu; ?>
		<script>
			var selectedCourse = "";
			
			$(document).ready(function()
			{
		    		setupHover();
			});		
			$( "form" ).submit(function(e)
			{
				e.preventDefault();
			});
			
			$( ".back" ).click(function () 
			{
				$( "#pageThree, #pageFour, #pageFive" ).fadeOut( 400, function(){
					$( "#pageOne" ).delay(400).fadeIn( "slow" );
			      	});
			});
			
			$( "#print" ).click(function () 
			{
				window.print();
			});
			
			$( "#share" ).click(function ()
			{
				$( "#pageOne" ).fadeOut( 400, function(){
					$( "#pageTwo" ).fadeIn( "slow" );
			      	});
			});
			
			$( "#submitRating" ).click(function ()
			{
				
				//Loading(true);
//
				var userRating = 0;
				if($("#star-5").is(':checked'))
				{
					userRating = 5;
				}
				else if($("#star-4").is(':checked'))
				{
					userRating = 4;
				}
				else if($("#star-3").is(':checked'))
				{
					userRating = 3;
				}
				else if($("#star-2").is(':checked'))
				{
					userRating = 2;
				}
				else if($("#star-1").is(':checked'))
				{
					userRating = 1;
				}
				
				var data = {course: selectedCourse, rating: userRating, comment: $( "#comments" ).val()};
				$.post( location.protocol + "//" + location.hostname + "/rateCourse.php", data, function(apiResponse)
				{
					
				}, 'json')
				.done(function(apiResponse) 
				{
					if(apiResponse["STATUS"] == "Success")
					{
						
						////Loading(false);

						swal({   title: "Success!",   text: "Your feedback has been saved, Thanks.",   type: "success",   showCancelButton: false}, function(){ 
							////Loading(true); 
							window.location.href = "index.php"; });
					}
					else
					{
						
						////Loading(false);

						sweetAlert("Error!", apiResponse["MESSAGE"], "error");
					}
				})
				.fail(function(errorThrown) 
				{
					
					////Loading(false);

					sweetAlert("Error!", "An error occurred submitting your feedback", "error");
				});
			});
			
			$( "#view" ).click(function ()
			{
				$( "#pageOne" ).fadeOut( 400, function(){
					$( "#pageFour" ).fadeIn( "slow" );
			      	});
			});
			
			$( "#searchCourseSubmit" ).click(function ()
			{
				
				//Loading(true);
//
				var data = {course: $( "#searchCourseField").val().toUpperCase()};
				$.post( location.protocol + "//" + location.hostname + "/getCourseRating.php", data, function(apiResponse)
				{
					
				}, 'json')
				.done(function(apiResponse) 
				{
					if(apiResponse["STATUS"] == "Success")
					{
						
						////Loading(false);

						$( "#average" ).empty();
						$( "#results" ).empty();
						var courseRating = apiResponse["RATING"];
						var courseRating_rounded = rounded = Math.round( courseRating );
						var comments = apiResponse["COMMENTS"];
						if(comments.length > 0)
						{
							for(var j = 0; j < courseRating_rounded; j++)
							{
								$( "#average" ).append("<img src='http://mytimetable.xyz/university/media/gold-star.png' alt='Star' width='35' height='35'>");
							}
							
							$( "#results" ).append("<tr><th style='text-align: center; width: 20%;''>Rating</th><th>Comment</th></tr>");
							for (var i = 0; i < comments.length; i++) 
							{
							    var comment = comments[i];
							    $( "#results" ).append("<tr><td class='displayLetter' style='text-align: center; width: 20%;'>" + comment["Rating"] + "</td><td>" + comment["Comment"] + "</td></tr>");
							}
						}
						else
						{
							$( "#results" ).append("<tr><td colspan='2' style='font-style: italic;'>No feedback available for this subject at the moment...</td></tr>");	
						}
					}
					else
					{
						
						////Loading(false);

						sweetAlert("Error!", apiResponse["MESSAGE"], "error");
					}
				})
				.fail(function(errorThrown) 
				{
					
					////Loading(false);

					sweetAlert("Error!", "An error occurred submitting your feedback", "error");
				});
			});
			
			$( ".subject" ).on("click", function ()
			{
				selectedCourse = $(this).text();
				$( "#pageTwo" ).fadeOut( 400, function(){
					$( "#pageThree" ).fadeIn( "slow" );
			      	});
			});
			
			$( "#top" ).click(function ()
			{
				$( "#pageOne" ).fadeOut( 400, function(){
					$( "#pageFive" ).fadeIn( "slow" );
			      	});
			});
		
			function setupHover()
			{
				$(".action").hover(function()
		    		{
		        		$(this).css("background-color", "rgba(255, 255, 255, 0.5)");
		        		$('.actionDescription').text($(this).children("img").attr("alt"));
		    		}, 
		    		function()
		    		{
		        		$(this).css("background-color", "white");
		        		$('.actionDescription').text('');
		    		});
			}
		</script>
	</body>
</html>