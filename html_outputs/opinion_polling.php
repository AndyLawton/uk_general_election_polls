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

    .column10 {
        float: left;
        width:10%;
        padding: 25px;
        text-align: center;
    }

    .column30 {
        float: left;
        width:30%;
        padding: 25px;
        text-align: center;
    }

    .column70 {
        float: left;
        width:70%;
        padding: 25px;
        text-align: center;
    }

    .column100 {
        float: left;
        width:100%;
        padding: 25px;
        text-align: center;
    }

    .center {
        width: 80%;
    }

    .latest {
        margin: auto;
    }

    .chart {
        margin: none;
    }

    .footer {
        text-align: center;
        color: #444444;
    }

    .donation {
        text-align: center;
        color: #111111;
    }

    .footer a, a:hover, a:visited, a:active {
      color: inherit;
      text-decoration: none;
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

    #T_polling_average .row0 {
        font-weight:bold;
        font-size:2em !important;
    }

    #T_last_25_polls .date_started {
        text-align: center !important;
    }

    body {
        max-width:1300px;
        margin: auto;

    }
</style>

<body>

<div class="row">
    <div class="column30">
        <h1> Polling Average </h1>
    </div>


    <div class="column70">
        <br>
        <?php require("polling_average.html") ?>
    </div>

</div>

<div class="row center chart" style="text-align: center;">
    <img src="campaign_polling.png"/>
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



<div class="row center chart" style="text-align: center;">
    <img src="monthly_trend.png"/>
</div>

<div class="row center latest">

    <h2> Last 25 Polls </h2>
    <?php require("top_25.html") ?>
</div>

<br>
<br>
<div class="row center donation">
    <a href='https://ko-fi.com/andlawton'> Buy me a coffee to keep this site running at Ko-Fi </a>
</div>
<br>
<div class="row center footer">
    &#169; <a href='https://andylawton.com'> Andy Lawton </a>
</div>
<br>


</body>
</html>