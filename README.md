# ft_transcendence

Welcome to **ft_transcendence**! This repository houses the source code for our exciting multiplayer online gaming platform, as part of the final 42 school project. 
Players can engage in various competitive games, and tournaments, all within a seamless web environment.

## Features

- **User Authentication**: Secure authentication system using Django's built-in authentication modules.
- **Gameplay**: Play real-time games with friends and other players in a competitive environment.
- **Tournaments**: Join tournaments, compete for prizes, and climb the leaderboard.
- **Social Features**: Interact with other players through chat, friend requests, and in-game messaging.
- **Admin Dashboard**: Manage users, games, tournaments, and overall platform settings efficiently.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: Vue.js, Nginx, Bootstrap
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git, GitHub

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ft_transcendence.git
   cd ft_transcendence
   ```

2. **Set up the environment**:
   ```bash
   # Backend setup
   cd backend
   cp .env.example .env  # Configure your environment variables
   docker-compose up --build

   # Frontend setup
   cd ../frontend
   npm install
   npm run build
   ```

3. **Access the application**:
   Open your browser and go to `http://localhost:8000` to view the application.

## Contributing

We welcome contributions to **ft_transcendence**! To contribute:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -am 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## Authors

- **lhasmi** - [Your GitHub Profile](https://github.com/lhasmi)

See also the list of [contributors](https://github.com/lhasmi/ft_transcendence/contributors) who participated in this project.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Hat tip to @dcharala and @sbhatta
