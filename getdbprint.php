<?php
$conn = pg_connect('host=192.168.100.181 port=5432 dbname=sensor user=postgres password=psql123') or die('Could not connect: '.pg_last_error());

$curDate = date('Y-m-d',time());
$curTime = date('H:i:s',time()-2);

//echo $curTime;
//echo "<br>";

$curSql = "DECLARE cursor1 CURSOR FOR SELECT * FROM sensordata WHERE date = '";
$text = $curSql.$curDate."' AND time = '".$curTime."'";
//echo $text;
$con = new PDO("pgsql:host=192.168.100.181;port=5432;dbname=sensor", "postgres", "psql123");

$con->beginTransaction();
//echo "con";

$stmt = $con->prepare($text);
$stmt->execute();
//echo "stmt";
$innerStatement = $con->prepare("FETCH 1 FROM cursor1");
$val = 0;
while($innerStatement->execute() && $row = $innerStatement->fetch(PDO::FETCH_ASSOC)) {
        $val=$row['data'];
        $val= (int)$val;
}


$num=12;
$arr = array('One'=> $val, 'value'=> $num);
echo (json_encode($arr));



?>
