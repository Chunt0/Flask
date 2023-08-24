1. **User Accesses Sign-Up Page (`/signup`):**
   - User navigates to `/signup`.
   - Flask routes to `signup` in `auth.py`.

2. **Sign-Up Form Displayed:**
   - Instantiate `RegistrationForm`.
   - Render and show `signup.html`.
   - User submits username and password.

3. **Form Submission - Validation:**
   - Validate form data.
   - If valid, proceed.

4. **User Account Creation:**
   - Hash password with `generate_password_hash`.
   - Create `User` object with username, hashed password.
   - Add to session, commit to database.

5. **Account Created Flash Message:**
   - Generate flash message.
   - Redirect to login page.

6. **User Accesses Login Page (`/login`):**
   - User navigates to `/login`.
   - Flask routes to `login` in `auth.py`.

7. **Login Form Displayed:**
   - Instantiate `LoginForm`.
   - Render and show `login.html`.
   - User submits username and password.

8. **Form Submission - Validation:**
   - Validate form data.
   - If valid, proceed.

9. **User Authentication:**
   - Query user by username.
   - If user exists, check password match.

10. **User Logged In:**
   - Call `login_user`.
   - Redirect to dashboard.

11. **Incorrect Login Attempt:**
   - Generate flash message on incorrect login.

12. **User Logs Out (`/logout`):**
   - Click "Log Out".
   - Flask routes to `logout` in `auth.py`.
   - Call `logout_user`.
   - Redirect to main page.
