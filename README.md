# SecWebPage

## Description

SecWebPage is a user management web application built with Flask and MySQL. It allows users to register, log in, and manage their roles (User/Admin) while ensuring secure authentication and spam prevention through Google reCAPTCHA.

## Features

- User registration with role selection
- Secure login with password hashing
- Role-based access control
- Session management using Flask sessions
- Google reCAPTCHA for enhanced security

## Technologies Used

- **Backend**: Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS
- **Security**: bcrypt for password hashing, Google reCAPTCHA

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/secwebpage.git
   cd secwebpage
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MySQL:
   - Create a database named `secwebpage` and a `users` table.

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at `http://localhost:5000`.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
