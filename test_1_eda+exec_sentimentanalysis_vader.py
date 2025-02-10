# -*- coding: utf-8 -*-

import pandas as pd
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
sns.set(color_codes=True)
import re
!pip install emoji
import emoji
!pip install nltk
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

df = pd.read_csv("VideoComments.csv")

# Filas superiores
df.head(5)

# Filas inferiores
df.tail(5)
df.shape

# Comprobar tipo de datos del dataset

df.dtypes

# Dimensiones del dataset
df.shape

# Eliminar filas duplicadas
duplicate_rows_df = df[df.duplicated()]
print("number of duplicate rows: ", duplicate_rows_df.shape)

# Contar filas
df.count()

# Eliminar duplicados y mostrar primeras filas de nuevo
df = df.drop_duplicates()
df.head(5)

# Contar filas de nuevo
df.count()

# Posible codigo para eliminacion de nulos (no necesario en este caso)
print(df.isnull().sum())

# Si fuera necesario suprimir nulos hariamos lo siguiente
df = df.dropna()    # Dropping the missing values.
df.count()
print(df.isnull().sum())

# Instalacion de modulo de traduccion de Google para comprobar el rendimiento
!pip install googletrans==4.0.0-rc1
from googletrans import Translator
translator = Translator()

def translate_to_english(comment):
    return translator.translate(comment, src='es', dest='en').text

# DataFrame es df y tiene una columna 'Comentario'
df['Comentario_Traducido'] = df['Comentario'].apply(translate_to_english)

# Compilar el patron de hyperlinks
hyperlink_pattern = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

# Umbral para la proporcion de texto/emojis
threshold_ratio = 0.65

# Lista para comentarios relevantes
relevant_comments = []

# Iterar sobre la columna 'Comentario'
for comment_text in df['Comentario_Traducido']:
    comment_text = comment_text.lower().strip()

    # Contar emojis en el comentario
    emojis = emoji.emoji_count(comment_text)

    # Contar caracteres de texto (excluyendo espacios)
    text_characters = len(re.sub(r'\s', '', comment_text))

    # Condiciones para agregar comentarios relevantes
    if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
        if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
            relevant_comments.append(comment_text)

# Imprimir los primeros 5 comentarios relevantes
print(relevant_comments[:100])

def sentiment_scores(comment, polarity):

    # Creating a SentimentIntensityAnalyzer object.
    sentiment_object = SentimentIntensityAnalyzer()

    sentiment_dict = sentiment_object.polarity_scores(comment)
    polarity.append(sentiment_dict['compound'])

    return polarity

polarity = []
positive_comments = []
negative_comments = []
neutral_comments = []

f = open("VideoComments.csv", 'r', encoding='utf-8')
comments = f.readlines()
f.close()
print("Analysing Comments...")
for index, items in enumerate(comments):
    polarity = sentiment_scores(items, polarity)

    if polarity[-1] > 0.05:
        positive_comments.append(items)
    elif polarity[-1] < -0.05:
        negative_comments.append(items)
    else:
        neutral_comments.append(items)

# Print polarity
polarity[:5]

avg_polarity = sum(polarity)/len(polarity)
print("Average Polarity:", avg_polarity)
if avg_polarity > 0.05:
    print("The Video has got a Positive response")
elif avg_polarity < -0.05:
    print("The Video has got a Negative response")
else:
    print("The Video has got a Neutral response")

print("The comment with most positive sentiment:", comments[polarity.index(max(
    polarity))], "with score", max(polarity), "and length", len(comments[polarity.index(max(polarity))]))
print("The comment with most negative sentiment:", comments[polarity.index(min(
    polarity))], "with score", min(polarity), "and length", len(comments[polarity.index(min(polarity))]))

positive_count = len(positive_comments)
negative_count = len(negative_comments)
neutral_count = len(neutral_comments)

# labels and data for Bar chart
labels = ['Positive', 'Negative', 'Neutral']
comment_counts = [positive_count, negative_count, neutral_count]

# Creating bar chart
plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])

# Adding labels and title to the plot
plt.xlabel('Sentiment')
plt.ylabel('Comment Count')
plt.title('Sentiment Analysis of Comments')

# Displaying the chart
plt.show()

"""También podemos trazar un gráfico circular para el mismo gráfico usando el siguiente código en el que primero configuramos el tamaño de la figura usando la función figure() y el parámetro figsize que establece las dimensiones en pulgadas, configurándolo como 10 pulgadas de ancho y 6 pulgadas de alto.
Luego, utilizando la función pie(), trazamos un gráfico circular usando el recuento de comentarios y etiquetas respectivos como parámetros.
"""

# labels and data for Bar chart
labels = ['Positive', 'Negative', 'Neutral']
comment_counts = [positive_count, negative_count, neutral_count]

plt.figure(figsize=(10, 6)) # setting size

# plotting pie chart
plt.pie(comment_counts, labels=labels)

# Displaying Pie Chart
plt.show()

import pandas as pd
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Leer datos desde un archivo CSV en un DataFrame
df = pd.read_csv("VideoComments.csv", encoding='utf-8')

# Crear objeto de analisis de sentimientos
sentiment_object = SentimentIntensityAnalyzer()

# Funcion para calcular la polaridad de un comentario
def sentiment_scores(comment):
    sentiment_dict = sentiment_object.polarity_scores(comment)
    return sentiment_dict['compound']

# Agregar una nueva columna con la polaridad
df['Polarity'] = df['Comentario'].apply(sentiment_scores)

# Clasificar comentarios por polaridad
df['Sentiment'] = df['Polarity'].apply(lambda x: 'Positive' if x > 0.05 else 'Negative' if x < -0.05 else 'Neutral')

# Agrupar por VideoId y contar comentarios por polaridad
grouped_sentiments = df.groupby(['VideoID', 'Sentiment']).size().unstack(fill_value=0)

# Mostrar los primeros resultados
print(grouped_sentiments)

# Generar un grafico para cada VideoId
for video_id, group in grouped_sentiments.iterrows():
    labels = group.index
    counts = group.values

    # Crear grafico de barras
    plt.bar(labels, counts, color=['blue', 'red', 'grey'])

    # Configurar etiquetas y titulo
    plt.xlabel('Sentiment')
    plt.ylabel('Comment Count')
    plt.title(f'Sentiment Analysis for VideoId: {video_id}')

    # Mostrar grafico
    plt.show()

!pip install textblob

from textblob import TextBlob
import pandas as pd

# Leer datos desde un archivo CSV en un DataFrame
df = pd.read_csv("VideoComments.csv", encoding='utf-8')

# Funcion para calcular la polaridad de un comentario
def sentiment_scores(comment):
    sentiment = TextBlob(comment).sentiment.polarity
    return sentiment

# Agregar una nueva columna con la polaridad
df['Polarity'] = df['Comentario'].apply(sentiment_scores)

# Clasificar comentarios por polaridad
df['Sentiment'] = df['Polarity'].apply(lambda x: 'Positive' if x > 0.05 else 'Negative' if x < -0.05 else 'Neutral')

# Agrupar por VideoId y contar comentarios por polaridad
grouped_sentiments = df.groupby(['VideoID', 'Sentiment']).size().unstack(fill_value=0)

# Resetear el indice para mostrar en formato tabular
result_table = grouped_sentiments.reset_index()

# Mostrar la tabla
print("Resultados de análisis de sentimiento por VideoId:")
print(result_table)

# Guardar la tabla en un archivo CSV
result_table.to_csv("SentimentAnalysisResults.csv", index=False)
