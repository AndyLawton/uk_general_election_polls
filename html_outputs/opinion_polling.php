<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="keywords" content="polling, westminster, general elections, polls"/>
    <meta name="author" content="Andy Lawton">
    <meta name="description" content="Latest polling average for Westminster Elections"/>
    <title>Westminster Opinion Polling</title>
    <link rel="icon" type="image/x-ico" href="favicon.ico" />
</head>

<style>
    * {
        box-sizing: border-box;
    }

    /* Create two unequal columns that floats next to each other */
    .column {
        float: left;
        width:50%;
        padding: 25px;
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

    #T_last_25_polls_ .date_started {
        text-align: center !important;
    }

    body {
        max-width:1300px;
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



<div class="row center" style="text-align: center;">
    <img src="monthly_trend.png"/>
</div>

<div class="row center">

    <h2> Last 25 Polls </h2>
    <?php require("top_25.html") ?>
</div>


</body>
</html>