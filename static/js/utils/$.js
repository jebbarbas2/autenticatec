//@ts-check

export class DummyQuery {
    /** @type {HTMLElement[]} */ #matches
    
    /**
     * @param {string} selector 
     */
    constructor(selector) {
        const matches = [...document.querySelectorAll(selector)]

        if (matches.some(match => !(match instanceof HTMLElement))) {
            throw new Error('DummyQuery: All matches must be HTMLElement')
        }

        //@ts-ignore - Ya yo se que si son HTMLElement con lo de arriba
        this.#matches = matches
    }

    get matches() { return this.#matches }
    get match() { return this.#matches[0] }

    /**
     * @param {string} name 
     * @param {any} [value]
     */
    prop(name, value) {
        if (value === undefined) return this.match[name]
        this.#matches.forEach(match => match[name] = value)
        return this
    }

    /**
     * @param {string} [value] 
     */
    val(value){
        if (value === undefined) return this.prop('value')
        return this.prop('value', value)
    }

    /**
     * @param {string} event 
     * @param {any} listener 
     */
    on(event, listener){
        this.#matches.forEach(match => match.addEventListener(event, listener))
        return this
    }
}

/**
 * @param {string} selector 
 */
export function $(selector) {
    return new DummyQuery(selector)
}