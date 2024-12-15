# Lab Session: Tuesday
# Demo: 12/12/2024
# Anishka Raina(Ar933), YI GU(yg642), Group 5
import os
import pygame
import RPi.GPIO as GPIO
import json
import re

# Expanded Recipe Database in JSON format

recipes = {

    "Broccoli Soup": {

        "ingredients": ["broccoli", "cream", "butter"],

        "instructions": "1. Heat butter in a large saucepan over medium heat. 2. Add chopped broccoli and cook, stirring occasionally, until tender, about 5-7 minutes. 3. Stir in cream and cook for another 3 minutes. 4. Use an immersion blender or transfer to a blender to blend until smooth. 5. Return the soup to the saucepan, simmer for 5 minutes, and adjust seasoning with salt and pepper. Serve hot.",

        "image": "/home/pi/lab7/broccoli-cheese-soup.webp"

    },

    "Banana Smoothie": {

        "ingredients": ["banana", "cream"],

        "instructions": "1. Peel and slice bananas into small pieces. 2. Add bananas and cream to a blender. 3. Blend on high speed until smooth and creamy, about 1 minute. 4. Pour into a glass, chill for 10 minutes if desired, and serve immediately.",

        "image": "/home/pi/lab7/Banana_Smoothie-5.webp"

    },

    "Tomato Potato Curry": {

        "ingredients": ["tomato", "potato", "butter"],

        "instructions": "1. Heat butter in a deep skillet over medium heat. 2. Add diced potatoes and cook for 10 minutes, stirring frequently, until lightly golden. 3. Add chopped tomatoes, stir well, and cook until softened, about 5 minutes. 4. Add curry spices (such as turmeric, cumin, and coriander), stir, and cook for another 2 minutes. 5. Add water or broth, cover, and simmer for 20 minutes until potatoes are tender. Adjust seasoning with salt and pepper and serve hot.",

        "image": "/home/pi/lab7/potato-curry-aloo-curry.jpg"

    },

    "Banana Bread": {

        "ingredients": ["banana", "butter", "cream"],

        "instructions": "1. Preheat the oven to 350F (175C). 2. In a mixing bowl, mash the bananas until smooth. 3. Melt the butter and mix it into the mashed bananas. 4. Add cream, sugar, and eggs to the mixture and stir well. 5. Sift in flour, baking powder, and a pinch of salt, and fold gently until combined. 6. Pour the batter into a greased loaf pan. 7. Bake for 45-50 minutes or until a toothpick inserted in the center comes out clean. Cool before slicing.",

        "image": "/home/pi/lab7/Banana-Bread-LEAD-2-66837beab63c495292d89743c6767171.jpg"

    },

    "Creamy Butter Pasta": {

        "ingredients": ["cream", "butter"],

        "instructions": "1. Cook pasta in boiling salted water until al dente, then drain. 2. In a large skillet, melt butter over medium heat. 3. Add cream and whisk until it starts to thicken, about 3-4 minutes. 4. Toss the pasta into the skillet and mix until evenly coated. 5. Add grated Parmesan cheese (optional), season with salt and pepper, and serve immediately.",

        "image": "/home/pi/lab7/creamy_butter_pasta.jpeg"

    },

    "Banana Pancakes": {

        "ingredients": ["banana", "cream", "butter"],

        "instructions": "1. Mash the bananas in a large bowl until smooth. 2. Add cream, eggs, and a pinch of salt, and whisk until combined. 3. Gradually stir in flour until the batter is smooth. 4. Heat a non-stick pan over medium heat and grease it with butter. 5. Pour small portions of the batter into the pan and cook until bubbles appear on the surface, about 2 minutes. 6. Flip and cook for another 1-2 minutes until golden. Serve warm with syrup.",

        "image": "/home/pi/lab7/banana_pancake.jpeg"

    },

    "Butter Cookies": {

        "ingredients": ["butter", "cream"],

        "instructions": "1. Preheat the oven to 375F (190C). 2. In a mixing bowl, beat butter and sugar until light and fluffy. 3. Add cream and mix until combined. 4. Gradually add flour and mix until a soft dough forms. 5. Roll the dough into small balls and place them on a baking sheet lined with parchment paper. 6. Flatten slightly with a fork. 7. Bake for 12-15 minutes or until edges are golden. Cool on a wire rack before serving.",

        "image": "/home/pi/lab7/rack-of-butter-cookies-1.jpg"

    },

    "Fruit Salad": {

        "ingredients": ["banana", "cream"],

        "instructions": "1. Peel and slice bananas into thin rounds. 2. Combine bananas with other fruits (such as berries, apples, or grapes) in a large bowl. 3. Whisk cream with a little honey or sugar and drizzle over the fruits. 4. Toss gently to coat. Chill for 20 minutes before serving.",

        "image": "/home/pi/lab7/fruit-salad.jpg"

    },

    "Broccoli Stir-Fry": {

        "ingredients": ["broccoli", "butter"],

        "instructions": "1. Cut broccoli into bite-sized florets and wash thoroughly. 2. Heat butter in a large skillet or wok over medium heat. 3. Add broccoli and stir-fry for 5-7 minutes until tender-crisp. 4. Season with salt, pepper, and optional garlic or soy sauce. Serve as a side dish.",

        "image": "/home/pi/lab7/brocolo-stir-fry.jpeg"

    },

    "Potato Cream Soup": {

        "ingredients": ["potato", "cream"],

        "instructions": "1. Peel and dice potatoes into small cubes. 2. Boil the potatoes in salted water until tender, about 10-15 minutes, then drain. 3. Mash the potatoes and mix with cream until smooth. 4. Heat the mixture in a saucepan over medium heat until warm. 5. Adjust seasoning with salt and pepper and serve hot, garnished with fresh herbs.",

        "image": "/home/pi/lab7/potato-cream-soup.jpeg"

    },

    "Tomato Butter Toast": {

        "ingredients": ["tomato", "butter"],

        "instructions": "1. Toast slices of bread until golden. 2. Spread softened butter generously on the warm toast. 3. Top with thin slices of fresh tomato. 4. Sprinkle with salt, pepper, and optional fresh basil leaves. Serve immediately.",

        "image": "/home/pi/lab7/tomato-butter-toast.jpeg"

    },

    "Broccoli Potato Bake": {

        "ingredients": ["broccoli", "potato", "butter"],

        "instructions": "1. Preheat the oven to 375F (190C). 2. Boil diced potatoes and broccoli florets for 5-7 minutes, then drain. 3. Layer the vegetables in a greased baking dish. 4. Melt butter and pour over the vegetables. 5. Sprinkle with breadcrumbs and cheese (optional). 6. Bake for 20 minutes or until the top is golden and crispy. Serve warm.",

        "image": "/home/pi/lab7/brocolli-potato-bake.jpeg"

    },

    "Tomato Cream Pasta": {

        "ingredients": ["tomato", "cream"],

        "instructions": "1. Cook pasta in salted boiling water until al dente, then drain. 2. In a skillet, heat cream over medium heat and stir in diced tomatoes. 3. Cook until the tomatoes soften and the sauce thickens, about 5 minutes. 4. Toss the pasta in the sauce and mix well. Adjust seasoning with salt and pepper. Serve hot, garnished with Parmesan cheese.",

        "image": "/home/pi/lab7/tomato-cream-pasta.jpg"

    },

    "Banana Butter Wrap": {

        "ingredients": ["banana", "butter"],

        "instructions": "1. Spread softened butter evenly on a tortilla or flatbread. 2. Slice bananas into thin rounds and arrange them on the buttered tortilla. 3. Roll the tortilla tightly and secure with a toothpick if necessary. Serve immediately.",

        "image": "/home/pi/lab7/banana-butter-wrap.jpeg"

    },


    "Corn Salad": {

        "ingredients": ["corn", "butter", "onion"],

        "instructions": "1. Melt butter in a large skillet over medium heat. 2. Add diced onions and sauté until translucent, about 3 minutes. 3. Add the corn kernels and cook for another 5 minutes, stirring frequently. 4. Season with salt and pepper to taste. Serve warm as a side dish.",

        "image": "/home/pi/lab7/corn-salad.jpeg"

    },

    "Garlic Mashed Potatoes": {

        "ingredients": ["potato", "garlic", "butter", "cream"],

        "instructions": "1. Peel and dice potatoes into small cubes. 2. Boil the potatoes in salted water until fork-tender, about 15-20 minutes. 3. Drain the potatoes and return them to the pot. 4. Mash the potatoes while still warm. 5. In a small saucepan, melt butter and sauté minced garlic until fragrant. 6. Stir the garlic butter and warm cream into the mashed potatoes until smooth. Adjust seasoning with salt and pepper. Serve immediately.",

        "image": "/home/pi/lab7/garlic-mashed-potatoes.jpeg"

    },

    "Tomato Pepper Omelette": {

        "ingredients": ["egg", "pepper", "onion", "tomato"],

        "instructions": "1. Beat the eggs in a bowl and season with salt and pepper. 2. Dice onion, pepper, and tomato into small pieces. 3. Heat a non-stick skillet with a bit of oil or butter over medium heat. 4. Sauté the onion and pepper until softened, about 3-4 minutes. 5. Add the diced tomato and cook for another 2 minutes. 6. Pour the beaten eggs over the vegetables and cook until set, about 4-5 minutes. Fold the omelette in half and serve hot.",

        "image": "/home/pi/lab7/Banana_Smoothie-5.webp"

    },

    "Egg Salad": {

        "ingredients": ["egg", "cream", "onion"],

        "instructions": "1. Boil eggs for 8-10 minutes until hard-boiled. 2. Cool the eggs in ice water, then peel and chop them into small pieces. 3. Finely dice the onion and mix it with the eggs in a bowl. 4. Add cream and stir until the mixture is smooth and creamy. Season with salt and pepper to taste. Serve chilled on bread or lettuce.",

        "image": "/home/pi/lab7/egg-salad.jpeg"

    },

    "Tomato Garlic Pasta": {

        "ingredients": ["tomato", "garlic", "butter"],

        "instructions": "1. Cook pasta in salted boiling water until al dente, then drain. 2. In a large skillet, melt butter over medium heat. 3. Add minced garlic and sauté until fragrant, about 1 minute. 4. Add diced tomatoes and cook for 5 minutes until softened. 5. Toss the cooked pasta in the skillet until evenly coated. Serve hot, garnished with fresh basil and Parmesan cheese.",

        "image": "/home/pi/lab7/tomato-garlic-pasta.jpeg"

    },

    "Corn Chowder": {

        "ingredients": ["corn", "potato", "cream"],

        "instructions": "1. In a large pot, sauté diced potatoes in butter over medium heat for 5 minutes. 2. Add the corn kernels and cook for another 3 minutes. 3. Pour in cream and bring to a simmer. 4. Cook for 10-15 minutes until the potatoes are tender and the chowder thickens. Adjust seasoning with salt and pepper. Serve warm with fresh parsley.",

        "image": "/home/pi/lab7/corn-chowder.jpeg"

    },

    "Stuffed Bell Peppers": {

        "ingredients": ["pepper", "tomato", "onion"],

        "instructions": "1. Preheat the oven to 375F (190C). 2. Cut the tops off the bell peppers and remove the seeds and membranes. 3. In a skillet, sauté diced onion and tomato until soft. 4. Stuff the peppers with the onion-tomato mixture and place them in a baking dish. 5. Bake for 20-25 minutes until the peppers are tender. Serve warm.",

        "image": "/home/pi/lab7/stuffed-bell-pepper.jpeg"

    },

    "Egg Fried Rice": {

        "ingredients": ["egg", "onion", "corn"],

        "instructions": "1. Heat oil in a large skillet or wok over medium-high heat. 2. Sauté diced onion and corn kernels for 3-4 minutes until softened. 3. Push the vegetables to the side and scramble the eggs in the center of the skillet. 4. Add cooked rice and stir everything together until well mixed. Season with soy sauce and serve warm.",

        "image": "/home/pi/lab7/egg-fried-rice.jpeg"

    },

    "Garlic Bread": {

        "ingredients": ["garlic", "butter"],

        "instructions": "1. Preheat the oven to 375F (190C). 2. Mix softened butter with minced garlic and a pinch of salt. 3. Spread the garlic butter on slices of bread. 4. Place the bread on a baking sheet and bake for 8-10 minutes until golden and crispy. Serve warm.",

        "image": "/home/pi/lab7/garlic-bread.jpeg"

    },

    "Tomato Basil Soup": {

        "ingredients": ["tomato", "cream", "garlic"],

        "instructions": "1. Heat butter in a large pot over medium heat. 2. Sauté minced garlic until fragrant, about 1 minute. 3. Add diced tomatoes and cook for 10 minutes until soft. 4. Blend the mixture until smooth. 5. Stir in cream and bring to a gentle simmer. Garnish with fresh basil leaves and serve hot.",

        "image": "/home/pi/lab7/tomato-basil-souo.jpeg"

    },

    "Potato Egg Hash": {

        "ingredients": ["potato", "egg", "onion"],

        "instructions": "1. Heat oil in a skillet over medium heat. 2. Add diced potatoes and cook until golden and crispy, about 10 minutes. 3. Add diced onion and sauté until translucent. 4. Push the vegetables to the side and scramble eggs in the center of the skillet. Mix everything together and season with salt and pepper. Serve hot.",

        "image": "/home/pi/lab7/potato-egg-hash.jpeg"

    },

    "Vegetable Stir-Fry": {

        "ingredients": ["broccoli", "pepper", "onion"],

        "instructions": "1. Heat oil in a wok or large skillet over high heat. 2. Add chopped broccoli, bell peppers, and onions. 3. Stir-fry for 5-7 minutes until vegetables are tender but still crisp. 4. Add soy sauce and toss to coat. Serve immediately.",

        "image": "/home/pi/lab7/vegtable stir fry.jpeg"

    },

     "Broccoli Cheese Soup": {

        "ingredients": ["broccoli", "cream", "butter", "garlic"],

        "instructions": "1. Melt butter in a large pot over medium heat and sauté minced garlic until fragrant, about 1 minute. 2. Add chopped broccoli and cook, stirring occasionally, for 5-7 minutes until slightly softened. 3. Stir in cream and bring to a simmer. 4. Blend the mixture with an immersion blender or in a regular blender until smooth. 5. Return to the pot, add shredded cheese, and stir until melted and creamy. Season with salt and pepper to taste and serve hot.",

        "image": "/home/pi/lab7/broccoli-cheese-soup.webp"

    },

    "Tomato Corn Salsa": {

        "ingredients": ["tomato", "corn", "onion"],

        "instructions": "1. Dice the tomato and onion into small, even pieces. 2. Cook the corn kernels in boiling water for 2-3 minutes or until tender, then drain. 3. In a bowl, combine the diced tomato, onion, and cooked corn. 4. Season with salt, lime juice, and a pinch of chili powder if desired. Mix well and serve as a fresh side dish or dip.",

        "image": "/home/pi/lab7/tomato-corn-salsa.jpeg"

    },

    "Cornbread Muffins": {

        "ingredients": ["corn", "butter", "cream"],

        "instructions": "1. Preheat the oven to 400F (200C) and grease a muffin tin. 2. In a mixing bowl, combine cornmeal, melted butter, and cream. 3. Add sugar, baking powder, and a pinch of salt, then mix until a smooth batter forms. 4. Pour the batter into the prepared muffin tin, filling each cup about 2/3 full. 5. Bake for 20-25 minutes, or until the tops are golden brown and a toothpick inserted in the center comes out clean. Let cool slightly before serving.",

        "image": "/home/pi/lab7/cornbread-muffins.jpeg"

    },

    "Garlic Cream Pasta": {

        "ingredients": ["garlic", "cream", "butter"],

        "instructions": "1. Cook pasta in a large pot of boiling salted water until al dente, then drain. 2. In a skillet, melt butter over medium heat and sauté minced garlic until fragrant, about 1-2 minutes. 3. Stir in cream and bring to a simmer. 4. Cook for 3-5 minutes, stirring occasionally, until the sauce thickens slightly. 5. Toss the cooked pasta in the sauce until well coated. Serve immediately, garnished with Parmesan cheese and parsley if desired.",

        "image": "/home/pi/lab7/garlic_cream_pasta.jpeg"

    },

    "Vegetable Omelette": {

        "ingredients": ["egg", "onion", "broccoli", "pepper"],

        "instructions": "1. Beat the eggs in a bowl and season with salt and pepper. 2. Finely chop the onion, broccoli, and bell pepper. 3. Heat a non-stick skillet over medium heat and add a bit of butter or oil. 4. Sauté the chopped vegetables for 3-4 minutes until slightly softened. 5. Pour the beaten eggs over the vegetables and cook without stirring until the edges begin to set. 6. Fold the omelette in half and cook for another 1-2 minutes. Serve hot.",

        "image": "/home/pi/lab7/vegtable-omlette.jpeg"

    },

    "Creamed Corn": {

        "ingredients": ["corn", "cream", "butter"],

        "instructions": "1. Melt butter in a saucepan over medium heat. 2. Add the corn kernels and cook, stirring, for 3-4 minutes. 3. Stir in cream and bring to a gentle simmer. 4. Cook for 5-7 minutes, stirring occasionally, until the mixture thickens. 5. Season with salt and pepper to taste and serve warm as a comforting side dish.",

        "image": "/home/pi/lab7/creamed-corn.jpeg"

    },

    "Potato Garlic Gratin": {

        "ingredients": ["potato", "cream", "garlic", "butter"],

        "instructions": "1. Preheat the oven to 375F (190C). 2. Thinly slice the potatoes and mince the garlic. 3. In a small saucepan, heat cream with minced garlic over low heat until warm. 4. Arrange a layer of potatoes in a greased baking dish, then pour a small amount of the cream mixture over the top. Repeat the layers until all ingredients are used. 5. Dot the top with small pieces of butter and bake for 40-45 minutes, or until the potatoes are tender and the top is golden brown. Serve warm.",

        "image": "/home/pi/lab7/potato-garlic-gratin.jpeg"

    },

    "Egg Garlic Toast": {

        "ingredients": ["egg", "garlic", "butter"],

        "instructions": "1. Toast slices of bread until golden brown. 2. Spread softened garlic butter generously on the warm toast. 3. In a skillet, fry an egg sunny-side up or over-easy. 4. Place the fried egg on top of the garlic toast. Serve immediately, garnished with a sprinkle of salt and pepper.",

        "image": "/home/pi/lab7/egg-garlic-toast.jpeg"

    },

    "Creamy Tomato Corn Soup": {

        "ingredients": ["tomato", "corn", "cream"],

        "instructions": "1. In a large pot, heat diced tomatoes and corn over medium heat, stirring occasionally. 2. Add cream and bring to a gentle simmer. 3. Use an immersion blender to partially blend the mixture, leaving some chunks for texture. 4. Cook for an additional 5 minutes, stirring frequently. 5. Adjust seasoning with salt and pepper, and serve hot with a garnish of fresh herbs.",

        "image": "/home/pi/lab7/creamy-tomato-corn-soup.jpeg"

    },

    "Stuffed Potato Skins": {

        "ingredients": ["potato", "onion", "butter"],

        "instructions": "1. Preheat the oven to 400F (200C). 2. Cut baked potatoes in half and scoop out most of the flesh, leaving a thin shell. 3. Sauté diced onions in butter until soft. 4. Fill each potato skin with the onion mixture and top with a small piece of butter. 5. Bake for 10-15 minutes, or until the skins are crispy and golden. Serve hot.",

        "image": "/home/pi/lab7/stuffed-potato-skins.jpeg"

    },

    "Banana Corn Fritters": {

        "ingredients": ["banana", "corn", "egg"],

        "instructions": "1. In a mixing bowl, mash the banana until smooth. 2. Add corn kernels and a beaten egg, then mix until well combined. 3. Heat oil in a skillet over medium heat. 4. Drop small spoonfuls of the mixture into the skillet and fry for 2-3 minutes per side, or until golden and crispy. Drain on paper towels and serve warm.",

        "image": "/home/pi/lab7/banana-corn-fritters.jpeg"
    },
    "Banana Cream Parfait": {
        "ingredients": ["banana", "cream"],
        
        "instructions": "1. Whisk cream with a little sugar until soft peaks form. 2. Layer sliced bananas and whipped cream alternately in a glass. 3. Top with a sprinkle of crushed cookies or granola. Chill for 10 minutes before serving.",
        
        "image": "/home/pi/lab7/banana-cream-parfait.jpeg"
    },
    "Tomato Pepper Bruschetta": {
        "ingredients": ["tomato", "pepper", "garlic"],

        "instructions": "1. Dice tomatoes and bell peppers into small pieces. 2. Mix with minced garlic, olive oil, and balsamic vinegar. 3. Spoon the mixture onto toasted bread slices and serve immediately.",
        
        "image": "/home/pi/lab7/banana-cream-parfait.jpeg"
    },

}



