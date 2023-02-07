/**
 * Created by Juan on 12/12/2016.
 */

function cleanOrganizationForm() {
    $('.organization-fields input, .organization-fields select').val('');
    initializeSelect($('.organization-fields select'));
}

function generateErrorList(errors) {
    var list = $('<ul class="errorlist"></ul>');
    errors.forEach(function(error) {
        list.append($('<li>' + error + '</li>'));
    });

    return list;
}

function setMode(mode) {
            if (mode === "edit") {
                $("[data-profile-mode='view']").toggleClass("hidden", true);
                $("[data-profile-mode='edit']").toggleClass("hidden", false);
                $("#btn-edit-profile").removeClass("fab-trans");
                $("#btn-cancel-profile-edit").addClass("fab-trans");
                $("#btn-update-user").addClass("fab-trans");
            }
            else {
                $("[data-profile-mode='edit']").toggleClass("hidden", true);
                $("[data-profile-mode='view']").toggleClass("hidden", false);
                $("#btn-edit-profile").addClass("fab-trans");
                $("#btn-cancel-profile-edit").removeClass("fab-trans");
                $("#btn-update-user").removeClass("fab-trans");
            }
}

function getFormData() {
    let data = {};
    $('.form-field').each( function() {
        let id = $(this).prop('id');
        let parameter_name = id.split('id_',2)[1];
        let value = $(this).val();
        data[parameter_name] = value; 
    });
    return data;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    
    $("#btn-edit-profile").on("click", function(){
        setMode("edit");
    });

    $("#btn-cancel-profile-edit").on("click", function(){
        setMode("view");
    });

    if ($(".user-registration .alert-error").length > 0) {
        setMode("edit");
    }

    $("#btn-update-user").on("click", function() {
        let formData = getFormData();
        $.ajax({
            url : '/update_account/',
            headers: { "X-CSRFToken": getCookie("csrftoken")}, 
            method : 'POST',
            data : formData,
            success : function(response) {
                location.reload();
            },
            error : function(response) {
                alert(response.responseText);
            },


        });
    });
    
    var organizationForm = $('div.organization-fields');
    var organizationSelect = $('div.user-fields').find('select[name="organization_id"]');
    initializeSelect(organizationForm.find('[name="organization_id"]'));

    $('<option value="new">Add New Organization...</option>').insertAfter(organizationSelect.children().first());
    organizationSelect.on('change', function() {
        if ($(this).val() === 'new') {
            cleanOrganizationForm();
            $('#organization-dialog').modal('toggle');
        }
    });

    $('#new-organization-button').on('click', function() {
        clearFieldErrors($('.organization-fields .has-error'));
        var data = $('.organization-fields input, .organization-fields select').toArray().reduce(function(dict, field) {
            dict[field.name] = field.value;
            return dict;
        }, {});

        $.ajax({
            url: $('#new-organization-api').val(),
            type: 'post',
            data: $.extend({
                csrfmiddlewaretoken: $('form input[name="csrfmiddlewaretoken"]').val()
            }, data)
        }).done(function(data, message, xhr) {
            if (xhr.status === 201) {
                // organization created
                var newOption = $('<option value="' + data.organization_code + '">' + data.organization_name + '</option>');
                $('.user-fields select[name="organization_code"]').append(newOption).val(data.organization_code);
                $('#organization-dialog').modal('toggle');
            } else if (xhr.status === 206) {
                // organization form error
                var form = $('.organization-fields');

                for (var fieldName in data) {
                    if (!data.hasOwnProperty(fieldName)) {
                        continue;
                    }

                    var element = form.find('[name="' + fieldName + '"]');
                    var field = element.parents('.form-field');
                    var errors = generateErrorList(data[fieldName]);
                    field.addClass('has-error');
                    field.append(errors);

                    element.on('change keypress', function(event, isTriggered) {
                        if (isTriggered) {  // http://i.imgur.com/avHnbUZ.gif
                            return;
                        }

                        var fieldElement = $(this).parents('div.form-field');
                        clearFieldErrors(fieldElement);
                    });
                }
            }
        }).fail(function(data) {
            console.log(data);
        });
    });

    $('#organization-modal-close').on('click', function() {
        var organizationSelect = $('.user-fields select[name="organization_code"]');
        organizationSelect.val('');
        initializeSelect(organizationSelect);
    });
});
