//@ts-check

import { FlaskAImageService } from '../utils/FlaskAImageService.js'
import { AuthService } from './AuthService.js'
import { State } from '../utils/State.js'
import { Video } from '../utils/Video.js'
import { $ } from '../utils/$.js'
import { snackDanger } from '../utils/snacks.js'

const _flaskAImageService = new FlaskAImageService()
const _authService = new AuthService()

const videoUser = new Video('#videoUser')
const txtLogin = $('#txtLogin')
const txtPassword = $('#txtPassword')

const btnLogin = $('#btnLogin')
const btnFacingModeToggler = $('.video-facing-mode-toggler')

/** @type {number|null} */
let detectorInterval = null

const streamingState = new State(false)
streamingState.addChangeListener(async streaming => {
    if (streaming) {
        await videoUser.startStreaming()
        //detectorInterval = setInterval(() => detect(), 1000/FPS)
    }
    else {
        if (detectorInterval !== null) {
            clearInterval(detectorInterval)
            detectorInterval = null
        }

        videoUser.stopStreaming()
    }
})

// async function login() {
//     const blob = await videoUser.toBlob()
//     _flaskAImageService.a(blob)
// }

txtLogin.on('keypress', e => {
    if (e.key === 'Enter') {
        txtPassword.match.focus()
    }
})

txtPassword.on('keypress', e => {
    if (e.key === 'Enter') {
        btnLogin.match.click()
    }
})

btnLogin.on('click', async e => {
    const login = txtLogin.val() + ''
    const password = txtPassword.val() + ''

    if (login.trim() === '') return snackDanger('Please provide your email or username to continue')
    if (password.trim() === '') return snackDanger('Please provide your password to continue')

    btnLogin.prop('disabled', true)
    await _authService.login(login, password)
    btnLogin.prop('disabled', false)
})

btnFacingModeToggler.on('click', e => {
    videoUser.toggleFacingMode()
})

document.addEventListener('DOMContentLoaded', e => {
    streamingState.set(true)
})

document.addEventListener('visibilitychange', e => {
    streamingState.set(document.visibilityState === 'visible')
})