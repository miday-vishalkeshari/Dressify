Filter Parameters:

style mood: "Casual", "Formal", "Party", "Workout"

style cloth types: "Tshirts","Casual_Shirts","Formal_Shirts","Jeans","Track_Pants","Shorts","Trousers","Pants"

style footware type: "Casual_Sneakers", "Running_Shoes", "Formal_Shoes", "Loafers", "Sandals", "FlipFlops", "Boots", "HighHeels", "Brogues", "Derby_Shoes", "Oxfords", "Moccasins", "Espadrilles", "Slip_Ons", "Sliders", "Ankle_Boots", "Chappals"


body type: "Petite", "Column Female", "Inverted Triangle Female", "Apple", "Brick","Pear", "Hourglass", "Full Hourglass", "Rectangle", "Square","Inverted Triangle Male", "Triangle", "Column Male", "Trapezium", "Circle", "Oval"


skin colour: "Very Fair", "Fair", "Medium Fair", "Medium", "Medium Dark", "Dark", "Very Dark"


Seasons: "Spring", "Summer", "Monsoon", "Autumn", "Winter"

======================================================================================================================================================================================
Different body types can be accentuated or balanced with specific clothing styles:

Apple: Emphasize the lower body; opt for A-line dresses and V-neck tops.
Pear: Highlight the upper body; choose boat-neck tops and flared pants.
Hourglass: Accentuate the waist; fitted dresses and belts work well.
Rectangle: Create curves; use peplum tops and layered outfits.
Inverted Triangle: Balance shoulders with hips; wear wide-leg pants and V-neck tops

======================================================================================================================================================================================

Different occasions call for varying styles:

-->Casual: T-shirts, jeans, casual shirts, and shorts.
-->Formal: Formal shirts, trousers, and tailored pants.
-->Party: Stylish tops, dresses, and fashionable trousers.
-->Workout: Track pants, athletic shorts, and breathable T-shirts.


-->Casual: Casual_Sneakers, Sandals, FlipFlops, Slip_Ons, Sliders, Chappals
-->Formal: Formal_Shoes, Brogues, Derby_Shoes, Oxfords, Loafers
-->Sport/Active: Running_Shoes
-->Seasonal/Occasion: Boots, Ankle_Boots, Espadrilles, HighHeels, Moccasins
======================================================================================================================================================================================
Sample filter structure: 
Skin colour --> body type --> style mood --> style type 

private val colorCombinations = mapOf(
    "Very Fair" to mapOf(
        "Rectangle" to mapOf(
            "Casual" to listOf("T-shirts", "Jeans", "Sneakers"),
            "Formal" to listOf("Blazers", "Trousers", "Formal Shoes"),
            "Party" to listOf("Cocktail Dresses", "Heels", "Clutches"),
            "Workout" to listOf("Tank Tops", "Leggings", "Running Shoes")
        ),
        "Apple" to mapOf(
            "Casual" to listOf("Peplum Tops", "Straight Jeans", "Flats"),
            "Formal" to listOf("Wrap Dresses", "Pencil Skirts", "Heels"),
            "Party" to listOf("A-line Dresses", "Statement Jewelry", "Heels"),
            "Workout" to listOf("Loose T-shirts", "Track Pants", "Trainers")
        ),
        "Pear" to mapOf(
            "Casual" to listOf("Off-Shoulder Tops", "Wide-Leg Pants", "Sandals"),
            "Formal" to listOf("Blouses", "A-line Skirts", "Pumps"),
            "Party" to listOf("Fit-and-Flare Dresses", "Bold Earrings", "Heels"),
            "Workout" to listOf("Fitted Tops", "Yoga Pants", "Sneakers")
        ),
        "Hourglass" to mapOf(
            "Casual" to listOf("Fitted Tops", "Skinny Jeans", "Boots"),
            "Formal" to listOf("Sheath Dresses", "Blazers", "Heels"),
            "Party" to listOf("Bodycon Dresses", "Clutches", "Heels"),
            "Workout" to listOf("Sports Bras", "Leggings", "Running Shoes")
        ),
        "Inverted Triangle" to mapOf(
            "Casual" to listOf("V-neck Tops", "Wide-Leg Pants", "Flats"),
            "Formal" to listOf("Peplum Tops", "Straight Pants", "Heels"),
            "Party" to listOf("Empire-Waist Dresses", "Statement Necklaces", "Heels"),
            "Workout" to listOf("Loose Tops", "Joggers", "Trainers")
        )
    )
)

======================================================================================================================================================================================
tips: 
1. It's beneficial to avoid colors that closely match your skin tone to prevent a washed-out appearance.
2. 
