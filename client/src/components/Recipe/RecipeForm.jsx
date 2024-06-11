import React, { useState } from 'react';


function AddRecipe() {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [ingredients, setIngredients] = useState('');
    const [instructions, setInstructions] = useState('');
    const [photo, setPhoto] = useState(''); // Initialize to empty string
    const [tag, setTag] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('/recipes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    ingredients: ingredients,
                    instructions: instructions,
                    photo: photo,
                    tag: tag  
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to add recipe');
            }

            const newRecipe = await response.json();
            console.log('Recipe added:', newRecipe);

            // Set the success message
            setSuccessMessage('Recipe has been added');

            // Clear the form fields
            setTitle('');
            setDescription('');
            setIngredients('');
            setInstructions('');
            setPhoto('');
            setTag('');

        } catch (error) {
            console.error('Failed to add recipe:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Add Recipe</h2>
            <div>
                <label>Title:</label>
                <input
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                ></input>
            </div>
            <div>
                <label>Description:</label>
                <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                ></textarea>
            </div>
            <div>
                <label>Ingredients:</label>
                <textarea
                    value={ingredients}
                    onChange={(e) => setIngredients(e.target.value)}
                    required
                ></textarea>
            </div>
            <div>
                <label>Instructions:</label>
                <textarea
                    value={instructions}
                    onChange={(e) => setInstructions(e.target.value)}
                    required
                ></textarea>
            </div>
            <div>
                <label>Photo:</label>
                <input
                    type="text" 
                    value={photo}
                    onChange={(e) => setPhoto(e.target.value)}
                />
            </div>
            <div>
                <label>Category:</label>
                <select
                    value={tag}
                    onChange={(e) => setTag(e.target.value)}
                    required
                >
                    <option value="">Select Category</option>
                    <option value="1">Italian</option>
                    <option value="2">Mexican</option>
                    <option value="3">Asian</option>
                    <option value="4">Vegetarian</option>
                    <option value="5">Indian</option>
                    <option value="6">American</option>
                </select>
            </div>
            <button type="submit">Add Recipe</button>
            {successMessage && <p>{successMessage}</p>}
        </form>
    );
}

export default AddRecipe;
