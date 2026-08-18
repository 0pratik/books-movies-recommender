# Books & Movies Recommender System

## Overview

A hybrid recommendation system that recommends **books and movies** using multiple recommendation techniques. The project includes separate recommendation systems for books and movies, along with a **Streamlit application called SynergyReco** that brings the recommendation experience together.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Jupyter Notebook

## Recommendation Techniques

### Books Recommendation

The book recommendation system uses:

- Popularity-based recommendation
- Collaborative filtering
- User-item rating data
- Book information and ratings

### Movies Recommendation

The movie recommendation system uses **content-based filtering** with:

- CountVectorizer
- Cosine Similarity
- Movie metadata

## SynergyReco

**SynergyReco** is the Streamlit application included in this project. It provides an interactive interface for exploring recommendations across the book and movie recommendation systems.

Application code:

```text
App/
└── synergyreco.py
```

## Project Structure

```text
books-movies-recommender/
│
├── App/
│   └── synergyreco.py
│
├── Dataset and notebook/
│   ├── Books_recommender_System/
│   │   ├── Dataset/
│   │   │   ├── Books.csv
│   │   │   ├── Ratings.csv
│   │   │   └── Users.csv
│   │   └── NoteBook/
│   │       └── Books_recommender_system.ipynb
│   │
│   └── Movie_recommender_System/
│       ├── Dataset/
│       │   ├── tmdb_5000_credits.csv
│       │   └── tmdb_5000_movies.csv
│       └── NoteBook/
│           └── Movie Recommender System .ipynb
│
└── README.md
```

## Key Features

- Book recommendation system
- Movie recommendation system
- Multiple recommendation techniques
- Content-based movie recommendations
- Cosine similarity
- Interactive Streamlit application
- Separate notebooks for books and movies

## How It Works

The project preprocesses and analyzes the book and movie datasets.

For movies, **CountVectorizer** converts relevant textual information into numerical features, and **cosine similarity** identifies similar movies.

For books, user ratings and book information are used to generate recommendations.

The **SynergyReco Streamlit application** provides an interactive interface for using the recommendation systems.

## Author

**Pratik Kale**
