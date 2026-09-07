# BrewMatch ☕︎

BrewMatch is a full-stack coffee recommendation app that matches users to drinks through a randomized personality quiz, then uses their coffee journal and ratings to personalize future suggestions. Users can register/login, take the quiz, save and rate drinks, track them on a calendar, view streaks and stats, and receive both a familiar recommendation and a “Try Something New” suggestion based on their taste history.

This application includes:
- User Registration and JWT Authentication
- Randomized 15-Question Personality Quiz
- Personalized Coffee Recommendation Engines
- Coffee Journal with Ratings, Notes, Calendar, and Streaks
- PostgreSQL Persistence with SQLAlchemy ORM
- Protected REST API Routes with FastAPI
- Responsive UI with React and Tailwind CSS
- Automated Testing with pytest, Vitest, and React Testing Library
- **CI/CD Pipeline with GitHub Actions**
- **Automated Deployment to Vercel and Render**

The frontend is built with **Next.js, React, TypeScript, and Tailwind CSS**, while the backend uses **FastAPI, Python, SQLAlchemy, Pydantic, and PostgreSQL**.

The recommendation system is content-based rather than fully ML-driven. It derives preferences such as temperature, sweetness, strength, milkiness, and flavors from past ratings, then scores drink combinations accordingly. “What You Might Like” follows known preferences, while “Try Something New” excludes previously logged combinations while still staying close to the user’s taste. Ollama is used only for optional personalized recommendation copy, with deterministic fallback logic if the model is unavailable.


**Demo account:** `johndoe@gmail.com` / `123456`
