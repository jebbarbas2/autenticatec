//@ts-check

import { snackDanger } from "../utils/snacks.js"

export class AuthService {
    static #instance

    constructor() {
        if (AuthService.#instance !== null) return AuthService.#instance
        AuthService.#instance = this
    }

    /**
     * @param {string} login 
     * @param {string} password 
     */
    async login(login, password) {
        const res = await fetch('/login', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login, password })
        })

        const resJson = await res.json()

        if (!res.ok) {
            return snackDanger(resJson.message)
        }
        else {
            window.location.href = resJson.data.redirect_url
        }   
    }
}