<?php
	ini_set('date.timezone', 'Australia/Sydney');

	function connectToDatabaseWithName ($name)
	{
		//add server prefix
		// $name = "PREFIX_HERE_" . $name;
		//return connection
		$tempCon = mysqli_connect("aa12bi54h2ojgj7.cz35zpndbftl.ap-northeast-1.rds.amazonaws.com", "admin", "d033e22ae348aeb5660fc2140aec35850c4da997", "testxss");
		if (mysqli_connect_errno())
  		{
  			return FALSE;
  		}
  		else
  		{
  			return $tempCon;
  		}
	}
	
	function queryDatabaseWithStatement ($statement, $con)
	{
		// Check connection
		if (mysqli_connect_errno())
		{
			return FALSE;
		}
		//perform query
		$result = mysqli_query($con, $statement);
			
		//return data
		return $result;
	}
?>