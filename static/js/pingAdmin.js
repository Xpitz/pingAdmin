function initSwitchery() {
    var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
    $('.js-switch').each(function() {
        new Switchery($(this)[0], $(this).data());
    });
}

function initTableiCheck() {
    $('#checkAll, #checkItem').iCheck({
        handle : 'checkbox',
        checkboxClass : 'icheckbox_square-blue',
    });
    $('#checkAll').on('ifChecked ifUnchecked', function(event){
        if (event.type === 'ifChecked') {
            $('.checkItem').iCheck('check');
        } else {
            $('.checkItem').iCheck('uncheck');
        }
    });
}

$(document).ready(function() {
    initSwitchery();
    initFormValid();
    initTableiCheck();
});
