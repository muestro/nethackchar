// progress.js


$(document).ready(function(){
    /* key events */
    $('#newCharInput').keypress(function(e){
        if(e.which == 13){
            $('#newCharSaveButton').click();
        }
    });

    $('.editableItem').each(function(){
        if($(this).text() == 'no'){
            $(this).addClass('charDetailsNoValue');
        }else if($(this).text() == 'yes'){
            $(this).addClass('charDetailsYesValue');
        }
    });

    $('#notes').autoResize();

    // update the date fields values of the local time
    $('[dateValue]').each(function(){
        var utcTime = $(this).attr('dateValue');
        var localDateTime = new Date(utcTime);
        $(this).append(localDateTime.toLocaleString());
    });
});

/* Create character */
function showCreateCharacterFields(){
    $('#newCharacterItem').show();
    $('#newCharInput').focus();
}

function removeCreateCharacterFields(){
    $('#newCharacterItem').hide();
    $('#newCharInput').val('');
}

/* Edit Character */
function showEditFields(){
    $('#saveButton').show();
    $('#editButton').hide();
	$('.editableItem').hide();
	$('.editField').show();

    $('#notes').removeAttr('disabled');
}

function hideEditFields(){
	$('.editableItem').show();
	$('.editField').hide();

    $('#notes').attr('disabled', 'true');
}

/* Show Character */
function showCharacter(key){
    window.location.href = "/nethack/progress?charKey=" + key;
}

/* Post functions modifying character */
function createCharacter(){
    var charName = $('#newCharInput').val();
    var data = {};
    data['charName'] = charName;

    // set the cursor to wait
    $("*").css("cursor", "wait");

    // post to the server which will result in a redirect
    $.post('/nethack/progress/createUser', data, function(){
        window.location.href = "/nethack/progress";
    })
    .fail(function(){
        window.location.href = "/nethack/progress";
    });
}

function saveCharacter(){
	var data = {};
    var charKey = $('.characterContainer').attr('key');
	if(charKey){
		data['key'] = charKey;
	}else{
        alert('save failed.');
        return;
    }
    $('.characterContainer').find('.editField[name^="edit_"]').each(function(){
		var value = null;
		if($(this).attr('type') == 'checkbox'){
			if($(this).prop('checked')){
				value = 'yes';
			}else{
				value = 'no';
			}			
		}else{
			value = $(this).val();
		}
		data[$(this).attr('name').split('edit_')[1]] = value;
	});

	$.post('/nethack/progress/save', data, function(){
        window.location.href = "/nethack/progress?charKey=" + charKey;
	})
    .fail(function(){
        window.location.href = "/nethack/progress";
    });
	
	hideEditFields();
}

function deleteCharacter(){
	var data = {};
    var charKey = $('.characterContainer').attr('key');
    if(charKey){
        data['key'] = charKey;

        // set the cursor to wait
        $("*").css("cursor", "wait");

        $.post('/nethack/progress/delete', data, function(data){
            window.location.href = "/nethack/progress";
        })
        .fail(function(){
            window.location.href = "/nethack/progress";
        });
    }

}