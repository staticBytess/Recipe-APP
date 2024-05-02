class returnHome extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <a href="/"><button>Return to Home Page</button></a>
        `
    }
}

class saveRecipe extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <a href="/addFave?value={{ recipe.id }}"><button type="submit">Add to Favorites</button></a>
        `
    }
}


customElements.define('return-home', returnHome)
customElements.define('save-recipe', saveRecipe)


