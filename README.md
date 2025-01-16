# Household Services Application

## Project Overview

The **Household Services Application** is a platform designed to connect customers with service professionals for various household services such as plumbing, electrical repairs, and AC maintenance. The application features three user roles:

- **Customers**: Can register, log in, and request household services.
- **Service Professionals**: Manage service requests assigned to them and update their statuses.
- **Admin**: Oversees user activities, manages service requests, and ensures proper system operation.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Future Improvements](#future-improvements)
- [Project Video](#project-video)

## Features

- **Role-based Authentication**: Secure login and registration for customers, service professionals, and admins.
- **Service Request System**: Customers can request services, and service professionals can manage and update service request statuses.
- **Admin Dashboard**: Admin can manage users, view service requests, and monitor system activities.
- **Responsive UI**: The frontend is designed using Bootstrap with a modern dark theme for a clean, user-friendly interface.

## Technologies Used

- **Backend**: Flask, SQLite, Flask-Login
- **Frontend**: Bootstrap, Jinja2 (for templating)
- **Database**: SQLite
- **Other Libraries**: Flask-WTF (for form handling)

## Installation Instructions

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/venkatesh-am/household-services.git
   cd household-services
   ```

2. Navigate to the `code` directory:

   ```bash
   cd code
   ```

3. **Set up the virtual environment**:
   - Create a virtual environment:

     ```bash
     python -m venv venv
     ```

   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

4. Install the required Python packages:

   ```bash
   python -m pip install -r requirements.txt --timeout 100 --no-cache-dir
   ```

5. **Configure the Database URI**:
   - Open the `app.py` file located in the `code` directory.
   - Find the line where the database URI is set (it will look something like this):
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
     ```
   - Update the path to point to your local database file. For example, if your database is located at `/path/to/your/database.db`, change the line to:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////path/to/your/database.db'
     ```

6. Set up the SQLite database by running the following:

   ```bash
   flask db upgrade
   ```

7. Run the application locally:

   ```bash
   python app.py
   ```

   The application will be available at `http://127.0.0.1:5000/`.

## Database Schema

The database is structured using the following relational tables:

- **Users**: Contains `id`, `username`, `password`, and `role` to distinguish between customers, service professionals, and admins.
- **Services**: Contains `service_id`, `name`, `payment`, and `description` for each service.
- **Service Requests**: Tracks requests with `request_id`, `service_id`, `customer_id`, `professional_id`, `status`, and `remarks`.
- **Professionals**: Contains `professional_id`, `expertise`, and `profile_verified` status for each service professional.

## Testing

The application has been tested locally to ensure the proper functioning of the following:

- User registration and login
- Service request creation and status updates
- Role-specific dashboards for customers, service professionals, and admins

## Future Improvements

- **Data Analytics**: Implement data analytics to track service usage trends and user satisfaction.
- **Service Feedback**: Allow customers to leave feedback on completed services to improve the platform’s user engagement.

## Project Video

You can view the demo video for the project here:  
[Project Video](https://drive.google.com/file/d/18Q6SNa8OYoORR17uXiMwDLwbtU3OMwE1/view?usp=sharing)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to customize it further if needed!
```