# Improved Recipe Matching Algorithm

def find_recipes(available_ingredients):
    # Initialize a list to store recipe scores and other details
    recipe_scores = []

    # Iterate over each recipe and its details in the recipes dictionary
    for recipe, details in recipes.items():
        # Find the matching ingredients between available ingredients and recipe ingredients
        matching_ingredients = set(available_ingredients) & set(details["ingredients"])
        
        # Calculate the score as the ratio of matching ingredients to total ingredients in the recipe
        score = len(matching_ingredients) / len(details["ingredients"])
        
        # Split the instructions into individual steps using regex for numbering
        steps = re.split(r'\d+\.\s', details["instructions"])
        
        # Remove any empty strings and trim whitespace from each step
        steps = [step.strip() for step in steps if step]
        
        # Format each step with numbering (e.g., "Step 1: ...")
        steps = [f"Step {i}: {step}" for i, step in enumerate(steps, 1)]
        
        # Append the recipe name, score, formatted steps, and image path to the recipe_scores list
        recipe_scores.append({"name": recipe, "score": score, "instructions": steps, "path": details["image"]})

    # Sort recipes by their score in descending order (highest score first)
    recipe_scores = sorted(recipe_scores, key=lambda x: x["score"], reverse=True)
    
    # Return the sorted list of recipes
    return recipe_scores
