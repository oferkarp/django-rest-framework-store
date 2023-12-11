# *******************************
# ** Django REST Framework Store **
# *******************************

# API Endpoints:

Welcome Page (welcome_page): Provides an overview of available API endpoints.

you can visit here to see the web:
-https://django-rest-framework-store.onrender.com

1.Product Operations:

2.Products (products):
   Retrieves products based on search, max price, and category.
   Allows addition of new products.

3.Category Retrieval (get_unique_categories): Fetches unique categories of products available.

4.Product Detail (product_detail): Manages individual product operations like retrieval, update, and deletion.

Order Operations:

5.Orders (orders): Fetches and creates orders (currently not in use).

Cart Operations:

6.Cart Items (cart_items):
  Manages cart items: retrieving all items.

7.User Cart Items (user_cart_items):
  Retrieves cart items by user.
  Allows addition of new items to the cart.

User Operations:

8.Get Username by ID (get_username_by_id): Retrieves user details by ID.

9.User Registration (user_registration): Registers new users.

Cart Management:

10.Delete Cart Item (delete_cart_item): Deletes items from a user's cart.

11.Checkout View (checkout_view):
  Handles the checkout process, creating orders from cart items.

12.Clear Cart (clear_cart): Clears the cart for a specific user.

User Order History:

13.User Orders (user_orders): Retrieves orders placed by a specific user.
