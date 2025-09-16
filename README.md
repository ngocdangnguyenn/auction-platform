# AuctionTech – Centime Auction Platform

## Overview
AuctionTech is a web application for online auctions, where users bid for high-tech products by proposing prices down to the cent. The winner is the user who offers the lowest unique bid. Originally developed as a graded university project, this repo now serves as a showcase of practical software engineering and data skills for internships and graduate studies.

## Key Features
- Modular backend (Flask, SQLAlchemy, app factory, blueprints)
- Secure authentication & role-based access (client/admin)
- Token-based bidding system
- Real-time auction logic (lowest unique bid, automatic refunds)
- Admin dashboard (manage products, auctions, users, token packs)
- Client dashboard (bidding, account management, notifications)
- Responsive frontend (Bootstrap, custom CSS, interactive JS)
- Dockerized for reproducibility & deployment
- Automated testing (pytest), code quality (flake8, black, isort, pre-commit)
- Environment-based configuration for security

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, Flask-Migrate
- **Frontend:** Bootstrap, custom CSS/JS
- **Database:** MySQL (via docker-compose)
- **DevOps:** Docker, docker-compose
- **Testing/Quality:** pytest, flake8, black, isort, pre-commit

## Quickstart
```bash
git clone https://github.com/ngocdangnguyen-ng/auctiontech.git
cd auctiontech
pip install -r requirements.txt
# Or with Docker
# docker-compose up --build
```
1. Copy `.env.example` to `.env` and fill in your secrets and database URI.
2. Start the app:
   ```bash
   flask run
   ```
3. Or use Docker:
   ```bash
   docker-compose up --build
   ```

## Data Modeling & Business Logic
- **Schema:** User token balances, auctions, bids, products, token packs
- **Logic:** Bids are placed with tokens; winner is lowest unique bid; refunds if no winner
- **Consistency:** All transactions and refunds handled atomically
- **Extensible:** Schema and logic designed for future analytics, reporting, or AI integration

## Testing & Reproducibility
- **Testing:** Automated tests for business logic and endpoints (pytest)
- **Code Quality:** Linting, formatting, pre-commit hooks
- **Docker:** Reproducible environment for development, testing, and deployment

## Relevance for AI/Data/Software Engineering
This project demonstrates:
- **Data modeling:** Designing schemas for transactional systems (tokens, auctions, bids)
- **Business logic:** Implementing complex rules (lowest unique bid, refunds, role-based access)
- **Testing & reproducibility:** Practices essential for reliable software and research pipelines
- **Code organization:** Modular, maintainable codebase (transferable to ML/AI projects)
- **DevOps:** Dockerized setup, environment management, CI-ready structure

> These skills are directly transferable to AI/data science: handling data consistency, reproducibility, and scalable code organization are critical for ML pipelines and research.

## Contact
- **Email**: [nndnguyen2016@gmail.com](mailto:nndnguyen2016@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/ngocnguyen-fr](https://www.linkedin.com/in/ngocnguyen-fr)
- **Portfolio:** [https://portfolio-qyyg.onrender.com](https://portfolio-qyyg.onrender.com)

---
I welcome feedback and suggestions for improvement. Thank you for visiting AuctionTech!

## License
This project is licensed under the MIT License. See the LICENSE file for details.
