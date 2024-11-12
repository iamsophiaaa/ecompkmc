from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Product
from .forms import AddProduct

def search(request):
    query = request.GET.get('query', '').lower()  # Get the search query from the URL
    products = Product.objects.all()  # Get all products
    
    if query:
        # Preprocess product descriptions and names (convert to lowercase and strip whitespace)
        product_texts = [f"{product.name} {product.description}".lower().strip() for product in products]
        
        # Print product texts and the query to make sure they are correct
        print("Product texts:", product_texts)
        print("Search Query:", query)
        
        # Add the query to the list of texts
        texts = product_texts + [query.lower()]
        
        # Initialize the TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')  # Remove common English stopwords
        
        # Transform the product texts and the query into TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Print the TF-IDF matrix to inspect the vectorization process
        print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
        print("TF-IDF Matrix:", tfidf_matrix.toarray())
        
        # The last row of the tfidf_matrix will represent the query's vector
        query_vector = tfidf_matrix[-1]
        
        # Calculate cosine similarities between the query and all product vectors
        similarities = cosine_similarity(query_vector, tfidf_matrix[:-1])  # Exclude the query itself
        
        # Print similarity values for debugging
        print("Cosine Similarities:", similarities)
        
        # Get the product indices sorted by similarity (highest to lowest)
        sorted_indices = similarities.argsort()[0][::-1]
        
        # Filter out products with very low similarity (e.g., below 0.1)
        threshold = 0.1
        sorted_products = [products[int(i)] for i in sorted_indices if similarities[0][i] > threshold]
        
        # Return the sorted products with query to the template
        return render(request, 'product/search_results.html', {'results': sorted_products, 'query': query})
    
    else:
        return render(request, 'product/search_results.html', {'results': [], 'query': query})



def add_product(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Or redirect to the login page if the user is not authenticated

    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            # Save the product with the logged-in user as the seller
            form.save(user=request.user)
            return redirect('core:product_list') 
        
        else:
            print(form.errors) # Redirect to the list of products (or any other page you choose)
    else:
        form = AddProduct()

    context = {
        'form': form
    }

    return render(request, 'product/add_product.html', context)



def edit_product(request, product_id):
    # Get the product to edit
    product = get_object_or_404(Product, id=product_id)
    
    # Check if it's a POST request to handle form submission
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            # Save the updated product
            form.save()
            # Redirect to a success page or product list
            return redirect('core:product_list')  # Replace with the correct redirect URL
    else:
        # GET request, initialize form with existing product data
        form = AddProduct(instance=product)
    
    # Render the form and pass the form object to the template
    return render(request, 'product/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('core:product_list')  # Redirect back to the list page after deletion

    return render(request, 'product/delete_product.html', {'product': product})
