$(document).ready(function(){
	$('.tabs').tabs(); //Inicializo los tabs
	$('.tooltipped').tooltip(); //Inicializo los tooltip
	$('.modal').modal(); //Inicializo las modales
	hideLoader();
	checkIsLogged();
	signup();
	login();
	logout();
	createNote();
});

user = {
	id: null,
	fistName: null,
	lastName: null,
	createdAt: null
};

notesQuantity = 0;

/**
 * Función que se encarga de validar existe una sesion activa
 */
function checkIsLogged() {
	const token = getSession();
	if (token) {
		$('.signup-login').addClass('hide');
		$('.notes').removeClass('hide');
		getUserInfo();
		getNotes();

	}
}


/**
 * Función que escucha el evento submit del formulario signin y
 * hace la petición al API para registrase
 */
function signup() {

	$('#form-signup').unbind().submit((e) => {
		e.preventDefault();
		showLoader();
		const firstName = $('#signup-first_name').val();
		const lastName = $('#signup-last_name').val();
		const password = $('#signup-password').val();
		const email = $('#signup-email').val();
		const data = {first_name: firstName, last_name: lastName, password, email};
		$.ajax({
			type: 'POST',
			url: 'http://localhost:8000/v1/user/signup',
			contentType:  'application/json; charset=utf-8',
			data: JSON.stringify(data)

		}).done((response) => {
			if (response.code == 201) {
				showToast('Se ha registrado exitosamente');
				$('.tabs').tabs('select', 'login');
				$('#form-signup')[0].reset();
			} 

		}).fail((error) => {
			response = error.responseJSON
			if (response !== undefined){
				if (response.code == 412){
					showToast('Email ya existe, por favor introduzca otro');
				} else if (response.code == 400) {
					showToast('Datos inválidos, por favor verifique que tengan el formato correcto');
				}
			} else {
				showToast('Ocurrió un error en la solicitud, por favor intente de nuevo');
			}

		}).always(() => {
			hideLoader();
		});
	});

}

/**
 * Función que escucha el evento submit del formulario de login
 * y hace la petición al api para iniciar sesión
 */
function login() {

	$('#form-login').unbind().submit((e) => {
		e.preventDefault();
		showLoader();
		const password = $('#login-password').val();
		const email = $('#login-email').val();
		const data = {password, email};

		$.ajax({
			type: 'POST',
			url: 'http://localhost:8000/v1/user/login',
			contentType:  'application/json; charset=utf-8',
			data: JSON.stringify(data)

		}).done((response) => {
			if (response.code == 200) {
				$('.signup-login').addClass('hide');
				$('.notes').removeClass('hide');
				saveSession(response.data.token_id);
				getUserInfo();
				getNotes();

			}

		}).fail((error) => {
			response = error.responseJSON
			if (response !== undefined) {
				if (response.code == 401) {
					showToast('Email o contraseña invalidos');
				}
			} else {
				showToast('Ocurrió un error en la solicitud, por favor intente de nuevo');
			}

		}).always(() => {
			hideLoader();
		});
		
	});
}

/**
 * Función que escucha el evento click del boton para cerrar sesión
 * y hace la peticion al API para cerrar sesión
 */
function logout() {

	$('li#logout').click((e) => {
		showLoader();
		$.ajax({
			type: 'POST',
			url: 'http://localhost:8000/v1/secure-user/user/logout',
			contentType:  'application/json; charset=utf-8',
			headers: {
					"Authorization": "Bearer " + getSession()
			}		
		}).done((response) => {
			if (response.code == 200) {
				deleteSession();
				$('.notes').addClass('hide');
				$('.signup-login').removeClass('hide');
				$('.tabs').tabs('select', 'login');
				removeInfoNavbar();
				removeNotes();
			}
		}).fail((error) => {
			response = error.responseJSON;
			if (response !== undefined) {
				if (response.code == 401) {
					deleteSession();
					$('.notes').addClass('hide');
					$('.signup-login').removeClass('hide');
					$('.tabs').tabs('select', 'login');
					removeInfoNavbar();
					removeNotes();
				}
			} else {
				showToast('Ocurrió un error en la solicitud, por favor intente de nuevo');
			}
			
		}).always(() => {
			hideLoader();
		})
	})
}

/**
 * Funcion que escucha el evento submit del formulario de create-note y
 * hace la peticion al api para crear la nota
 */
function createNote() {

	$('#form-create-note').unbind().submit((e) => {
		e.preventDefault();
		showLoader();
		const title = $('#create-note-title').val();
		const content = $('#create-note-content').val();
		const data = {title, content};

		$.ajax({
			type: 'POST',
			url: 'http://localhost:8000/v1/secure-user/note/create',
			contentType:  'application/json; charset=utf-8',
			headers: {
				"Authorization": "Bearer " + getSession()
			},
			data: JSON.stringify(data)

		}).done((response) => {
			if (response.code == 201) {
				showToast('Nota creada');
				$('.modal').modal('close');
				$('#form-create-note')[0].reset();
				addNotesInHtml(response.data.notes);
			}

		}).fail((error) => {
			response = error.responseJSON
			if (response !== undefined) {
				if (response.code == 401 || response.code == 404) {
					showToast('Sesión inactiva, por favor vuelva a iniciar sesión');
					$('.tabs').tabs('select', 'login');
					$('#form-create-note')[0].reset();
					$('.modal').modal('close');
					deleteSession();


				} else if (response.code == 400) {
					showToast('Formato de los datos incorrecto');
				}
			} else {
				showToast('Ocurrió un error en la solicitud, por favor intente de nuevo');
			}
		}).always(() => {
			hideLoader();
		});
		
	});
};

