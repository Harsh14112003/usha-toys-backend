from database import get_db

def seed_data():
    db = get_db()
    
    # Categories
    categories = [
        {"name": "Educational Toys", "icon": "🎓", "count": 24},
        {"name": "Action Figures", "icon": "🦸", "count": 18},
        {"name": "Dolls", "icon": "🎎", "count": 15},
        {"name": "Remote Cars", "icon": "🏎️", "count": 12},
        {"name": "Board Games", "icon": "🎲", "count": 20},
        {"name": "Baby Toys", "icon": "🧸", "count": 16},
    ]
    
    # Products
    products = [
        {
            "name": "Rainbow Stacking Rings",
            "description": "Colorful stacking rings that help develop motor skills and color recognition. Made from safe, non-toxic materials perfect for little hands.",
            "price": 499,
            "originalPrice": 699,
            "category": "baby-toys",
            "ageGroup": "0-2",
            "image": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=600&h=600&fit=crop",
                "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=600&h=600&fit=crop",
            ],
            "rating": 4.8,
            "reviewCount": 124,
            "inStock": True,
            "featured": True,
            "badge": "Best Seller",
        },
        {
            "name": "Wooden Building Blocks Set",
            "description": "50-piece wooden building blocks in various shapes and colors. Sparks creativity and spatial awareness in young minds.",
            "price": 899,
            "originalPrice": 1199,
            "category": "educational",
            "ageGroup": "3-5",
            "image": "https://images.unsplash.com/photo-1587654780291-39c9404d7dd0?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1587654780291-39c9404d7dd0?w=600&h=600&fit=crop",
            ],
            "rating": 4.6,
            "reviewCount": 89,
            "inStock": True,
            "featured": True,
            "badge": "Sale",
        },
        {
            "name": "Superhero Action Figure Set",
            "description": "Set of 4 poseable superhero action figures with accessories. Durable and perfect for imaginative play.",
            "price": 1299,
            "category": "action-figures",
            "ageGroup": "6-8",
            "image": "https://images.unsplash.com/photo-1608889825205-eebdb9fc5806?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1608889825205-eebdb9fc5806?w=600&h=600&fit=crop",
            ],
            "rating": 4.5,
            "reviewCount": 67,
            "inStock": True,
            "featured": True,
        },
        {
            "name": "Princess Fashion Doll",
            "description": "Beautiful fashion doll with 3 outfit changes and styling accessories. Hours of dress-up fun!",
            "price": 799,
            "originalPrice": 999,
            "category": "dolls",
            "ageGroup": "3-5",
            "image": "https://images.unsplash.com/photo-1613682988402-a12a3e551090?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1613682988402-a12a3e551090?w=600&h=600&fit=crop",
            ],
            "rating": 4.7,
            "reviewCount": 156,
            "inStock": True,
            "featured": True,
            "badge": "Popular",
        },
        {
            "name": "RC Monster Truck",
            "description": "High-speed remote control monster truck with all-terrain wheels. Includes rechargeable battery and charger.",
            "price": 1999,
            "originalPrice": 2499,
            "category": "remote-cars",
            "ageGroup": "6-8",
            "image": "https://images.unsplash.com/photo-1581235707960-35f13de9834b?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1581235707960-35f13de9834b?w=600&h=600&fit=crop",
            ],
            "rating": 4.4,
            "reviewCount": 43,
            "inStock": True,
            "featured": True,
            "badge": "New",
        },
        {
            "name": "Family Strategy Board Game",
            "description": "Exciting strategy board game for the whole family. 2-6 players, ages 8+. Hours of fun guaranteed!",
            "price": 649,
            "category": "board-games",
            "ageGroup": "8+",
            "image": "https://images.unsplash.com/photo-1611371805429-8b5c1b2c34ba?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1611371805429-8b5c1b2c34ba?w=600&h=600&fit=crop",
            ],
            "rating": 4.9,
            "reviewCount": 201,
            "inStock": True,
            "featured": True,
            "badge": "Top Rated",
        },
        {
            "name": "Musical Learning Tablet",
            "description": "Interactive learning tablet with songs, letters, and numbers. Perfect for early education with bright colors and sounds.",
            "price": 1499,
            "category": "educational",
            "ageGroup": "3-5",
            "image": "https://images.unsplash.com/photo-1560472355-536de3962603?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1560472355-536de3962603?w=600&h=600&fit=crop",
            ],
            "rating": 4.3,
            "reviewCount": 78,
            "inStock": True,
            "featured": False,
        },
        {
            "name": "Soft Plush Teddy Bear",
            "description": "Ultra-soft plush teddy bear, 18 inches tall. Hypoallergenic and machine washable. A perfect cuddly companion.",
            "price": 599,
            "category": "baby-toys",
            "ageGroup": "0-2",
            "image": "https://images.unsplash.com/photo-1559715541-5daf8a0296d0?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1559715541-5daf8a0296d0?w=600&h=600&fit=crop",
            ],
            "rating": 4.8,
            "reviewCount": 312,
            "inStock": True,
            "featured": False,
        },
        {
            "name": "Dinosaur Adventure Set",
            "description": "12-piece dinosaur figurine set with a play mat featuring a prehistoric landscape. Educational and fun!",
            "price": 1099,
            "originalPrice": 1399,
            "category": "action-figures",
            "ageGroup": "3-5",
            "image": "https://images.unsplash.com/photo-1535572290543-960a8046f5af?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1535572290543-960a8046f5af?w=600&h=600&fit=crop",
            ],
            "rating": 4.6,
            "reviewCount": 95,
            "inStock": True,
            "featured": False,
            "badge": "Sale",
        },
        {
            "name": "RC Racing Car Pro",
            "description": "Professional-grade RC racing car with 2.4GHz remote. Reaches speeds up to 30km/h. For serious racers!",
            "price": 2499,
            "category": "remote-cars",
            "ageGroup": "8+",
            "image": "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=600&h=600&fit=crop",
            ],
            "rating": 4.5,
            "reviewCount": 34,
            "inStock": False,
            "featured": False,
        },
        {
            "name": "Classic Chess Set",
            "description": "Beautifully crafted wooden chess set with storage box. Perfect for learning and family game nights.",
            "price": 849,
            "category": "board-games",
            "ageGroup": "6-8",
            "image": "https://images.unsplash.com/photo-1586165368502-1bad197a6461?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1586165368502-1bad197a6461?w=600&h=600&fit=crop",
            ],
            "rating": 4.7,
            "reviewCount": 142,
            "inStock": True,
            "featured": False,
        },
        {
            "name": "Baby's First Rattle Set",
            "description": "Set of 5 colorful, safe rattles perfect for newborns. BPA-free and easy to grip for tiny hands.",
            "price": 349,
            "category": "baby-toys",
            "ageGroup": "0-2",
            "image": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=600&h=600&fit=crop",
            ],
            "rating": 4.4,
            "reviewCount": 88,
            "inStock": True,
            "featured": False,
        },
    ]
    
    # Clear existing and insert
    print("Seeding categories...")
    db.categories.delete_many({})
    db.categories.insert_many(categories)
    
    print("Seeding products...")
    db.products.delete_many({})
    db.products.insert_many(products)
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
