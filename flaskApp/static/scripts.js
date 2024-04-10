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
        <button type="submit">Save Recipe</button>
        `
    }
}


customElements.define('return-home', returnHome)
customElements.define('save-recipe', saveRecipe)