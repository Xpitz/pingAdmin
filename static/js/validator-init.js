function initFormValid() {
    $("#command_form").bootstrapValidator({
        live: 'disabled',
        submitButtons: '#submit',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            'assets[]': {
                validators: {
                    notEmpty: {
                        message: '* 资产与资产组必须选择一项'
                    },
                }
            },
            'groups[]': {
                validators: {
                    notEmpty: {
                        message: '* 资产与资产组必须选择一项'
                    }
                }
            },
            modules: {
                validators: {
                    notEmpty: {
                        message: '* 请填写该字段'
                    }
                }
            },
            content: {
                validators: {
                    notEmpty: {
                        message: '* 请填写该字段'
                    }
                }
            },
            sls: {
                validators: {
                    notEmpty: {
                        message: '* 请填写该字段'
                    }
                }
            },
            scripts: {
                validators: {
                    notEmpty: {
                        message: '* 请填写该字段'
                    }
                }
            },
        }
    });
}