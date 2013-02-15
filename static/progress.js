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
}

function hideEditFields(){
	$('.editableItem').show();
	$('.editField').hide();
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
    $.post('/nethack/progress/createUser', data, function(data){
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
    $('.characterContainer').find('.editField').each(function(){
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



	$.post('/nethack/progress/save', data, function(data){
        window.location.href = "/nethack/progress?charKey=" + charKey;
	});
	
	hideEditFields();
}

function deleteCharacter(){
	var data = {};
    var charKey = $('.characterContainer').attr('key');
    if(charKey){
        data['key'] = charKey;
        $.post('/nethack/progress/delete', data, function(data){
            window.location.href = "/nethack/progress";
        });
    }else{
        alert('delete failed.');
    }

}