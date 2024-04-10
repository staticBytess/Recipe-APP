class bottomOptions extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <a href="/"><button>Return to Home Page</button></a>
        `
    }
}

customElements.define('bottom-options', bottomOptions)