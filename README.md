# 🎬 Hollywood Movie Recommendation System

## 📌 About the Project

The **Hollywood Movie Recommendation System** is a machine learning project designed to help users discover movies based on their interests. It recommends the **top 5 movies related to a user's selected movie**, making it easier to explore similar movies without manually searching through a large collection.

The system uses movie data and a precomputed similarity matrix to identify movies that are most similar to the selected movie. It provides a simple and user-friendly way to discover new movies based on existing preferences.

## ✨ Features

- **Movie Recommendations:** Suggests the top 5 movies related to the selected movie.
- **Similarity-Based Matching:** Uses precomputed movie similarity scores to identify related movies.
- **Interactive Interface:** Provides a simple interface for users to search for movies and view recommendations.
- **Machine Learning Approach:** Applies data processing and similarity-based recommendation techniques.
- **Easy to Use:** Helps users discover movies with just a few clicks.

## 🛠️ Technologies Used

- **Python** – Core programming language.
- **Pandas** – Data manipulation and preprocessing.
- **NumPy** – Numerical computations.
- **Scikit-learn** – Machine learning and similarity calculations.
- **Streamlit** – Web application interface.
- **Jupyter Notebook** – Data analysis, experimentation, and model development.
- **Pickle** – Storage and loading of preprocessed movie data and similarity results.

## ⚙️ How It Works

1. The system loads the preprocessed movie dataset.
2. The user selects a movie from the available collection.
3. The system retrieves similarity scores for the selected movie.
4. Movies are ranked according to their similarity scores.
5. The top 5 related movies are displayed to the user.

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Sanskar-Thorat25/Hollywood-Movie-Recommendation-System.git
```

### 2. Navigate to the Project Directory

```bash
cd Hollywood-Movie-Recommendation-System
```

### 3. Install Dependencies

Make sure Python is installed, then run:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, where you can select a movie and explore recommendations.

**Note:** The application requires its model and preprocessed data files to be available in the expected locations.

## 📂 Project Structure

```text
Hollywood-Movie-Recommendation-System/
│
├── app.py
├── Movie Recommendation System.ipynb
├── movies_dict.pkl
├── similarity.pkl
├── requirements.txt
└── README.md
```

## 🎯 Project Objective

The main objective of this project is to build a movie recommendation application that simplifies movie discovery through similarity-based recommendations. It demonstrates how Python, machine learning techniques, and a web interface can be combined to create a practical recommendation system.

## 🔮 Future Improvements

- Display movie posters and additional movie details.
- Add movie genres, ratings, and release-year filters.
- Improve recommendation quality using additional movie features.
- Deploy the application online for easy access.
- Expand the dataset to include more movies.

## 👨‍💻 Author

**Sanskar Thorat**

GitHub: [Sanskar-Thorat25](https://github.com/Sanskar-Thorat25)

---

⭐ If you find this project useful, consider giving the repository a star!