/**
 * Función que realiza la petición al API para obtener los datos del usuario logueado
 */
function getUserInfo() {
	$.ajax({
		type: 'GET',
		url: 'http://localhost:8000/v1/secure-user/user/info',
		contentType:  'application/json; charset=utf-8',
		headers: {
				"Authorization": "Bearer " + getSession()
		}		
	}).done((response) => {
		if (response.code == 200) {
			user.id = response.data.user.id
			user.firstName = response.data.user.first_name
			user.lastName = response.data.user.last_name
			user.createdAt = response.data.user.createdAt
			setInfoNavbar();
		}
		
	}).fail((error) => {
		response = error.responseJSON
		if (response !== undefined) {
			if (response.code == 401 || response.code == 404) {
				showToast('Sesión inactiva, por favor vuelva a iniciar sesión');
				$('.tabs').tabs('select', 'login');
				deleteSession();
			} 
		} else {
			showToast('Ocurrió un error en la solicitud, por favor intente de nuevo');
		}
	})
}


/**
 * Función que realiza la petición al API para obtener las notas del usuario logueado
 */
function getNotes() {
	showLoader();
	$.ajax({
		type: 'GET',
		url: 'http://localhost:8000/v1/secure-user/note/index',
		contentType:  'application/json; charset=utf-8',
		headers: {
				"Authorization": "Bearer " + getSession()
		}		
	}).done((response) => {
		if (response.code == 200) {
			addNotesInHtml(response.data.notes);
		}
	}).fail((error) => {
		response = error.responseJSON
		if (response !== undefined) {
			if (response.code == 401 || response.code == 404) {
				showToast('Sesión inactiva, por favor vuelva a iniciar sesión');
				$('.tabs').tabs('select', 'login');
				deleteSession();
			} 
		} else {
			showToast('Ocurrió un error en la solicitud, por favor intente de nuevo');
		}
	}).always(() => {
		hideLoader();
	})
}

 /**
  * Función que muesta que un loader en la vista
  */
function showLoader(){
	$(".loader").removeClass('hide')
}

/**
 * Función que elimina el loader en la vista
 */
function hideLoader() {
	$(".loader").addClass('hide')
}

/**
 * Función que muestra mensajes informativos
 */
function showToast(message) {
	data = {html: message, displayLength: 3000}
	M.toast(data)
}
 /**
  * Función que guarda el token de sesión en el localstorage
  */
function saveSession(token) {
	localStorage.setItem('aimo-session', token);
}

/**
 * Función que obtiene el token de sesión del localstorage y lo retorna
 */
function getSession() {
	return localStorage.getItem('aimo-session')
}

/**
 * Función que elimina el token de sesión del localstorage
 */
function deleteSession() {
	localStorage.removeItem('aimo-session')
}

/**
 * Función que muestra el nombre y apellido del usuario logueado en la vista
 */
function setInfoNavbar() {
	$('li#username').html(`<i class="material-icons left">account_box</i> ${user.firstName}  ${user.lastName}`);
	$('li#username').removeClass('hide');
	$('li#logout').removeClass('hide');
}


/**
 * Función que borra el nombre y apellido del usuario que estaba logueado
 */
function removeInfoNavbar() {
	$('li#username').text('');
	$('li#username').addClass('hide');
	$('li#logout').addClass('hide');
}

/**
 * Función que agrega las notas al html
 */
function addNotesInHtml(notesArray) {

	

	if (notesArray.length > 0) {
		$(".notes-empty").addClass('hide');
	}

	notesArray.forEach((note, index) => {
		column = ((index + notesQuantity)  % 4) + 1;

		const createdAt = moment(`${note.created_at} +0000`, "DD-MM-YYYY hh:mm:ss Z")
		
		notesHTML =
		`<div class="card teal lighten-1 animation-notes">
			<div class="card-content white-text">
				<div class="row note-title"><span class="card-title">${note.title}</span></div>
				<div class="row note-title"><span class="badge">${createdAt.format('DD-MM-YYYY')}</span></div>
				
				
				<div class="divider"></div
				<p>${note.content}</p>
			</div>
		</div>
		`
		$(`div#column-${column}`).append(notesHTML);
	});

	notesQuantity = notesArray.length
}

/**
 * Función que elimina todas las notas del html
 */
function removeNotes() {
	$("div#column-1").empty();
	$("div#column-2").empty();
	$("div#column-3").empty();
	$("div#column-4").empty();
	notesQuantity = 0;
	$(".notes-empty").removeClass('hide');
}

