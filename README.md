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
git clone https://github.com/ngocdangnguyenn/auctiontech.git
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

## Contact
- **Email**: [nndnguyen2016@gmail.com](mailto:nndnguyen2016@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/ngocdangnguyenn](https://www.linkedin.com/in/ngocdangnguyenn)
- **Portfolio:** [https://portfolio-qyyg.onrender.com](https://portfolio-qyyg.onrender.com)

---
I welcome feedback and suggestions for improvement. Thank you for visiting AuctionTech!

## License
This project is licensed under the MIT License. See the LICENSE file for details.
