/*
$('#searchInput').change( function () {
    $('.card').show();
    var filter = $(this).val(); // get the value of the input, which we filter on
    $('.container').find(".card-category:not(:contains(" + filter + "))").parent().css('display','none');
});
*/

$('#searchInput').change(function () {

    var filter = $(this).val();
    console.log(filter);
    /*$('#allCards').find(".card-category:not(:contains(" + filter + "))").parent().css('display','none');*/

    $('#allCards').find(".card-category:not(:contains(" + filter + "))").parent().parent().parent().css('display','none');
});

$('#refreshbtn').on('click',function () {

    $( "#home-section" ).load(window.location.reload() );
});
