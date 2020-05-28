(function($) {
    $(document).on('formset:added', function(event, $row, formsetName) {
        console.log(formsetName);
        if (formsetName == 'product_set') {
            //console.log(formsetName);
        }
    });

    $(document).on('formset:removed', function(event, $row, formsetName) {
        // Row removed
    });
})(django.jQuery);
