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
        padding: 40px;
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
</style>

<body>

<div class="row">
    <div class="column">
        <?php require("polling_average.html") ?>
        <br/>
        <?php require("pollsters_recent.html") ?>
    </div>


    <div class="column">
        <?php require("monthly_averages.html") ?>
    </div>

</div>
<br>



<div class="row center">
    <img src="monthly_trend.png"/>
</div>

<div class="row">
    <?php require("top_25.html") ?>
</div>


</body>
</html>