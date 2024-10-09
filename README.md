# CRUD api using fastapi, sqlalchemy, and postgres

#### CRUD endpoints for the following tables:
1. users
    - first_name (str)
    - last_name (str)
    - email (str)
    - minimun_fee (int)

2. films
   - title (str)
   - description (str)
   - budget (int)
   - release_year (int)
   - genres (list[str])
   - companies

3. companies 
   - name (str)
   - contact_email_address (str)
   - phone_number (str)
   

#### Implement the following relationships / join tables
- users and films have a many-to-many relationship where the role of the user can be either “writer”, “producer”, or “director”
- users and companies have a many-to-many relationship where the role is “owner” or “member”
- companies and films have a one-to-many relationship
- implement CRU (create, read, and update only) for the user’s role’s with films and user’s role’s companies