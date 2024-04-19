const translations = {
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
	}
}

export const getText = (text, lang) => {
	return translations[text][lang]
}