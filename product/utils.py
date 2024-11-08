from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.models import Product
from django.shortcuts import render

def search(request):
    query = request.GET.get('query', '').lower()  # Get the search query and convert to lowercase
    products = Product.objects.all()  # Get all products from the database

    # Step 1: Ensure the query is not empty
    if query:
        # Step 2: Collect product descriptions and names
        product_texts = [f"{product.name} {product.description}".lower() for product in products]
        
        # Debug: Print the product texts and the search query
        print("Product texts:", product_texts)
        print("Search Query:", query)
        
        # Add the query to the list of texts (product descriptions + query)
        texts = product_texts + [query]
        
        # Step 3: Initialize TF-IDF Vectorizer
        vectorizer = TfidfVectorizer(stop_words=None)  # Disable stop words to prevent removing "java"
        
        # Step 4: Transform product texts and query into TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Debug: Print the shape of the TF-IDF matrix to check if it is correctly populated
        print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
        print("TF-IDF Matrix (first 5 rows):", tfidf_matrix.toarray()[:5])  # Display first 5 rows for inspection
        
        # Step 5: Extract the query's vector (last row of the matrix)
        query_vector = tfidf_matrix[-1]
        
        # Step 6: Calculate cosine similarities between the query and all product vectors
        similarities = cosine_similarity(query_vector, tfidf_matrix[:-1])  # Exclude the query from comparison
        
        # Debug: Print the cosine similarities to inspect the results
        print("Cosine Similarities:", similarities)
        
        # Step 7: Get the product indices sorted by similarity (highest to lowest)
        sorted_indices = similarities.argsort()[0][::-1]
        
        # Debug: Print the sorted indices to verify the order
        print("Sorted Indices:", sorted_indices)
        
        # Step 8: Get the sorted products based on similarity
        sorted_products = [products[int(i)] for i in sorted_indices]
        
        return render(request, 'product/search_results.html', {'results': sorted_products, 'query': query})
    else:
        # If no query is provided, return empty results
        return render(request, 'product/search_results.html', {'results': [], 'query': query})
