# Motorcycle Events Manager

**Motorcycle Events Manager** is a modern web app designed to coordinate events for a community of motorcyclists.
Developed in Python with Django and enriched with Bootstrap for the front-end, the app uses PostgreSQL as a relational database.
The deployment is managed on Railway, while Cloudinary takes care of hosting and media management.

---

## Architecture and technologies

The app is based on an MVC architecture: Django governs the business logic and interactions with the PostgreSQL database,
while Bootstrap 5 guarantees a responsive interface accessible from desktop and mobile. Railway ensures continuous deployment,
with integrated rollback and monitoring, and Cloudinary allows fast and secure uploads of event images.

---

## Features overview

Each section of the app is designed to offer a simple and immediate experience:

- **Home page**: a hero section introduces the project with title, slogan and calls to action; immediately below,
the next three events in the calendar and the most popular ones for registrations.
- **Event calendar**: a list view with filters by category (motorcycle rallies, motorcycle tours, food and wine tours, track days)
and by registration status (open, closed, not yet open, cancelled). It is possible to define a date range
and sort the events by date or number of participants.
- **Event card**: each event has a title, extended description, date/time, starting location (with link to Google Maps),
cover image and, if available, the GPS track. Registrations are activated and closed according to a pre-established
calendar, and the organizer can cancel the event at any time.
- **Registration management**: only authenticated users can register; the profile requires the mandatory
entry of the motorbike and allows you to indicate the number of companions.
- **User profile**: summary of personal data, motorcycle and events registered for, with easy access
to modify your details.

---

## User flow

1. **Registration/Login**: the user creates an account by providing email and password, or logs in if already registered.
2. **Profile configuration**: mandatory entry of motorcycle data (brand, model, engine capacity).
3. **Event discovery**: navigation in the calendar or search using filters to find the event of interest.
4. **Registration**: choice of event, entry of the number of participants and confirmation of registration in the expected period.

---

> 🌐 Try the application now on Railway:
> https://web-production-dac68.up.railway.app/

---

## Project files

Use this link to get the source files, with the populated database and some configurations.
> [Motorcycle event manager - source file](https://github.com/Leonardo-Davio/EventManagerWebApp/releases/tag/RawSource)

--- 

## DISCLAIMER

This site was created exclusively for academic purposes as part of the university project relating to the Multimedia Design and Production course at the University of Florence. The information provided here is purely indicative and does not in any way bind the University Bodies; therefore, no responsibility is assumed for the use that will be made of it.

For any clarification or further information, you can contact the project manager at leonardo.davio@edu.unifi.it.
