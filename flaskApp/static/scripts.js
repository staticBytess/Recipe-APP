class returnHome extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <a href="/"><button>Return to Home Page</button></a>
        `
    }
}
customElements.define('return-home', returnHome)