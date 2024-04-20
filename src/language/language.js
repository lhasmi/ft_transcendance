const texts = {
	tournament: {
		en: 'tournament',
		de: 'tournier',
		ru: 'турнир'
	},
	profile: {
		en: 'profile',
		de: 'profil',
		ru: 'профиль'
	},
	friends: {
		en: 'friends',
		de: 'freunde',
		ru: 'друзья'
	},
	logout: {
		en: 'logout',
		de: 'ausloggen',
		ru: 'выйти'
	},
	login: {
		en: 'login',
		de: 'loggen',
		ru: 'войти'
	},
	register: {
		en: 'register',
		de: 'anmeldung',
		ru: 'регистрация'
	},
	status: {
		en: 'status',
		de: 'status',
		ru: 'статус'
	},
	offline: {
		en: 'offline',
		de: 'offline',
		ru: 'офлайн'
	},
	online: {
		en: 'online',
		de: 'online',
		ru: 'онлайн'
	},
	loginToPlay: {
		en: 'login to play online',
		de: 'loggen zu spielen online',
		ru: 'войди чтобы играть онлайн'
	},
	alreadyHaveAcc: {
		en: 'already have an account?',
		de: 'habt ein Konto?',
		ru: 'уже есть аккаунт?'
	},
	dontHaveAcc: {
		en: 'don’t have an account?',
		de: 'habt kein Konto?',
		ru: 'еще не зарегестрирован?'
	},
	username: {
		en: 'username',
		de: 'username',
		ru: 'имя пользователя'
	},
	email: {
		en: 'email',
		de: 'email',
		ru: 'эпочта'
	},
	password: {
		en: 'password',
		de: 'passwort',
		ru: 'пароль'
	},
	editProfile: {
		en: 'edit profile',
		de: 'bearbeiten profil',
		ru: 'изменить профиль'
	},
	gamesHistory: {
		en: 'games history',
		de: 'spielegeschichte',
		ru: 'история игр'
	},
	lastGames: {
		en: 'last games',
		de: 'letzte spiele',
		ru: 'последние игры'
	},
	picture: {
		en: 'picture',
		de: 'bild',
		ru: 'фото'
	},
	saveChanges: {
		en: 'save changes',
		de: 'änderungen speichern',
		ru: 'сохранить изменения'
	},
	cancel: {
		en: 'cancel',
		de: 'stornieren',
		ru: 'отмена'
	},
	friendsListEmpty: {
		en: 'friends list is empty',
		de: 'freundesliste ist leer',
		ru: 'список друзей пуст'
	},
	addFriend: {
		en: 'add friend',
		de: 'freund hinzufügen',
		ru: 'добавить друга'
	},
	add: {
		en: 'add',
		de: 'hinzufügen',
		ru: 'добавить'
	}
}

const errors =	 {
	usernameEmpty: {
		en: 'username is empty',
		de: 'username ist leer',
		ru: 'имя пользователя пустое'
	},
	emailEmpty: {
		en: 'email is empty',
		de: 'email ist leer',
		ru: 'эпочта пустая'
	},
	emailInvalid: {
		en: 'email is invalid',
		de: 'email ist ungültig',
		ru: 'эпочта неверна'
	},
	passwordEmpty: {
		en: 'password is empty',
		de: 'passwort ist leer',
		ru: 'пароль пустой'
	},
	passwordsDontMatch: {
		en: 'passwords don\'t match',
		de: 'passwörter stimmen nicht überein',
		ru: 'пароли не совпадают'
	},
}

export const getText = (text, lang) => {
	return texts[text][lang]
}

export const getError = (error, lang) => {
	return errors[error][lang]
}