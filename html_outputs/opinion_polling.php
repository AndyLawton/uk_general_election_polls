<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>UK Opinion Polling-2</title>
</head>

<style>
    * {
        box-sizing: border-box;
    }

    /* Create two unequal columns that floats next to each other */
    .column {
        float: left;
        width:50%;
        padding: 10px;
        text-align: center;
    }

    .center {
        width: 80%;
        margin: auto;
    }

    /* Clear floats after the columns */
    .row:after {
        content: "";
        display: table;
        clear: both;
    }

    #T_polling_average_ .row0 {
        font-weight:bold;
        font-size:2em !important;
    }

    body {
        max-width:1200px;
        margin: auto;

    }
</style>

<body>

<div class="row">
    <div class="column">
        <h1> Polling Average </h1>
    </div>


    <div class="column">
        <br>
        <?php require("polling_average.html") ?>
    </div>

</div>

<div class="row">
    <div class="column">
        <h2> Latest Polls by Pollster </h2>
        <?php require("pollsters_recent.html") ?>
    </div>


    <div class="column">
        <h2> Monthly Polling Average </h2>
        <?php require("monthly_averages.html") ?>
    </div>

</div>
<br>



<div class="row center">
    <img src="monthly_trend.png"/>
</div>

<div class="row center">

    <h2> Last 25 Polls </h2>
    <?php require("top_25.html") ?>
</div>


</body>
</html>